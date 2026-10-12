# Ma Durga Live Drawing and Colorization

This Python application colorizes a Ma Durga and lion line-art image, saves the
finished artwork, and animates the drawing in a window. It keeps the source
composition and dark outlines, then traces the visible lines progressively
before revealing the colorized result.

## Features

- Draws the linework progressively on a white canvas without showing a hand or
  cursor.
- Transitions from the traced line art to the colorized image.
- Uses traditional reds, oranges, golds, warm skin tones, and lion colors.
- Saves a full-resolution PNG before starting the preview.
- Supports Python 3.13 on Windows.

## Requirements

- Python 3.13
- OpenCV
- NumPy

Install the Python packages from this folder:

```powershell
python -m pip install opencv-python numpy
```

## Input image

Place the sketch in this folder using either filename:

1. `image_4.png` — preferred source
2. `ma_durga.jpg` — fallback source if `image_4.png` is absent

The program stops with a `FileNotFoundError` if neither image is available.

## Run

From this folder:

```powershell
python ma_durga.py
```

On Windows, you can also double-click `run_ma_durga.bat`.

The program writes `corrected_ma_durga_final.png` in this folder, then opens
the live drawing animation. Press **Q** or **Esc** to skip the drawing portion;
the final color image is still shown briefly. Close the window to finish.

## Project files

- `ma_durga.py` — image colorization and animation.
- `run_ma_durga.bat` — Windows launcher.
- `corrected_ma_durga_final.png` — generated output (created when the script runs).
- `LICENSE` — project license and attribution terms.
