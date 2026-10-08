import os
import requests
import base64
from typing import Optional, Tuple

class BodhanOCRService:
    def __init__(self):
        self.api_key = os.getenv("BODHAN_API_KEY")
        self.endpoint = os.getenv("BODHAN_OCR_ENDPOINT")
        
    def recognize_character(self, image_bytes: bytes, language: str) -> Tuple[Optional[str], float]:
        """
        Sends image to Bodhan IndicOCR API.
        Returns: (detected_character, confidence)
        """
        if not self.api_key or not self.endpoint:
            if os.getenv("GROQ_API_KEY"):
                return self._recognize_with_groq(image_bytes, language)
            raise ValueError("No OCR provider configured. Set BODHAN_API_KEY + BODHAN_OCR_ENDPOINT, or GROQ_API_KEY.")
        
        try:
            # Convert image to base64
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            data_uri = f"data:image/png;base64,{base64_image}"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "indic-ocr",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": data_uri
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            
            json_resp = response.json()
            
            detected_char = json_resp["choices"][0]["message"]["content"]
            
            if not detected_char:
                return None, 0.0
                
            return detected_char.strip(), 1.0
            
        except requests.exceptions.Timeout:
            raise ValueError("OCR service timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            print(f"Bodhan API Error: {e}")
            raise ValueError("Failed to reach OCR service.")
        except (KeyError, IndexError, ValueError, TypeError) as e:
            print(f"Bodhan API Malformed Response: {e}")
            raise ValueError("Received malformed response from OCR service.")

    def _recognize_with_groq(self, image_bytes: bytes, language: str) -> Tuple[Optional[str], float]:
        """Fallback OCR using a Groq-hosted vision model when Bodhan is not configured."""
        from groq import Groq

        mime = "image/png" if image_bytes[:8] == b"\x89PNG\r\n\x1a\n" else "image/jpeg"
        data_uri = f"data:{mime};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
        prompt = (
            f"This image shows a single handwritten {language} letter. "
            f"Reply with ONLY that one {language} character in Unicode, nothing else. "
            "If no letter is readable, reply with NONE."
        )
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=30)
            response = client.chat.completions.create(
                model=os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b"),
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_uri}},
                    ],
                }],
                temperature=0,
            )
            text = (response.choices[0].message.content or "").strip()
        except Exception as e:
            print(f"Groq Vision OCR Error: {e}")
            raise ValueError("Failed to reach OCR service.")

        # Drop any reasoning block and keep only the final answer line
        if "</think>" in text:
            text = text.split("</think>")[-1].strip()
        text = text.splitlines()[-1].strip().strip("'\"`.") if text else ""
        if not text or text.upper() == "NONE":
            return None, 0.0
        return text, 0.9
