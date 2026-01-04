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
    content = [{"type": "input_text", "text": prompt}]

    for photo in photos:
        mime_type = photo.content_type  # ⭐ 핵심
        if mime_type not in ["image/jpeg", "image/png", "image/webp", "image/gif"]:
            continue  # 혹시 모를 비이미지 방어

        content.append(
            {
                "type": "input_image",
                "image_url": f"data:{mime_type};base64,{encode_image(photo)}",
            }
        )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": content,
            }
        ],
        max_output_tokens=900,
    )

    return response.output_text
