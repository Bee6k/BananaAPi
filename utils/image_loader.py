"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: utils
File: image_loader.py
Description: Image processing and conversion utility for CustomTkinter & PIL.

CS THEME COVERAGE:
- Theme 3: Interoperability (Base64 Binary Decoding & Graphics Rendering)

VIDEO PRESENTATION TALKING POINTS:
1. "The ImageLoader utility handles image format interoperability."
2. "It converts raw Base64 binary strings returned by the REST API into PIL Images
   and wraps them into CustomTkinter 'CTkImage' components for smooth DPI-scaled UI rendering."
===============================================================================
"""

import base64
import io
from typing import Tuple, Optional
from PIL import Image
import customtkinter as ctk


def base64_to_pil_image(b64_string: str) -> Optional[Image.Image]:
    """
    Convert a Base64 encoded string into a PIL Image.

    Args:
        b64_string (str): Raw or Data-URI base64 string.

    Returns:
        Optional[PIL.Image.Image]: Loaded Image or None if parsing fails.
    """
    try:
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]
        image_bytes = base64.b64decode(b64_string)
        return Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        print(f"[ImageLoader Error] Failed to decode base64 string: {e}")
        return None


def create_ctk_image(
    pil_image: Image.Image,
    target_size: Tuple[int, int] = (500, 260)
) -> ctk.CTkImage:
    """
    Wrap a PIL Image into a high-DPI compatible CustomTkinter CTkImage.

    Args:
        pil_image (PIL.Image.Image): Base PIL Image.
        target_size (Tuple[int, int]): Width and height tuple.

    Returns:
        ctk.CTkImage: Formatted CustomTkinter image widget asset.
    """
    # Resize while maintaining aspect ratio if desired, or fit to size
    resized_pil = pil_image.copy().resize(target_size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(
        light_image=resized_pil,
        dark_image=resized_pil,
        size=target_size
    )
