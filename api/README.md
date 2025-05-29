# TTS/STT API Service

A FastAPI-based service that provides Text-to-Speech (TTS) and Speech-to-Text (STT) endpoints using ElevenLabs API.

## Features

- Text-to-Speech conversion using ElevenLabs API
- List available voices
- Speech-to-Text endpoint (placeholder for future implementation)
- Docker support
- CORS enabled for cross-origin requests

## Setup

1. Clone the repository
2. Create a `.env` file with your ElevenLabs API key:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t tts-stt-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env tts-stt-api
   ```

## API Endpoints

### GET /
- Welcome message

### GET /voices
- Returns list of available voices

### POST /tts
- Converts text to speech
- Request body:
  ```json
  {
    "text": "Text to convert",
    "voice_id": "voice_id_here"  // Optional, defaults to Rachel
  }
  ```

### POST /stt
- Converts speech to text (placeholder)
- Accepts audio file upload

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notes

- The STT endpoint is currently a placeholder as ElevenLabs doesn't provide a direct STT API
- Consider using other services like Whisper API or Google Speech-to-Text for STT functionality