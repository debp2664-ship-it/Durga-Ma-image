from pathlib import Path

import cv2
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
REQUESTED_SOURCE_PATH = BASE_DIR / "image_4.png"
FALLBACK_SOURCE_PATH = BASE_DIR / "ma_durga.jpg"
OUTPUT_PATH = BASE_DIR / "corrected_ma_durga_final.png"


def load_reference_image():
    source_path = (
        REQUESTED_SOURCE_PATH
        if REQUESTED_SOURCE_PATH.is_file()
        else FALLBACK_SOURCE_PATH
    )
    image = cv2.imread(str(source_path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(
            f"Could not find '{REQUESTED_SOURCE_PATH}' or '{FALLBACK_SOURCE_PATH}'."
        )
    return image


def polygon_mask(height, width, points):
    polygon = np.array(
        [[round(x * width), round(y * height)] for x, y in points],
        dtype=np.int32,
    )
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 255)
    return mask > 0


def ellipse_mask(height, width, center, radii):
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.ellipse(
        mask,
        (round(center[0] * width), round(center[1] * height)),
        (round(radii[0] * width), round(radii[1] * height)),
        0,
        0,
        360,
        255,
        -1,
    )
    return mask > 0


def apply_color(color_map, subject_mask, color, lighting, fillable):
    shade = np.clip(
        np.asarray(color, dtype=np.float32)[None, None, :]
        * lighting[:, :, None],
        0,
        255,
    )
    coverage = cv2.GaussianBlur(
        subject_mask.astype(np.float32),
        (0, 0),
        sigmaX=3.0,
    )
    coverage = np.clip(coverage, 0, 1) * fillable
    alpha = coverage[:, :, None]
    color_map[:] = np.clip(
        color_map.astype(np.float32) * (1 - alpha)
        + shade * alpha,
        0,
        255,
    ).astype(np.uint8)


def render_corrected_artwork(original_image):
    height0, width0 = original_image.shape[:2]
    width, height = width0 * 2, height0 * 2
    image = cv2.resize(
        original_image,
        (width, height),
        interpolation=cv2.INTER_CUBIC,
    )
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Keep only the inner portions of thick ink strokes for recoloring; retain
    # the outer ink edge and fine facial/decorative lines in their original dark.
    ink = (gray < 115).astype(np.uint8)
    distance_from_edge = cv2.distanceTransform(ink, cv2.DIST_L2, 5)
    fillable = distance_from_edge > 1.8

    y, x = np.mgrid[0:height, 0:width].astype(np.float32)
    x /= width
    y /= height
    lighting = np.clip(1.10 - 0.12 * x - 0.10 * y, 0.88, 1.10)
    color_map = np.full((height, width, 3), 255, dtype=np.uint8)

    # Lion: golden coat, orange-gold mane, and warm ivory paws/underside.
    lion_body = polygon_mask(
        height,
        width,
        [(0.37, 0.49), (0.61, 0.47), (0.79, 0.49), (0.91, 0.56),
         (0.97, 0.73), (0.95, 0.93), (0.47, 0.96), (0.41, 0.79)],
    )
    paws_and_underside = polygon_mask(
        height,
        width,
        [(0.10, 0.84), (0.43, 0.84), (0.50, 0.91), (0.46, 0.97),
         (0.10, 0.97)],
    ) | polygon_mask(
        height,
        width,
        [(0.70, 0.84), (0.95, 0.84), (0.95, 0.97), (0.70, 0.97)],
    )
    apply_color(color_map, fillable & lion_body, (36, 143, 226), lighting, fillable)
    apply_color(
        color_map,
        fillable & paws_and_underside,
        (220, 236, 249),
        lighting,
        fillable,
    )
    lion_head = polygon_mask(
        height,
        width,
        [(0.04, 0.42), (0.30, 0.41), (0.38, 0.53), (0.36, 0.70),
         (0.29, 0.79), (0.12, 0.78), (0.04, 0.65)],
    )
    lion_face = ellipse_mask(height, width, (0.205, 0.585), (0.105, 0.115))
    apply_color(
        color_map,
        fillable & lion_head,
        (36, 126, 211),
        lighting,
        fillable,
    )
    apply_color(
        color_map,
        fillable & lion_face,
        (64, 177, 250),
        lighting,
        fillable,
    )

    # Maa's arms and hands have warm skin tones; her hair stays deep brown.
    skin = ellipse_mask(height, width, (0.50, 0.245), (0.050, 0.074))
    arm_regions = [
        [(0.27, 0.20), (0.34, 0.18), (0.40, 0.31), (0.44, 0.45),
         (0.39, 0.52), (0.30, 0.47), (0.27, 0.35)],
        [(0.58, 0.17), (0.67, 0.17), (0.74, 0.28), (0.70, 0.39),
         (0.63, 0.44), (0.57, 0.35)],
        [(0.66, 0.31), (0.78, 0.28), (0.79, 0.39), (0.72, 0.46),
         (0.63, 0.41)],
    ]
    for region in arm_regions:
        skin |= polygon_mask(height, width, region)
    apply_color(color_map, fillable & skin, (136, 179, 250), lighting, fillable)

    # Blouse and red-orange sari are separate from the skin and lion.
    blouse = polygon_mask(
        height,
        width,
        [(0.425, 0.32), (0.57, 0.32), (0.615, 0.42), (0.57, 0.49),
         (0.425, 0.47), (0.40, 0.39)],
    )
    apply_color(color_map, fillable & blouse, (34, 100, 230), lighting, fillable)
    sari = polygon_mask(
        height,
        width,
        [(0.55, 0.35), (0.60, 0.39), (0.64, 0.48), (0.64, 0.56),
         (0.61, 0.65), (0.58, 0.73), (0.55, 0.80), (0.38, 0.80),
         (0.33, 0.76), (0.37, 0.70), (0.42, 0.63), (0.47, 0.56),
         (0.51, 0.48)],
    )
    apply_color(color_map, fillable & sari, (40, 47, 222), lighting, fillable)
    sari_hem = polygon_mask(
        height,
        width,
        [(0.34, 0.74), (0.39, 0.77), (0.53, 0.77), (0.57, 0.72),
         (0.55, 0.77), (0.52, 0.80), (0.38, 0.79)],
    )
    apply_color(
        color_map,
        fillable & sari & sari_hem,
        (36, 177, 255),
        lighting,
        fillable,
    )

    # Tiny repeated zardozi rosettes give the sari a woven, festive finish.
    brocade = np.zeros((height, width), dtype=np.uint8)
    for cy in np.arange(0.55, 0.72, 0.035):
        for cx in np.arange(0.415, 0.575, 0.035):
            center = (round(cx * width), round(cy * height))
            for angle in range(0, 360, 72):
                offset = (
                    round(5 * np.cos(np.deg2rad(angle))),
                    round(5 * np.sin(np.deg2rad(angle))),
                )
                cv2.circle(
                    brocade,
                    (center[0] + offset[0], center[1] + offset[1]),
                    2,
                    255,
                    -1,
                    cv2.LINE_AA,
                )
            cv2.circle(brocade, center, 2, 255, -1, cv2.LINE_AA)
    brocade_mask = (brocade > 0) & sari & fillable
    color_map[brocade_mask] = (28, 172, 255)

    # Glowing gold crown, halo, necklaces and ornaments.
    halo = ellipse_mask(height, width, (0.50, 0.15), (0.17, 0.14))
    halo_inner = ellipse_mask(height, width, (0.50, 0.15), (0.135, 0.115))
    halo &= ~halo_inner
    crown = polygon_mask(
        height,
        width,
        [(0.39, 0.04), (0.61, 0.04), (0.63, 0.18), (0.57, 0.22),
         (0.43, 0.22)],
    )
    jewelry = polygon_mask(
        height,
        width,
        [(0.43, 0.28), (0.57, 0.28), (0.61, 0.35), (0.58, 0.43),
         (0.42, 0.43), (0.39, 0.35)],
    )
    gold = halo | crown | jewelry
    apply_color(color_map, fillable & gold, (26, 166, 255), lighting, fillable)

    # Ruby and emerald accents in the mukut, halo, and central ornaments.
    for nx, ny, gem_color in [
        (0.455, 0.105, (35, 38, 222)),
        (0.545, 0.105, (35, 38, 222)),
        (0.475, 0.155, (54, 150, 38)),
        (0.525, 0.155, (54, 150, 38)),
        (0.500, 0.080, (35, 38, 222)),
        (0.500, 0.345, (35, 38, 222)),
    ]:
        gem = np.zeros((height, width), dtype=np.uint8)
        cv2.circle(
            gem,
            (round(nx * width), round(ny * height)),
            5,
            255,
            -1,
            cv2.LINE_AA,
        )
        gem_mask = (gem > 0) & fillable
        color_map[gem_mask] = gem_color

    # Metallic weapons: trident and left-side implement in gold; right implements
    # use silver highlights against gold shafts.
    trident = polygon_mask(
        height,
        width,
        [(0.294, 0.07), (0.303, 0.07), (0.309, 0.44), (0.294, 0.44)],
    )
    trident_head = polygon_mask(
        height,
        width,
        [(0.255, 0.07), (0.278, 0.09), (0.294, 0.13), (0.304, 0.09),
         (0.33, 0.07), (0.32, 0.15), (0.30, 0.18), (0.279, 0.16)],
    )
    right_weapons = polygon_mask(
        height,
        width,
        [(0.685, 0.12), (0.697, 0.12), (0.705, 0.45), (0.692, 0.45)],
    ) | polygon_mask(
        height,
        width,
        [(0.756, 0.18), (0.768, 0.18), (0.775, 0.44), (0.762, 0.44)],
    )
    apply_color(color_map, fillable & trident, (28, 166, 255), lighting, fillable)
    apply_color(
        color_map,
        fillable & trident_head,
        (28, 166, 255),
        lighting,
        fillable,
    )
    apply_color(
        color_map,
        fillable & right_weapons,
        (40, 160, 244),
        lighting,
        fillable,
    )
    silver = right_weapons & (np.sin(x * 180) > 0.65)
    apply_color(color_map, fillable & silver, (194, 213, 232), lighting, fillable)

    # Restore the original dark ink and its anti-aliased contours.
    alpha = np.clip((180.0 - gray.astype(np.float32)) / 65.0, 0, 1)
    alpha *= np.clip((2.8 - distance_from_edge) / 1.0, 0, 1)
    ink_color = np.array((35, 25, 36), dtype=np.float32)
    result = np.clip(
        color_map.astype(np.float32) * (1 - alpha[:, :, None])
        + ink_color * alpha[:, :, None],
        0,
        255,
    ).astype(np.uint8)
    return result


def animate_colorization(colored_image):
    window_name = "Maa Durga - Live Colorization"
    display_width = min(colored_image.shape[1], 1000)
    display_height = round(
        colored_image.shape[0] * display_width / colored_image.shape[1]
    )
    colored_preview = cv2.resize(
        colored_image,
        (display_width, display_height),
        interpolation=cv2.INTER_AREA,
    )
    gray = cv2.cvtColor(colored_preview, cv2.COLOR_BGR2GRAY)
    ink = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)[1]
    contours, _ = cv2.findContours(
        ink,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_NONE,
    )
    contours = sorted(
        (
            contour
            for contour in contours
            if cv2.arcLength(contour, False) >= 12
        ),
        key=lambda contour: cv2.arcLength(contour, True),
        reverse=True,
    )
    strokes = []
    chunk_size = 36
    for contour in contours:
        simplified = cv2.approxPolyDP(contour, 0.9, True).reshape(-1, 2)
        if len(simplified) < 2:
            continue
        closed_path = np.vstack((simplified, simplified[0]))
        for start in range(0, len(closed_path) - 1, chunk_size - 1):
            segment = closed_path[start:start + chunk_size]
            if len(segment) >= 2:
                strokes.append(segment.reshape(-1, 1, 2))

    try:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, display_width, display_height)
        image = np.full_like(colored_preview, 255)
        strokes_per_frame = 2
        stopped = False
        for start in range(0, len(strokes), strokes_per_frame):
            for stroke in strokes[start:start + strokes_per_frame]:
                cv2.polylines(
                    image,
                    [stroke],
                    False,
                    (38, 27, 40),
                    2,
                    cv2.LINE_AA,
                )
            cv2.imshow(window_name, image)
            if cv2.waitKey(30) & 0xFF in (27, ord("q")):
                stopped = True
                break

        if not stopped:
            # Once the full line drawing is traced, bring in its finished color.
            frame_count = 30
            for frame in range(1, frame_count + 1):
                progress = frame / frame_count
                smooth_progress = progress * progress * (3 - 2 * progress)
                image = cv2.addWeighted(
                    image,
                    1 - smooth_progress,
                    colored_preview,
                    smooth_progress,
                    0,
                )
                cv2.imshow(window_name, image)
                if cv2.waitKey(30) & 0xFF in (27, ord("q")):
                    break
        cv2.imshow(window_name, colored_preview)
        cv2.waitKey(2000)
    except cv2.error as exc:
        print(f"Live animation unavailable; saved image is unaffected: {exc}")
    finally:
        cv2.destroyAllWindows()


def main():
    source = load_reference_image()
    corrected = render_corrected_artwork(source)
    if not cv2.imwrite(
        str(OUTPUT_PATH),
        corrected,
        [cv2.IMWRITE_PNG_COMPRESSION, 3],
    ):
        raise OSError(f"Could not write corrected artwork to '{OUTPUT_PATH}'.")
    print(f"Corrected artwork written to: {OUTPUT_PATH}")
    print("Starting live colorization preview...")
    animate_colorization(corrected)


if __name__ == "__main__":
    main()
