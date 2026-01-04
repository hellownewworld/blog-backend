import base64
import os
import io
from typing import List

from fastapi import UploadFile
from openai import OpenAI
from dotenv import load_dotenv

from PIL import Image
import pillow_heif

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def normalize_image(file: UploadFile) -> tuple[str, bytes]:
    """
    업로드된 이미지를 OpenAI Vision에서 항상 처리 가능한 형태로 변환
    - HEIC → JPEG
    - JPEG/PNG/GIF/WEBP → 그대로 사용
    """
    file.file.seek(0)
    raw_bytes = file.file.read()

    # HEIC 변환 시도
    try:
        heif_file = pillow_heif.read_heif(raw_bytes)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
        )

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=90)
        return "image/jpeg", buffer.getvalue()

    except Exception:
        # HEIC가 아니면 원본 사용
        return file.content_type, raw_bytes


def to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def generate_blog(prompt: str, photos: List[UploadFile]) -> str:
    """
    텍스트 + 이미지(멀티모달)를 OpenAI Responses API로 전달하여
    블로그 글을 생성한다.
    """
    content = [
        {"type": "input_text", "text": prompt}
    ]

    for photo in photos:
        mime_type, image_bytes = normalize_image(photo)

        # OpenAI Vision 지원 포맷만 허용
        if mime_type not in [
            "image/jpeg",
            "image/png",
            "image/webp",
            "image/gif",
        ]:
            continue

        content.append(
            {
                "type": "input_image",
                "image_url": {
                    "url": f"data:{mime_type};base64,{to_base64(image_bytes)}"
                }
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
