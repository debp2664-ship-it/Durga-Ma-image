# Ma Durga Artwork and Live Drawing

A Python 3.13 OpenCV project that colorizes a Ma Durga and lion sketch, retains
its original dark linework, saves a PNG, and progressively animates the drawing.

## Project

The application is in [ma durga/Ma-Durga-sketch](./ma%20durga/Ma-Durga-sketch/).
Its README contains setup, input image, and animation details.

## Quick start on Windows

Install the dependencies:

```powershell
python -m pip install opencv-python numpy
```

Add a source sketch to the project folder. `image_4.png` is preferred;
`ma_durga.jpg` is used as the fallback. Then run:

```powershell
cd "ma durga\Ma-Durga-sketch"
python ma_durga.py
```

Alternatively, double-click `run_ma_durga.bat`.

The generated image is saved as `corrected_ma_durga_final.png`. The live
animation first traces the artwork on white, then reveals its colorized finish.

Review the [project license](./ma%20durga/Ma-Durga-sketch/LICENSE) before
redistributing or using the artwork commercially.
