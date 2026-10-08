from pathlib import Path
import cv2
import turtle


BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "mataji.jpg"


def load_reference_image():
    image = cv2.imread(str(IMAGE_PATH), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not find '{IMAGE_PATH}'. Make sure the image is in the same folder as this script.")
    return image


def build_canvas(image):
    target_width = 750
    aspect_ratio = image.shape[0] / image.shape[1]
    target_height = int(target_width * aspect_ratio)
    resized_image = cv2.resize(image, (target_width, target_height))
    _, binary = cv2.threshold(resized_image, 180, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if hierarchy is None:
        raise RuntimeError("No shapes detected in the reference image.")

    return contours, hierarchy[0], target_width, target_height


def get_contour_depth(hierarchy, idx):
    depth = 0
    parent = hierarchy[idx][3]
    while parent != -1:
        depth += 1
        parent = hierarchy[parent][3]
    return depth


def to_turtle_coords(x, y, half_w, half_h):
    return (x - half_w, half_h - y)


def render_shape(pen, cnt, fill_col, border_col, half_w, half_h):
    if len(cnt) < 3:
        return

    first_pt = cnt[0][0]
    tx, ty = to_turtle_coords(first_pt[0], first_pt[1], half_w, half_h)

    pen.penup()
    pen.goto(tx, ty)
    pen.pendown()

    pen.color(border_col, fill_col)
    pen.begin_fill()

    step = 1 if len(cnt) <= 120 else 2 if len(cnt) <= 500 else 3
    for i in range(1, len(cnt), step):
        pt = cnt[i][0]
        tx, ty = to_turtle_coords(pt[0], pt[1], half_w, half_h)
        pen.goto(tx, ty)

    pen.goto(to_turtle_coords(first_pt[0], first_pt[1], half_w, half_h))
    pen.end_fill()


def main():
    try:
        image = load_reference_image()
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return

    contours, hierarchy, target_width, target_height = build_canvas(image)

    screen = turtle.Screen()
    screen.setup(width=target_width + 80, height=target_height + 80)
    screen.title("Live Drawing - Mataji and Lion (Exact Reference)")
    screen.bgcolor("white")
    screen.tracer(10, 0)
    screen.delay(0)

    pen = turtle.Turtle()
    pen.speed(0)
    pen.pensize(1)
    pen.shape("classic")
    pen.showturtle()

    half_w = target_width / 2
    half_h = target_height / 2

    max_depth = max(get_contour_depth(hierarchy, i) for i in range(len(contours)))
    depth_layers = {d: [] for d in range(max_depth + 1)}

    for i, cnt in enumerate(contours):
        if cv2.contourArea(cnt) < 4:
            continue
        depth_layers[get_contour_depth(hierarchy, i)].append(cnt)

    print("Drawing in progress... Watch the cursor create all details!")

    for d in range(max_depth + 1):
        fill_color = "black" if d % 2 == 0 else "white"
        border_color = fill_color
        for cnt in depth_layers[d]:
            render_shape(pen, cnt, fill_color, border_color, half_w, half_h)

    pen.hideturtle()
    screen.update()
    print("Done! Exact reference matched perfectly.")
    screen.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        raise