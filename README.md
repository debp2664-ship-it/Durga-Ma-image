# Maa Durga Image Repository

This repository contains a Python-based creative coding project that draws a Maa Durga artwork using OpenCV contour extraction and Python Turtle.

## Project Overview

The main project lives in the [ma durga/Mataji-python-sketch](./ma%20durga/Mataji-python-sketch) folder. It reads a reference image, detects contours, and uses a live turtle cursor to recreate the artwork in a layered, sketch-like style.

## Included Files

- `ma durga/Mataji-python-sketch/mataji.py` — main drawing script
- `ma durga/Mataji-python-sketch/mataji.jpg` — reference image
- `ma durga/Mataji-python-sketch/run_mataji.bat` — Windows shortcut to run the script
- `ma durga/Mataji-python-sketch/LICENSE` — project licensing terms
- `ma durga/Mataji-python-sketch/IMAGE_LICENSE.md` — artwork-specific usage terms

## Requirements

Install the dependencies with:

```bash
pip install opencv-python numpy
```

## Run the project

From the project directory:

```bash
cd "ma durga/Mataji-python-sketch"
python mataji.py
```

On Windows, you can also double-click `run_mataji.bat`.

## Purpose

This project is a small creative coding experiment that blends:

- computer vision
- image contour analysis
- procedural art generation
- live animation via Python Turtle

It is intended for devotional, educational, and artistic exploration.

## Note

Please review the artwork-specific license in [ma durga/Mataji-python-sketch/IMAGE_LICENSE.md](./ma%20durga/Mataji-python-sketch/IMAGE_LICENSE.md) before redistributing or using the generated work commercially.
