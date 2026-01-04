import base64
import os
from typing import List
from fastapi import UploadFile
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def encode_image(file: UploadFile) -> str:
    file.file.seek(0)
    return base64.b64encode(file.file.read()).decode("utf-8")


def generate_blog(prompt: str, photos: List[UploadFile]) -> str:
    input_content = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                *[
                    {
                        "type": "input_image",
                        "image_base64": encode_image(photo),
                    }
                    for photo in photos
                ],
            ],
        }
    ]

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=input_content,
        max_output_tokens=900,
    )

    return response.output_text
