"""
MedLingo — Private Medical Document Understanding
Powered by Gemma 4 via Ollama. All processing stays on your device.
"""

import base64
import json
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="MedLingo", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Detect if we are running in a demo environment (Hugging Face or Colab)
IS_DEMO = os.getenv("SPACE_ID") is not None or os.getenv("COLAB_GPU") is not None

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# Use e2b for demos (faster on CPU), e4b for local use
DEFAULT_MODEL = "gemma4:e2b" if IS_DEMO else "gemma4:e4b"
GEMMA_MODEL = os.getenv("GEMMA_MODEL", DEFAULT_MODEL)

SYSTEM_PROMPT = """You are MedLingo, a medical document assistant. Your job is to help patients understand their medical documents — prescriptions, lab results, discharge summaries, radiology reports, and more.

Rules:
1. Read the document in the image carefully and identify its type.
2. Extract ALL relevant information: medications, dosages, lab values, diagnoses, instructions.
3. Explain everything in clear, simple language that a non-medical person can understand.
4. Flag any values that are outside normal ranges and explain what that means.
5. If a target language is specified, provide the full explanation in that language.
6. Always include a disclaimer that this is for informational purposes and does not replace professional medical advice.
7. Structure your response with clear sections using markdown headers.

Be warm, reassuring, and thorough. Patients reading medical documents are often anxious — help them feel informed and empowered."""

LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt": "Portuguese",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "bn": "Bengali",
    "ur": "Urdu",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "th": "Thai",
    "pl": "Polish",
    "nl": "Dutch",
    "it": "Italian",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
    "el": "Greek",
    "cs": "Czech",
    "ro": "Romanian",
    "hu": "Hungarian",
    "uk": "Ukrainian",
    "ru": "Russian",
    "id": "Indonesian",
    "ms": "Malay",
    "tl": "Filipino",
    "sw": "Swahili",
    "am": "Amharic",
    "ha": "Hausa",
    "yo": "Yoruba",
}


@app.get("/", response_class=HTMLResponse)
async def root():
    return Path("static/index.html").read_text()


@app.get("/api/languages")
async def get_languages():
    return LANGUAGES


@app.post("/api/analyze")
async def analyze_document(
    image: UploadFile = File(...),
    language: str = Form("en"),
):
    image_bytes = await image.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    lang_name = LANGUAGES.get(language, "English")
    user_prompt = f"Please analyze this medical document and explain it in {lang_name}. Be thorough and clear."

    async def stream_response():
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": GEMMA_MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {
                            "role": "user",
                            "content": user_prompt,
                            "images": [image_b64],
                        },
                    ],
                    "stream": True,
                },
            ) as response:
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            data = json.loads(line)
                            token = data.get("message", {}).get("content", "")
                            if token:
                                yield f"data: {json.dumps({'token': token})}\n\n"
                            if data.get("done"):
                                yield f"data: {json.dumps({'done': True})}\n\n"
                        except json.JSONDecodeError:
                            continue

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
