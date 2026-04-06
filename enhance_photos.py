#!/usr/bin/env python3
"""
Photo Enhancer — Batch image enhancement script
================================================
Fixes: underexposure, low contrast, haze/blur, dull colors
Output: sharp, vibrant, well-lit, modern-looking photos

Usage:
    python enhance_photos.py                         # enhances all images in current folder
    python enhance_photos.py photo1.jpg photo2.JPG   # specific files
    python enhance_photos.py --input ./raw --output ./enhanced

Requirements:
    pip install opencv-contrib-python Pillow numpy
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path
import argparse
import sys
import time


# ─────────────────────────────────────────────
# CORE ENHANCEMENT PIPELINE
# ─────────────────────────────────────────────

def fix_exposure_and_balance(img_bgr: np.ndarray) -> np.ndarray:
    """
    Fixes uneven lighting (shadows/highlights) using CLAHE
    (Contrast Limited Adaptive Histogram Equalization).
    Works in LAB colour space so hues stay accurate.
    """
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # clipLimit controls contrast boost; tileGridSize sets local region size
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l_eq = clahe.apply(l)

    merged = cv2.merge([l_eq, a, b])
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


def boost_vibrance_and_saturation(img_bgr: np.ndarray,
                                  saturation_factor: float = 1.35) -> np.ndarray:
    """
    Increases colour saturation for a vivid, modern look.
    Uses HSV space so luminance is unaffected.
    """
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_factor, 0, 255)
    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def sharpen_image(img_bgr: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Applies unsharp masking — sharpens edges without amplifying noise.
    strength=1.0 is a good default; increase to 1.5 for very blurry shots.
    """
    blurred = cv2.GaussianBlur(img_bgr, (0, 0), sigmaX=3)
    sharpened = cv2.addWeighted(img_bgr, 1.0 + strength, blurred, -strength, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def reduce_noise(img_bgr: np.ndarray) -> np.ndarray:
    """
    Fast Non-Local Means denoising — removes grain/sensor noise
    while keeping fine detail (hair, fabric texture).
    """
    return cv2.fastNlMeansDenoisingColored(img_bgr, None,
                                           h=7,        # luma noise strength
                                           hColor=7,   # chroma noise strength
                                           templateWindowSize=7,
                                           searchWindowSize=21)


def tone_curve_pop(img_bgr: np.ndarray) -> np.ndarray:
    """
    Applies a subtle S-curve to lift shadows and deepen highlights.
    This gives the 'punchy' modern look seen in edited photography.
    """
    # Build a gamma-like LUT with slight S-curve
    lut = np.arange(256, dtype=np.float32)
    # Lift shadows (gamma < 1 in shadows)
    lut = np.where(lut < 128,
                   128 * (lut / 128) ** 0.85,
                   255 - 128 * ((255 - lut) / 128) ** 0.95)
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    return cv2.LUT(img_bgr, lut)


def white_balance_auto(img_bgr: np.ndarray) -> np.ndarray:
    """
    Simple grey-world white balance — corrects colour casts
    (warm/yellow tints from indoor light, cool/blue from shade).
    """
    result = img_bgr.astype(np.float32)
    avg_b = np.mean(result[:, :, 0])
    avg_g = np.mean(result[:, :, 1])
    avg_r = np.mean(result[:, :, 2])
    avg_all = (avg_b + avg_g + avg_r) / 3.0

    result[:, :, 0] = np.clip(result[:, :, 0] * (avg_all / (avg_b + 1e-6)), 0, 255)
    result[:, :, 1] = np.clip(result[:, :, 1] * (avg_all / (avg_g + 1e-6)), 0, 255)
    result[:, :, 2] = np.clip(result[:, :, 2] * (avg_all / (avg_r + 1e-6)), 0, 255)
    return result.astype(np.uint8)


def enhance_photo(input_path: Path, output_path: Path,
                  preset: str = "balanced") -> bool:
    """
    Full enhancement pipeline for a single image.

    Presets:
        balanced  — best for group/outdoor photos (default)
        vivid     — more saturation + contrast (social media style)
        natural   — subtle, realistic corrections only
    """
    # ── Load ──────────────────────────────────────────────────────────────────
    img = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    if img is None:
        print(f"  ✗  Could not read: {input_path.name}")
        return False

    original_h, original_w = img.shape[:2]
    print(f"  → Loaded  {input_path.name}  ({original_w}×{original_h}px)")

    # ── Step 1: Noise reduction FIRST (before sharpening amplifies noise) ────
    img = reduce_noise(img)

    # ── Step 2: Auto white balance ────────────────────────────────────────────
    img = white_balance_auto(img)

    # ── Step 3: Exposure & local contrast (CLAHE) ────────────────────────────
    img = fix_exposure_and_balance(img)

    # ── Step 4: Tone curve (S-curve pop) ─────────────────────────────────────
    img = tone_curve_pop(img)

    # ── Step 5: Saturation boost ─────────────────────────────────────────────
    sat = {"balanced": 1.30, "vivid": 1.55, "natural": 1.15}.get(preset, 1.30)
    img = boost_vibrance_and_saturation(img, saturation_factor=sat)

    # ── Step 6: Sharpening ────────────────────────────────────────────────────
    sharp = {"balanced": 0.8, "vivid": 1.0, "natural": 0.5}.get(preset, 0.8)
    img = sharpen_image(img, strength=sharp)

    # ── Save with high quality ────────────────────────────────────────────────
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ext = output_path.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        cv2.imwrite(str(output_path), img,
                    [cv2.IMWRITE_JPEG_QUALITY, 97,
                     cv2.IMWRITE_JPEG_SAMPLING_FACTOR, cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444])
    elif ext == ".png":
        cv2.imwrite(str(output_path), img,
                    [cv2.IMWRITE_PNG_COMPRESSION, 1])  # fastest, best quality
    else:
        cv2.imwrite(str(output_path), img)

    size_kb = output_path.stat().st_size // 1024
    print(f"  ✓  Saved   {output_path.name}  ({size_kb} KB)")
    return True


# ─────────────────────────────────────────────
# BATCH PROCESSING
# ─────────────────────────────────────────────

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}


def collect_images(sources: list[str]) -> list[Path]:
    """Expand source paths (files or directories) into a flat image list."""
    images = []
    for src in sources:
        p = Path(src)
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS:
            images.append(p)
        elif p.is_dir():
            for ext in SUPPORTED_EXTS:
                images.extend(p.glob(f"*{ext}"))
                images.extend(p.glob(f"*{ext.upper()}"))
        else:
            print(f"[warn] Skipping unrecognised path: {src}")
    return sorted(set(images))


def main():
    parser = argparse.ArgumentParser(
        description="Batch photo enhancer — fixes lighting, sharpness & colour",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhance_photos.py                            # all images in current dir
  python enhance_photos.py img1.jpg img2.JPG          # specific files
  python enhance_photos.py --input ./raw              # all images in ./raw/
  python enhance_photos.py --input ./raw --output ./enhanced --preset vivid
        """,
    )
    parser.add_argument("files", nargs="*",
                        help="Image file(s) to enhance (optional)")
    parser.add_argument("--input", "-i", default=".",
                        help="Input folder (default: current directory)")
    parser.add_argument("--output", "-o", default="enhanced",
                        help="Output folder (default: ./enhanced/)")
    parser.add_argument("--preset", "-p",
                        choices=["balanced", "vivid", "natural"],
                        default="balanced",
                        help="Enhancement preset (default: balanced)")
    parser.add_argument("--suffix", "-s", default="_enhanced",
                        help="Suffix added to output filenames (default: _enhanced)")
    args = parser.parse_args()

    # Collect images
    if args.files:
        images = collect_images(args.files)
    else:
        images = collect_images([args.input])

    if not images:
        print("No supported images found. Supported formats:", ", ".join(SUPPORTED_EXTS))
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'─'*55}")
    print(f"  Photo Enhancer  |  preset: {args.preset}  |  {len(images)} image(s)")
    print(f"  Output → {output_dir.resolve()}")
    print(f"{'─'*55}\n")

    ok, fail = 0, 0
    t0 = time.time()

    for img_path in images:
        out_name = img_path.stem + args.suffix + img_path.suffix.lower()
        # Normalise extension to .jpg for non-PNG inputs
        if img_path.suffix.lower() not in (".png",):
            out_name = img_path.stem + args.suffix + ".jpg"
        out_path = output_dir / out_name

        success = enhance_photo(img_path, out_path, preset=args.preset)
        if success:
            ok += 1
        else:
            fail += 1

    elapsed = time.time() - t0
    print(f"\n{'─'*55}")
    print(f"  Done in {elapsed:.1f}s  |  {ok} enhanced  |  {fail} failed")
    print(f"  Results saved to: {output_dir.resolve()}")
    print(f"{'─'*55}\n")


if __name__ == "__main__":
    main()