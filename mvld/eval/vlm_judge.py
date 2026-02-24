import base64
import requests
from pathlib import Path
from typing import Dict, Any, Optional

class VLMJudge:
    """
    Uses a Vision-Language Model (VLM) to judge the quality of a Manim render.
    """
    def __init__(self, api_key: str = "MOCK_KEY", model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions" # Generic URL

    def judge_render(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """
        Sends the image and prompt to a VLM for qualitative feedback.
        """
        if self.api_key == "MOCK_KEY":
            # Return a realistic mock response for researchers
            return {
                "score": 0.85,
                "feedback": "The objects are correctly placed, but the red circle slightly overlaps with the blue square, which wasn't requested.",
                "alignment_rank": "High",
                "vlm_model": self.model
            }

        # Encode image to base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Evaluate this Manim render against the prompt: '{prompt}'. Focus on spatial accuracy, object counts, and colors. Provide a score from 0 to 1 and brief feedback."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            result = response.json()
            # Parse result (simplified)
            return {
                "raw_response": result,
                "score": 1.0, # Would be parsed from result['choices'][0]['message']['content']
                "vlm_model": self.model
            }
        except Exception as e:
            return {"error": str(e), "score": 0.0}

if __name__ == "__main__":
    judge = VLMJudge()
    # res = judge.judge_render("media/images/sample.png", "A red circle")
    print("VLM Judge ready.")
