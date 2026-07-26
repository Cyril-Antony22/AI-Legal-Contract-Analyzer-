"""
Module 2 - OCR Processing
--------------------------
Responsible for turning an uploaded file (PDF or image) into plain text.

Pipeline:
1. If the file is a PDF -> convert every page into an image (pdf2image).
   If it's already an image -> use it directly.
2. Clean up each image with OpenCV (grayscale + threshold) so OCR is more
   accurate on scanned / photographed documents.
3. Run EasyOCR on each cleaned image and stitch the text together.
"""

import os
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import easyocr

# EasyOCR downloads its language model the first time it runs, and loading
# it is slow. We create ONE reader and reuse it for every request instead
# of creating a new one every time (that would be very slow).
_reader = None


def get_reader():
    global _reader
    if _reader is None:
        # gpu=False so this also works on machines without a GPU.
        # Set gpu=True if you have a CUDA-enabled GPU for much faster OCR.
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader

def pdf_to_images(pdf_path, poppler_path=None):
    """Convert every page of a PDF into a PIL Image."""
    return convert_from_path(
        pdf_path,
        poppler_path=r"D:\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )


def preprocess_image(pil_image):
    """
    Use OpenCV to clean up an image before OCR:
    - convert to grayscale
    - apply adaptive thresholding to make text stand out from the background
    This step is what "Image Processing (OpenCV)" refers to in the project spec.
    """
    img = np.array(pil_image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    processed = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 15
    )
    return processed


def extract_text_from_file(file_path, poppler_path=None):
    """
    Main entry point used by app.py.
    Returns the full extracted text of the uploaded contract as one string.
    """
    reader = get_reader()
    ext = file_path.rsplit(".", 1)[-1].lower()

    if ext == "pdf":
        pages = pdf_to_images(file_path, poppler_path=poppler_path)
    else:
        pages = [Image.open(file_path)]

    full_text = []
    for page_number, page_image in enumerate(pages, start=1):
        cleaned = preprocess_image(page_image)
        # detail=0 -> just return the text strings, not bounding boxes/confidence
        results = reader.readtext(cleaned, detail=0, paragraph=True)
        page_text = "\n".join(results)
        full_text.append(f"--- Page {page_number} ---\n{page_text}")

    return "\n\n".join(full_text)
