# Temporal-Spatial Transposition

A mathematical visualization project that explores the concept of temporal-spatial transposition through animated helical paths in 4D space-time.

[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/IDES0/Temporal-Spatial-Transposition/blob/main/temporal_spatial_transpose_notebook.ipynb)

## 🎬 Overview

This project demonstrates how objects moving through 3D space over time can be visualized and analyzed through different dimensional perspectives. The core concept involves a circle moving along a helical path, and how this motion appears when viewed from different spatial-temporal orientations.

## 🚀 Main Application: Video-to-SpaceTime Processor

The **`video_to_spacetime.py`** is the primary tool that allows you to transform any video or GIF into temporal-spatial transpositions.

### Key Features:
- **Universal Input**: Load any video file (MP4, AVI, MOV) or GIF
- **Interactive GUI**: Real-time dimension selection and FPS control
- **Three Transposition Views**:
  - **X-Y-T**: Standard video playback (spatial view)
  - **Y-T-X**: Vertical slice through time at fixed X position
  - **T-X-Y**: Horizontal slice through time at fixed Y position
- **Real-time FPS Control**: Adjust playback speed during visualization
- **One-Click Export**: Export any view as a GIF with custom FPS

### How It Works:
1. **Load Media**: Input any video/GIF file
2. **Create Space-Time Volume**: Converts frames into a 4D data structure (Time × Height × Width × Channels)
3. **Interactive Slicing**: Real-time slicing through different dimensions
4. **Export Results**: Save transposed views as animated GIFs

### Usage:
```bash
python video_to_spacetime.py
# Enter filename when prompted (e.g., "surf3.gif")
```

### Interface Components:
- **Dimension Selector**: Radio buttons to switch between X-Y-T, Y-T-X, and T-X-Y views
- **FPS Text Box**: Direct input for custom playback speed
- **Export Button**: One-click GIF export with current settings
- **3D Preview**: Small 3D cube showing current slicing plane
- **Main View**: Large 2D visualization of the selected transposition

## 📚 Educational Notebook

The **`temporal_spatial_transpose_notebook.ipynb`** is an educational tool that helps users understand the underlying mathematical concepts through a simplified helical motion example.

### What It Demonstrates:
- **Mathematical Foundation**: Shows the helical equations x(t)=cos(t), y(t)=sin(t), z(t)=t
- **Four Synchronized Views**: Interactive demonstration of different spatial-temporal perspectives
- **Intersection Visualization**: Red dots show where the helix intersects with spatial planes
- **Real-time Frame Tracking**: Visual feedback of current animation state

### Key Features:
- **Synchronized Animation**: All four views update simultaneously
- **Intersection Visualization**: Red dots show where the helix intersects with current spatial planes
- **Real-time Frame Tracking**: Shows current animation frame across all views

## 🔬 Mathematical Foundation

The helical motion is defined by:
- **x(t) = cos(t)** - X position over time
- **y(t) = sin(t)** - Y position over time  
- **z(t) = t** - Time as the third spatial dimension

This creates a spiral path where the circle moves in a circular pattern while advancing upward through time.

## 🏄‍♂️ Example: Surf3.gif Analysis

The `surf3.gif` file demonstrates a real-world application of temporal-spatial transposition:

![Surf3 Animation](imports/surf3.gif)

### Transposition Exports

The `exports/` folder contains the transposed views of surf3.gif:

#### T-X-Y Transposition
![T-X-Y Transposition](exports/surf3_t-x-y_60fps.gif)

*Time vs X position, with Y fixed - shows temporal evolution of horizontal motion*

#### Y-T-X Transposition  
![Y-T-X Transposition](exports/surf3_y-t-x_60fps.gif)

*Y position vs Time, with X fixed - shows temporal evolution of vertical motion*

## 🛠️ Technical Implementation

### Requirements
```
numpy
matplotlib
opencv-python
Pillow
imageio
IPython
```

### Key Classes

#### `SpaceTimeVisualizer` (video_to_spacetime.py)
- **Main Processing Engine**: Converts videos to space-time volumes
- **Interactive GUI**: Real-time dimension selection and FPS control
- **Export Functionality**: One-click GIF generation
- **Multi-format Support**: Handles videos and GIFs seamlessly

#### `HelicalSpaceTimeVisualizer` (notebook)
- **Educational Tool**: Demonstrates mathematical concepts
- **Configurable Parameters**: Frames, cycles, and FPS
- **Real-time Intersection Calculations**: Shows spatial-temporal relationships
- **Synchronized Multi-view Rendering**: Four coordinated perspectives

### Animation Parameters
- **Frames**: 69 (optimized for smooth playback)
- **Cycles**: 2 (slower, more relaxed motion)
- **FPS**: 20 (smooth animation)
- **Circle Size**: 0.1 units (intersection tolerance)

## 🎯 Applications

This visualization technique has applications in:
- **Physics**: Understanding 4D space-time relationships
- **Computer Graphics**: Multi-dimensional animation analysis
- **Data Visualization**: Temporal-spatial data exploration
- **Mathematics**: Geometric transformations and projections
- **Video Analysis**: Understanding motion patterns in videos
- **Scientific Visualization**: Multi-dimensional data slicing

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Temporal-Spatial-Transposition
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Process Your Own Videos**:
   ```bash
   python video_to_spacetime.py
   # Enter your video filename when prompted
   ```

4. **Explore the Educational Notebook**:
   ```bash
   jupyter notebook temporal_spatial_transpose_notebook.ipynb
   ```

## 📁 Project Structure

```
Temporal-Spatial-Transposition/
├── video_to_spacetime.py                      # Main video processing utility
├── temporal_spatial_transpose_notebook.ipynb  # Educational demonstration
├── requirements.txt                           # Python dependencies
├── exports/                                   # Transposition examples
│   ├── surf3_t-x-y_60fps.gif                 # T-X-Y transposition
│   └── surf3_y-t-x_60fps.gif                 # Y-T-X transposition
├── surf3.gif                                  # Example source video
└── README.md                                  # This file
```

## 🔍 Understanding the Transpositions

### X-Y-T View (Standard)
- **X-axis**: Spatial width
- **Y-axis**: Spatial height  
- **Time**: Frame progression
- **Shows**: Normal video playback

### T-X-Y View
- **X-axis**: Time progression
- **Y-axis**: X position values
- **Fixed**: Y position
- **Shows**: How horizontal motion evolves over time

### Y-T-X View  
- **X-axis**: Time progression
- **Y-axis**: Y position values
- **Fixed**: X position
- **Shows**: How vertical motion evolves over time

## 🤝 Contributing

Feel free to contribute by:
- Adding new transposition views
- Improving visualization quality
- Adding support for different input formats
- Enhancing the mathematical foundations
- Optimizing performance for large videos

## 📄 License

This project is open source and available under the MIT License.

---

*Transform any video into temporal-spatial transpositions and explore the fascinating world of 4D space-time relationships!* 