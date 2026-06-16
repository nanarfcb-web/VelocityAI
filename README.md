# QuantumDub Supreme 2026

AI-powered video dubbing platform using FastAPI, Redis, and advanced ML models.

## Features

- **Audio Upload**: Accept WAV files via FastAPI endpoint
- **Speech Recognition**: Whisper for accurate transcription
- **Translation**: NLLB-200 for English to Arabic translation
- **Text-to-Speech**: XTTS v2 for natural Arabic voice synthesis
- **Async Processing**: Redis/RQ for scalable task queue
- **Audio Processing**: PyDub for chunk processing and normalization

## Architecture

- **Web Service**: FastAPI app for receiving upload requests
- **Worker**: Background job processor for dubbing tasks
- **Queue**: Redis-backed RQ for async task management

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

### Start Redis
```bash
redis-server
```

### Start Web Service
```bash
uvicorn app:app --reload
```

### Start Worker
```bash
python worker.py
```

## API Endpoints

### POST /dub
Upload an audio file for dubbing.

**Request**: multipart/form-data with `file` field
**Response**: 
```json
{
  "status": "processing",
  "task_id": "uuid-string"
}
```

## Environment Variables

- `REDIS_URL`: Redis connection string (default: `redis://localhost:6379`)
- `PORT`: Server port (default: 8000)

## Deployment

Use `render.yaml` for deployment on Render.com with web and worker services.
