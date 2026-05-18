# MedLingo — Private Medical Document Understanding

**Understand your medical documents in any language. 100% private. Runs entirely on your device.**

MedLingo uses **Gemma 4** via **Ollama** to read and explain medical documents — prescriptions, lab results, discharge summaries, radiology reports — in clear, simple language across 35+ languages. No data ever leaves your machine.

## The Problem

Over **1 billion people** worldwide receive medical documents in a language they don't fully understand. Immigrants, refugees, travelers, and minority language speakers face a daily reality where a prescription they can't read or a lab result they can't interpret can lead to missed medications, dangerous drug interactions, or unnecessary anxiety.

Existing solutions require uploading sensitive medical data to cloud servers — a non-starter for privacy-conscious patients and a violation of medical data regulations in many jurisdictions.

## The Solution

MedLingo runs **entirely locally** using Gemma 4's multimodal capabilities through Ollama. Users simply:

1. **Photograph** their medical document (or upload an image)
2. **Select** their preferred language from 35+ options
3. **Read** a clear, structured explanation — with flagged abnormal values and plain-language interpretations

No internet connection required. No data uploaded. No accounts needed.

## Key Features

- **Multimodal Document Understanding** — Gemma 4's vision capabilities read prescriptions, lab panels, discharge notes, and radiology reports
- **35+ Languages** — Leverages Gemma 4's native multilingual training (140+ languages) for accurate, culturally-aware translations
- **Privacy-First Architecture** — All processing happens locally via Ollama. Zero network requests for inference
- **Abnormal Value Flagging** — Automatically identifies out-of-range lab values and explains their significance
- **Mobile-Friendly** — Camera capture support for on-the-go use; responsive design works on any device
- **Streaming Responses** — Real-time token streaming so users see results as they're generated

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Browser    │────▶│   FastAPI    │────▶│    Ollama    │
│  (Frontend)  │◀────│  (Backend)   │◀────│  (Gemma 4)   │
└──────────────┘     └──────────────┘     └──────────────┘
     Upload            Base64 encode        Vision +
     + Language        + SSE stream         Multilingual
                                            Generation
```

All components run on `localhost`. The browser sends the image to FastAPI, which forwards it to Ollama's Gemma 4 model with a system prompt optimized for medical document interpretation. Responses stream back via Server-Sent Events for a real-time experience.

## Quick Start

### Prerequisites

- [Ollama](https://ollama.com) installed
- Python 3.10+

### Setup

```bash
# 1. Pull Gemma 4 model
ollama pull gemma4:e4b

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run MedLingo
python app.py
```

Then open **http://localhost:8000** in your browser.

### Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `GEMMA_MODEL` | `gemma4:e4b` | Model to use (try `gemma4:e2b` for faster inference) |

## Model Sizes

MedLingo works with any Gemma 4 variant available through Ollama:

| Model | VRAM Required | Best For |
|---|---|---|
| `gemma4:e2b` | ~7 GB | Quick results, limited hardware |
| `gemma4:e4b` | ~10 GB | Balanced quality and speed |
| `gemma4:26b` | ~18 GB | Highest quality analysis |

## Tech Stack

- **Model**: Gemma 4 (via Ollama)
- **Backend**: Python, FastAPI, httpx
- **Frontend**: Vanilla HTML/CSS/JS (zero build step)
- **Streaming**: Server-Sent Events (SSE)

## Hackathon

Built for the [Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon) on Kaggle.

**Tracks**: Health & Sciences · Digital Equity & Inclusivity · Ollama Special Technology

## License

Apache 2.0
