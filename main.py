import re
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from prompt import build_prompt
from vision import generate_blog
from dotenv import load_dotenv
load_dotenv() 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 시엔 도메인 제한 권장
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def parse_hashtags(text: str) -> list[str]:
    if "해시태그:" not in text:
        return []
    return text.split("해시태그:", 1)[1].strip().split()


# @app.post("/blog/generate")
# async def generate(
#     targetKeyword: str = Form(...),
#     photos: Optional[List[UploadFile]] = File(None),
# ):
#     photos = (photos or [])[:10]

#     prompt = build_prompt(targetKeyword)
#     blog_text = generate_blog(prompt, photos)

#     title = ""
#     body = blog_text

#     if "제목:" in blog_text:
#         title_part, rest = blog_text.split("제목:", 1)
#         title_line, body = rest.split("본문:", 1)
#         title = title_line.strip()

#     hashtags = parse_hashtags(body)

#     return JSONResponse(
#         {
#             "title": title,
#             "content": body.strip(),
#             "hashtags": hashtags,
#         }
#     )
@app.post("/blog/generate")
async def generate(
    targetKeyword: str = Form(...),
    photos: Optional[List[UploadFile]] = File(None),
):
    return {
        "title": "테스트 제목",
        "content": "테스트 본문입니다.\n여러 줄도 정상입니다.",
        "hashtags": ["#테스트", "#CORS", "#Render", "#FastAPI", "#OK"]
    }
    
@app.get("/cors-test")
def cors_test():
    return {"ok": True}