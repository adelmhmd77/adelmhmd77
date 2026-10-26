"""Prep a photo for ASCII conversion: remove background, CLAHE contrast, composite on white.
Usage: python scripts/prep_photo.py source-photo.jpg   -> source-prepped.png"""
import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
cut = remove(Image.open(src).convert("RGB")).convert("RGBA")

gray = cv2.cvtColor(np.array(cut.convert("RGB")), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)

alpha = np.array(cut)[:, :, 3] / 255.0
out = (gray * alpha + 255 * (1 - alpha)).astype("uint8")  # background -> pure white
Image.fromarray(out).save("source-prepped.png")
print("wrote source-prepped.png")
