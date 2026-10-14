"""
===============================================================================
BANANA GAME - ADVANCED CS EDUCATIONAL APPLICATION
Package: engine
File: banana_api.py
Description: HTTP Client interfacing with Marc Conrad's Banana REST API.

CS THEME COVERAGE:
- Theme 3: Interoperability (HTTP Protocol & Remote REST API Integration)

VIDEO PRESENTATION TALKING POINTS:
1. "Interoperability is demonstrated through HTTP communication with Marc Conrad's remote REST API."
2. "The BananaAPIClient initiates GET requests to 'https://marcconrad.com/uob/banana/api.php'."
3. "It handles payload parsing for both JSON and CSV formats with base64 encoded binary data."
4. "We enforce robust exception handling for HTTP 500 errors, network timeouts, and provide
   an offline fallback generator to ensure zero UI crashes even during server downtime."
===============================================================================
"""

import base64
import io
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Dict, Any, Optional


class BananaAPIClient:
    """
    HTTP REST Client responsible for communicating with Marc Conrad's Banana Game API.

    API Endpoint: https://marcconrad.com/uob/banana/api.php
    Query Parameters:
      - out: 'json' or 'csv' (default 'json')
      - base64: 'yes' or 'no' (default 'no')
    """

    PRIMARY_URL = "https://marcconrad.com/uob/banana/api.php"
    DEFAULT_TIMEOUT = 4.5  # seconds timeout for snappy HTTP requests & quick fallback

    def __init__(self, use_base64: bool = True, output_format: str = "json") -> None:
        """
        Initialize the Banana API Client.

        Args:
            use_base64 (bool): Whether to request base64 encoded image string.
            output_format (str): Desired output format ('json' or 'csv').
        """
        self.use_base64: bool = use_base64
        self.output_format: str = output_format.lower()

    def fetch_puzzle(self) -> Tuple[Image.Image, int, str]:
        """
        Perform HTTP GET request to fetch a new banana math equation puzzle.

        Returns:
            Tuple[PIL.Image.Image, int, str]:
                - PIL Image object of the equation.
                - Integer solution (0-9).
                - Source info text / metadata.

        Raises:
            Exception: If network fails and offline generator is invoked.
        """
        params = {
            "out": self.output_format,
            "base64": "yes" if self.use_base64 else "no"
        }

        try:
            response = requests.get(self.PRIMARY_URL, params=params, timeout=self.DEFAULT_TIMEOUT)
            response.raise_for_status()

            if self.output_format == "csv":
                return self._parse_csv_response(response.text)
            else:
                return self._parse_json_response(response.json())

        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"[BananaAPI Client Warning] HTTP Request failed: {e}. Utilizing fallback offline generator.")
            return self._generate_fallback_puzzle(str(e))

    def _parse_json_response(self, data: Dict[str, Any]) -> Tuple[Image.Image, int, str]:
        """
        Parse JSON payload from Banana API.

        JSON Format:
        {
            "question": "<URL or Base64 String>",
            "solution": 4
        }
        """
        question_str = data["question"]
        solution = int(data["solution"])

        if self.use_base64 or not question_str.startswith("http"):
            image = self._decode_base64_to_image(question_str)
            source_info = "Marc Conrad REST API (Base64 JSON Payload)"
        else:
            image = self._download_image_from_url(question_str)
            source_info = f"Marc Conrad REST API (Direct URL: {question_str})"

        return image, solution, source_info

    def _parse_csv_response(self, text: str) -> Tuple[Image.Image, int, str]:
        """
        Parse CSV payload from Banana API.

        CSV Format:
        <question_string>,<solution>
        """
        parts = text.strip().split(",")
        if len(parts) < 2:
            raise ValueError("CSV response format invalid.")

        question_str = parts[0].strip()
        solution = int(parts[1].strip())

        if question_str.startswith("http"):
            image = self._download_image_from_url(question_str)
            source_info = "Marc Conrad REST API (CSV URL Payload)"
        else:
            image = self._decode_base64_to_image(question_str)
            source_info = "Marc Conrad REST API (CSV Base64 Payload)"

        return image, solution, source_info

    def _decode_base64_to_image(self, b64_string: str) -> Image.Image:
        """
        Decode base64 binary string into a PIL Image.

        Args:
            b64_string (str): Base64 encoded image string.

        Returns:
            PIL.Image.Image: Decoded Image.
        """
        # Handle data URI scheme header if present
        if "," in b64_string:
            b64_string = b64_string.split(",", 1)[1]

        image_data = base64.b64decode(b64_string)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        return image

    def _download_image_from_url(self, url: str) -> Image.Image:
        """
        Download binary image from HTTP URL.

        Args:
            url (str): Remote image URL.

        Returns:
            PIL.Image.Image: Downloaded Image.
        """
        res = requests.get(url, timeout=self.DEFAULT_TIMEOUT)
        res.raise_for_status()
        image = Image.open(io.BytesIO(res.content)).convert("RGB")
        return image

    def _generate_fallback_puzzle(self, error_msg: str) -> Tuple[Image.Image, int, str]:
        """
        Generates a synthetic math puzzle image locally when network connection fails.
        Ensures offline resilience and seamless presentation demo.

        Returns:
            Tuple[PIL.Image.Image, int, str]: Local Image, Solution, Source status.
        """
        val1 = random.randint(1, 5)
        val2 = random.randint(1, 4)
        op = random.choice(["+", "*"])
        
        if op == "+":
            solution = val1 + val2
        else:
            solution = val1 * val2

        # Create PIL Canvas
        width, height = 500, 250
        image = Image.new("RGB", (width, height), color=(25, 25, 45))
        draw = ImageDraw.Draw(image)

        # Draw stylish equation card
        draw.rectangle([10, 10, width - 10, height - 10], outline=(241, 196, 15), width=3)
        
        # Text rendering
        equation_text = f"🍌 {val1}  {op}  🍌 {val2}  =  ?"
        fallback_notice = "Offline Mode (Fallback Engine)"

        try:
            font_lg = ImageFont.truetype("arial.ttf", 36)
            font_sm = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font_lg = ImageFont.load_default()
            font_sm = ImageFont.load_default()

        # Center equation text
        draw.text((width // 2 - 120, height // 2 - 30), equation_text, fill=(255, 255, 255), font=font_lg)
        draw.text((width // 2 - 110, height - 40), fallback_notice, fill=(231, 76, 60), font=font_sm)

        source_info = f"Offline Fallback Engine (HTTP Issue: {error_msg[:30]}...)"
        return image, solution, source_info
