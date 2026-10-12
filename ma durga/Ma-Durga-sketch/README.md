# Ma Durga Live Drawing and Colorization

A Python desktop project that colorizes a Ma Durga and lion line-art image,
saves a high-resolution PNG, and animates the drawing in an OpenCV window.
The animation progressively traces the image outlines on a clean white canvas,
then transitions to the finished color artwork. It does not display a hand,
cursor, or drawing tool.

## Features

- Traditional red, orange, and gold colors with warm skin and lion tones.
- Gold brocade accents, small crown gems, and metallic weapon highlights.
- Original composition, fine details, and dark outlines retained from the
  reference sketch.
- Live contour-tracing animation followed by a smooth reveal of the completed
  colors.
- Output image saved before the animation starts.
- Python 3.13 support; tested on Windows.

## Requirements

- Windows with Python 3.13 installed
- OpenCV (`opencv-python`)
- NumPy

Install the dependencies from PowerShell:

```powershell
python -m pip install opencv-python numpy
```

If you have multiple Python versions installed, use the Python 3.13 executable
explicitly:

```powershell
py -3.13 -m pip install opencv-python numpy
```

## Source image

Place the source sketch in this project folder. The program checks for these
files in the following order:

1. `image_4.png` — preferred source image
2. `ma_durga.jpg` — fallback image

If neither is present or OpenCV cannot read the selected image, the program
reports an error instead of generating a misleading output.

### Important: input composition

The color masks and subject regions in `ma_durga.py` are designed around the
project's Ma Durga-and-lion composition. A source image with a different layout,
crop, or aspect ratio can cause colors to land on the wrong areas. Use a source
with the same composition for the expected result.

## Run the application

Open PowerShell in this folder and run:

```powershell
python ma_durga.py
```

Alternatively, double-click `run_ma_durga.bat` in Windows Explorer. The batch
file changes to its own directory before starting the script.

The script first processes the image and saves the output. It then opens the
live animation window. Press **Q** or **Esc** to skip the outline-tracing
sequence. The final color image is shown briefly at the end; close the window
or wait for it to close.

## Output

The generated image is saved beside the script as:

```text
corrected_ma_durga_final.png
```

The output dimensions are twice the source image's width and height. Running
the program again replaces this generated output with the latest result.

## How it works

1. **Load the reference:** OpenCV loads `image_4.png` if present, otherwise
   `ma_durga.jpg`.
2. **Prepare the line art:** The source is enlarged to twice its original
   dimensions. OpenCV identifies dark ink and protects the finer linework.
3. **Apply color regions:** Polygon and ellipse masks define the broad subject
   areas (including skin, clothing, ornaments, weapons, and the lion). A gentle
   lighting multiplier is applied, followed by gold trim, brocade accents, and
   gem details.
4. **Restore outlines:** The source's dark contour details are composited above
   the color layers.
5. **Save the image:** The finished PNG is written before the preview begins.
6. **Animate the drawing:** The program extracts contours from the colored
   artwork, simplifies them into short paths, and progressively renders those
   paths on white. It then blends the traced linework into the final colored
   image.

## Project files

| File | Purpose |
| --- | --- |
| `ma_durga.py` | Image processing, colorization, output saving, and animation |
| `run_ma_durga.bat` | Windows launcher |
| `image_4.png` | Optional preferred input sketch |
| `ma_durga.jpg` | Fallback input sketch |
| `corrected_ma_durga_final.png` | Generated image |
| `LICENSE` | License and attribution terms |

## Troubleshooting

### “Could not find … image”

Put `image_4.png` or `ma_durga.jpg` in the same folder as `ma_durga.py`.
Check that the filename and extension match exactly.

### “No module named cv2” or “No module named numpy”

Install the dependencies with the same Python interpreter used to run the
script:

```powershell
python -m pip install opencv-python numpy
```

### The animation window does not open

The output PNG is saved before the animation starts. Open
`corrected_ma_durga_final.png` manually to view it. Run the program from a
desktop session that supports graphical windows rather than a headless
terminal.

### The colors do not align with my source

The color masks assume the reference image's original subject positions and
composition. Start with the included fallback sketch or use a compositionally
matching source.

## License

Review [LICENSE](LICENSE) before redistributing the project or using its
artwork commercially. Preserve required creator attribution.
