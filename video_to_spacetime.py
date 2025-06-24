import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import RadioButtons, Button, TextBox
import cv2
from PIL import Image
import os
import imageio

class SpaceTimeVisualizer:
    def __init__(self, file_path):
        # Load video/gif and convert to space-time volume
        self.file_path = file_path
        frames = self._load_media()
        
        # Try to detect original FPS if it's a video file
        self.fps = 20  # Default FPS
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in ['.gif', '.png', '.jpg', '.jpeg']:
            try:
                cap = cv2.VideoCapture(file_path)
                self.fps = cap.get(cv2.CAP_PROP_FPS)
                if self.fps <= 0 or self.fps > 1000:  # Allow very high FPS but reject invalid values
                    self.fps = 20
                cap.release()
            except:
                pass  # Use default if detection fails
        
        # Frame interval in milliseconds
        self.interval = 1000 / self.fps
        
        # Create space-time volume and normalize
        self.volume = np.stack(frames, axis=0)  # (time, height, width, channels)
        self.volume = self.volume.astype(float)
        # Normalize each channel separately
        for c in range(self.volume.shape[-1]):
            channel = self.volume[..., c]
            channel_min, channel_max = channel.min(), channel.max()
            if channel_max > channel_min:
                self.volume[..., c] = (channel - channel_min) / (channel_max - channel_min)
        
        self.time, self.height, self.width, self.channels = self.volume.shape
        print(f"Media dimensions: Time={self.time}, Height={self.height}, Width={self.width}, Channels={self.channels}")
        print(f"Playback rate: {self.fps:.1f} FPS (can be adjusted with text input)")
        print(f"Note: Actual maximum FPS is limited by your hardware capabilities")
        
        # Set up the figure
        plt.ion()  # Turn on interactive mode
        self.fig = plt.figure(figsize=(12, 8))
        
        # Create main 2D axis
        self.ax_2d = plt.axes([0.2, 0.1, 0.7, 0.8])
        
        # Create small 3D axis in the corner
        self.ax_3d = plt.axes([0.02, 0.6, 0.15, 0.35], projection='3d')
        
        # Add radio buttons for dimension selection
        rax = plt.axes([0.02, 0.25, 0.15, 0.15])
        self.radio = RadioButtons(rax, ('X-Y-T', 'Y-T-X', 'T-X-Y'))
        self.radio.on_clicked(self.dimension_changed)
        
        # Add export button
        bax = plt.axes([0.02, 0.1, 0.15, 0.08])
        self.button = Button(bax, 'Export GIF')
        self.button.on_clicked(self.export_button_clicked)
        
        # Add FPS text box for direct input
        tbox_ax = plt.axes([0.02, 0.2, 0.15, 0.04])
        self.fps_textbox = TextBox(
            tbox_ax, 'FPS:', 
            initial=str(int(self.fps))
        )
        self.fps_textbox.on_submit(self.update_fps_from_textbox)
        
        # Initialize state
        self.current_view = 'X-Y-T'
        self.frame = 0
        self.anim = None
        
        # Store base name for exports
        self.base_name = os.path.splitext(os.path.basename(file_path))[0]

    def _load_media(self):
        """Load frames from either video or gif file"""
        _, ext = os.path.splitext(self.file_path)
        frames = []
        
        if ext.lower() == '.gif':
            # Load GIF using PIL
            gif = Image.open(self.file_path)
            try:
                while True:
                    # Convert to RGB
                    frame = np.array(gif.convert('RGB'))
                    frames.append(frame)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass  # End of GIF file
        else:
            # Load video using OpenCV
            cap = cv2.VideoCapture(self.file_path)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # Convert from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)
            cap.release()
        
        if not frames:
            raise ValueError(f"Could not load frames from {self.file_path}")
            
        return frames
        
    def dimension_changed(self, label):
        if self.anim is not None:
            self.anim.event_source.stop()
            self.anim = None  # Clear reference before creating a new one
        self.current_view = label
        self.frame = 0  # Reset frame counter
        self.start_animation()  # Restart animation with new view
        
    def update(self, frame):
        self.frame = frame
        
        # Clear only the content, not the entire figure
        self.ax_2d.cla()
        self.ax_3d.cla()
        
        # Set 3D view angle
        self.ax_3d.view_init(elev=20, azim=45)
        
        # Update based on selected view
        if self.current_view == 'X-Y-T':
            # 2D view: regular video playback
            slice_data = self.volume[frame]
            self.ax_2d.imshow(slice_data)
            self.ax_2d.set_xlabel('X')
            self.ax_2d.set_ylabel('Y')
            self.ax_2d.set_title(f'Frame {frame} (X-Y plane)', pad=20)
            plane_pos = frame / (self.time - 1) if self.time > 1 else 0  # Normalize to [0,1]
            
        elif self.current_view == 'Y-T-X':
            # 2D view: vertical slice through time at fixed X
            # For color, we'll take slices through each channel and combine
            slice_data = np.zeros((self.time, self.height, 3))
            for c in range(3):
                slice_data[..., c] = self.volume[:, :, frame, c]
            self.ax_2d.imshow(slice_data, aspect='auto')
            self.ax_2d.set_xlabel('T')
            self.ax_2d.set_ylabel('Y')
            self.ax_2d.set_title(f'X = {frame} (Y-T plane)', pad=20)
            plane_pos = frame / (self.width - 1) if self.width > 1 else 0  # Normalize to [0,1]
            
        else:  # T-X-Y
            # 2D view: horizontal slice through time at fixed Y
            # For color, we'll take slices through each channel and combine
            slice_data = np.zeros((self.time, self.width, 3))
            for c in range(3):
                slice_data[..., c] = self.volume[:, frame, :, c]
            self.ax_2d.imshow(slice_data, aspect='auto')
            self.ax_2d.set_xlabel('X')
            self.ax_2d.set_ylabel('T')
            self.ax_2d.set_title(f'Y = {frame} (T-X plane)', pad=20)
            plane_pos = frame / (self.height - 1) if self.height > 1 else 0  # Normalize to [0,1]
        
        # Add grid to 2D view
        self.ax_2d.grid(True, alpha=0.3)
        
        # Simple 3D visualization
        self._setup_3d_axes()
        self._plot_3d_box()
        self._plot_simple_plane(self.current_view.split('-')[2], plane_pos)
        
        plt.draw()
        return self.ax_2d, self.ax_3d
    
    def _setup_3d_axes(self):
        """Setup 3D axes with proper scaling and ticks"""
        # Set cube aspect ratio (1:1:1)
        self.ax_3d.set_box_aspect((1, 1, 1))
        
        # Set ticks to show dimensions
        self.ax_3d.set_xticks([0, 1])
        self.ax_3d.set_xticklabels(['0', str(self.width)])
        self.ax_3d.set_yticks([0, 1])
        self.ax_3d.set_yticklabels(['0', str(self.height)])
        self.ax_3d.set_zticks([0, 1])
        self.ax_3d.set_zticklabels(['0', str(self.time)])
        
        # Set small font size for tick labels
        self.ax_3d.tick_params(axis='both', which='major', labelsize=6)
        
        # Set axis limits for unit cube
        self.ax_3d.set_xlim(0, 1)
        self.ax_3d.set_ylim(0, 1)
        self.ax_3d.set_zlim(0, 1)
    
    def _plot_3d_box(self):
        """Plot unit cube wireframe"""
        # Plot vertices
        x = np.array([0, 1])
        y = np.array([0, 1])
        z = np.array([0, 1])
        
        # Create box edges with thinner lines
        for i in [0, 1]:
            for j in [0, 1]:
                self.ax_3d.plot([x[0], x[1]], [y[j], y[j]], [z[i], z[i]], 'b-', alpha=0.2, linewidth=0.5)
                self.ax_3d.plot([x[j], x[j]], [y[0], y[1]], [z[i], z[i]], 'b-', alpha=0.2, linewidth=0.5)
                self.ax_3d.plot([x[j], x[j]], [y[i], y[i]], [z[0], z[1]], 'b-', alpha=0.2, linewidth=0.5)
    
    def _plot_simple_plane(self, axis, value):
        """Plot a simple scanning plane in unit cube"""
        # Create a finer mesh for the plane
        u = np.linspace(0, 1, 2)
        v = np.linspace(0, 1, 2)
        U, V = np.meshgrid(u, v)
        
        if axis == 'T':
            X, Y = U, V
            Z = np.full_like(X, value)
        elif axis == 'X':
            Y, Z = U, V
            X = np.full_like(Y, value)
        else:  # Y
            X, Z = U, V
            Y = np.full_like(X, value)
        
        # Plot the plane with higher alpha for visibility
        surf = self.ax_3d.plot_surface(X, Y, Z, color='red', alpha=0.5)
    
    def update_fps_from_textbox(self, text):
        """Update FPS from text input"""
        try:
            new_fps = float(text)
            if new_fps <= 0:
                print("FPS must be positive, using 1")
                new_fps = 1
                self.fps_textbox.set_val("1")
            elif new_fps > 1000:
                print("FPS capped at 1000")
                new_fps = 1000
                self.fps_textbox.set_val("1000")
                
            self.fps = new_fps
            self.interval = 1000 / self.fps
                
            # Restart animation with new speed
            self.restart_animation()
            print(f"FPS set to {self.fps:.1f}")
            
        except ValueError:
            # Restore previous value if input is invalid
            print("Invalid FPS value, using previous setting")
            self.fps_textbox.set_val(str(int(self.fps)))
    
    def restart_animation(self):
        """Helper to restart animation with current settings"""
        if self.anim is not None:
            self.anim.event_source.stop()
        self.start_animation()

    def start_animation(self):
        """Start or restart animation with current FPS"""
        if self.current_view == 'X-Y-T':
            frames = self.time
        elif self.current_view == 'Y-T-X':
            frames = self.width
        else:  # T-X-Y
            frames = self.height
            
        # Create new animation and keep reference to prevent garbage collection
        self.anim = FuncAnimation(self.fig, self.update, frames=frames,
                                interval=self.interval, blit=False)
        plt.draw()
        
        # Store reference to animation to prevent deletion warning
        self.fig.canvas.animation = self.anim

    def export_button_clicked(self, event):
        """Handle export button click"""
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Generate output filename based on current view and FPS
        output_filename = f"{self.base_name}_{self.current_view.lower()}_{int(self.fps)}fps.gif"
        output_path = os.path.join('exports', output_filename)
        
        # Temporarily disable the button
        self.button.label.set_text('Exporting...')
        self.fig.canvas.draw_idle()
        
        try:
            # Export the current view
            if self.current_view == 'X-Y-T':
                frames = self.time
                data = self.volume
            elif self.current_view == 'Y-T-X':
                frames = self.width
                data = np.zeros((frames, self.time, self.height, 3))
                for x in range(frames):
                    for c in range(3):
                        data[x, :, :, c] = self.volume[:, :, x, c]
            else:  # T-X-Y
                frames = self.height
                data = np.zeros((frames, self.time, self.width, 3))
                for y in range(frames):
                    for c in range(3):
                        data[y, :, :, c] = self.volume[:, y, :, c]

            # Convert float array back to uint8 for saving
            data = (data * 255).astype(np.uint8)
            
            # Calculate duration in ms based on current FPS
            duration = int(1000 / self.fps)
            
            # Save frames as GIF with current FPS
            with imageio.get_writer(output_path, mode='I', duration=duration) as writer:
                for i in range(frames):
                    frame = data[i]
                    writer.append_data(frame)
            
            # Update button text to show success
            self.button.label.set_text('Export Complete!')
            print(f"Export complete! Saved to {output_path} at {self.fps:.1f} FPS")
            
        except Exception as e:
            # Update button text to show error
            self.button.label.set_text('Export Failed!')
            print(f"Export failed: {str(e)}")
        
        # Reset button text after 2 seconds
        self.fig.canvas.draw_idle()
        plt.pause(2)
        self.button.label.set_text('Export GIF')
        self.fig.canvas.draw_idle()

    def run(self):
        self.start_animation()
        plt.show(block=True)

def main():
    file_path = input("Enter path to video or GIF file: ")
    visualizer = SpaceTimeVisualizer("imports/" + file_path)
    visualizer.run()

if __name__ == "__main__":
    main() 