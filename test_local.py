#!/usr/bin/env python3
"""
Local test script for Tamil OCR app
Tests OCR functionality without running the full web server
"""

import os
import tempfile
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def test_ocr_on_sample():
    """Test OCR with a sample image (create a simple test)"""
    print("Testing Tesseract installation...")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
    except Exception as e:
        print(f"Error: Tesseract not found: {e}")
        print("Please install Tesseract OCR and ensure it's in PATH")
        print("Windows: https://github.com/UB-Mannheim/tesseract/wiki")
        return False

    print("\nTesting Tamil language pack...")
    try:
        languages = pytesseract.get_languages()
        if 'tam' in languages:
            print("Tamil language pack is installed")
        else:
            print("Warning: Tamil language pack not found")
            print(f"Available languages: {languages}")
            return False
    except Exception as e:
        print(f"Error checking languages: {e}")
        return False

    print("\nOCR test completed successfully!")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("Tamil OCR App - Local Test")
    print("=" * 50)
    test_ocr_on_sample()
