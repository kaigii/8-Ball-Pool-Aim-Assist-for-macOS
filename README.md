<div align="center">

# 8-Ball-Pool-Aim-Assist-for-macOS

[繁體中文](README.zh-TW.md)


![alt text](https://img.shields.io/badge/macOS-12.0%2B-blue)
![alt text](https://img.shields.io/badge/Python-3.9%2B-green)
![alt text](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)

**A computer vision-based aim assist tool designed for playing 8 Ball Pool on macOS. It uses real-time image analysis to detect white aiming lines in the game screen and draws extended, stable prediction paths to help players make more accurate shots.**

</div>

---

## 📸 Demo

<div align="center">

**Game Screen with Aim Assist Overlay:**
<img width="700" alt="Game Screen with Aim Assist Overlay" src="https://github.com/user-attachments/assets/235f035f-c62a-4296-b3be-0e59e63aa2ff" />

**Real-time Parameter Tuner:**
<img alt="Real-time Parameter Tuner" src="https://github.com/user-attachments/assets/2466d522-b804-441a-806f-cc8960a21d72" />

</div>
Through an intuitive GUI interface, you can adjust all image processing parameters in real-time to find the optimal settings for your screen.

## ✨ Features

<div align="center">

### 🎯 **Core Capabilities**

</div>

| Feature | Description | Impact |
|---------|-------------|---------|
| ⚡ **Real-time Screen Analysis** | Captures specified game areas with millisecond-level processing | Instant response for seamless gameplay |
| 🔍 **Advanced Image Processing** | Uses bilateral filtering, Canny edge detection, and other algorithms to precisely extract line features | Crystal-clear line detection |
| 🎯 **Dual Hough Transform** | Detects both long and short line segments separately, improving detection rates at different viewing angles | Reliable detection from any angle |
| 🛡️ **Point Cloud Verification** | Uses RANSAC principles to verify and filter the most reliable line segments through edge point cloud support, eliminating noise interference | Noise-free, accurate results |
| ✨ **Smooth Line Tracking** | Exclusive LineTracker module eliminates line flickering and provides elegant fade-out effects | Professional, stable visual feedback |
| 🪟 **Non-intrusive Overlay** | Transparent overlay window built with PySide6 that can be superimposed on the game without affecting mouse events | Zero interference with gameplay |
| 🎛️ **Real-time Parameter Tuner** | Built-in powerful GUI parameter adjustment tool (tuner.py) for real-time fine-tuning of all visual processing parameters | Perfect customization for your setup |

## 🚀 Getting Started

<div align="center">

### 🛠️ **Quick Setup Guide**

</div>

### 📋 Prerequisites
> Make sure you have Python 3.9 or higher installed on your Mac.

### ⚡ Installation

<details>
<summary><b>🔧 Step 1: Clone the repository</b></summary>

```bash
git clone https://github.com/kaigii/8-Ball-Pool-Aim-Assist-for-macOS.git
cd 8-Ball-Pool-Aim-Assist-for-macOS
```

</details>

<details>
<summary><b>📦 Step 2: Install dependencies</b></summary>

It's recommended to install in a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

</details>

## 🎮 Usage

<div align="center">

### 🎯 **Game Setup & Configuration**

</div>

### 📱 **Step 1: Project game screen to Mac**
> Use macOS's built-in "iPhone Screen Mirroring" feature or any other screen mirroring app to project your mobile game screen completely to your Mac desktop.

### 🎯 **Step 2: Set up pool table capture area**
> This is the most critical step! You need to manually specify the area for the program to analyze.

<div align="center">

| Action | Description |
|--------|-------------|
| 📐 **Measure** | Press `Command + Shift + 4` on your Mac. The cursor will become a cross and display current coordinates. |
| 🎯 **Position** | Move the mouse to the top-left corner of the pool table area in the game window and note the x and y coordinates. |
| 📏 **Calculate** | Drag the mouse to the bottom-right corner to calculate the **width** and **height** of the rectangle. |
| ⚙️ **Configure** | Open the `config.py` file in the project and modify the values in the `GAME_WINDOW_RECT` dictionary. |

</div>

### 🚀 **Step 3: Run the main program**
When everything is ready, execute in the terminal:

```bash
python3 main.py
```

> The program will start a transparent overlay window and automatically open the parameter tuner. You should now see detected aiming lines on the game screen.

## 🛠️ Configuration and Fine-tuning

The core configuration of this project is divided into two parts: `config.py` file for basic behavior and appearance settings, and the Tuner interface for fine-tuning image recognition accuracy.

### config.py File Settings
This file controls the core behavior and visual style of the auxiliary lines.

- **GAME_WINDOW_RECT**:
  - Purpose: Defines the screen capture area.
  - Adjustment: As described in "Usage", use Command+Shift+4 to measure and fill in the actual pixel coordinates and size of the pool table in the game.

- **HSV_WHITE_LOWER / HSV_WHITE_UPPER**:
  - Purpose: Defines the "white" range that the program should recognize. This is crucial for filtering out the game's auxiliary lines.
  - Adjustment: If line recognition is poor, you can fine-tune these values. Usually the range from `[0, 0, 200]` to `[180, 30, 255]` works for most situations.

- **USE_DUAL_HOUGH**:
  - Purpose: Switch line detection mode. True means using both long and short line segment detectors simultaneously, adapting to more situations; False uses only a single detector.
  - Adjustment: Keeping True usually works best.

- **LINE_ALPHA_DEFAULT**:
  - Purpose: Initial opacity (0-255) of newly detected auxiliary lines.
  - Adjustment: Higher values make lines more solid. 40 is a relatively soft initial value.

- **LINE_FADE_STEP**:
  - Purpose: Opacity reduction per frame when lines disappear.
  - Adjustment: Higher values make lines disappear faster. 8 provides a smooth fade-out effect.

- **LINE_WIDTH / LINE_COLOR**:
  - Purpose: Control the width (pixels) and color (RGB) of auxiliary lines.
  - Adjustment: Adjust according to personal preference.

- **ENABLE_TUNER**:
  - Purpose: Determines whether to automatically open the Tuner adjustment window when starting the main program.
  - Adjustment: When you find satisfactory parameters, you can set this to False for a cleaner execution.

### Tuner Real-time Parameter Adjustment
When running `main.py`, the Tuner window will automatically open, allowing you to adjust image processing parameters in real-time through sliders and immediately see results in the preview window. All your adjustments are automatically saved to the `params_ransac.json` file.

**Preview Window Goals:**
- **Left (Edge Detection)**: Ideally, this window should be completely black with only clear, clean white auxiliary lines remaining. Other desktop patterns (like the deer) should be completely filtered out.
- **Right (Detection Results)**: Green "point clouds" should be densely distributed on white auxiliary lines, and blue "Hough line segments" should perfectly coincide with auxiliary lines.

**Slider Functions:**
- **Bilateral Filter**: Image smoothing filter. Usually keep small values to remove slight image noise.
- **Canny Edge**: Key to edge detection.
  - **T1 and T2**: Control sensitivity. Adjust these two values until there's minimal noise and clearest lines in the left preview window.
- **min_inliers**: How many green point clouds a line needs to support to be considered valid. Appropriately increasing this value can filter out incorrect short lines.
- **Hough Long / Hough Short**: Control line segment detection algorithms.
  - **Threshold**: Detection threshold, higher values are more strict.
  - **MinLineLen**: Minimum accepted line segment length.
  - **MaxLineGap**: Maximum allowed gap between points on a line segment.

## 📄 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

This means you are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license.

For the full license text, see the [Creative Commons website](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## ❤️ Contributing

Contributions are welcome! Whether it's reporting a bug, suggesting a feature, or submitting a pull request, your help is appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

 