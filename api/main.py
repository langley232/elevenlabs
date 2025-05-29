from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from elevenlabs import generate, set_api_key
from elevenlabs.api import Voices
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import tempfile
import shutil
import io

# Load environment variables
load_dotenv()

# Set ElevenLabs API key
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

app = FastAPI(title="TTS/STT API Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TTSRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Default voice ID (Rachel)


@app.get("/")
async def root():
    return {"message": "Welcome to TTS/STT API Service"}


@app.get("/voices")
async def get_voices():
    try:
        voices = Voices.from_api()
        return {"voices": [{"id": voice.voice_id, "name": voice.name} for voice in voices]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    try:
        # Generate audio
        audio = generate(
            text=request.text,
            voice=request.voice_id,
            model="eleven_monolingual_v1"
        )

        # Create a streaming response with the audio data
        return StreamingResponse(
            io.BytesIO(audio),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f'attachment; filename="tts_output.mp3"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stt")
async def speech_to_text(audio_file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            shutil.copyfileobj(audio_file.file, temp_file)
            temp_file_path = temp_file.name

        # Note: ElevenLabs currently doesn't have a direct STT API
        # You might want to use other services like Whisper API or Google Speech-to-Text
        # For now, we'll return a placeholder response
        return {"message": "STT functionality will be implemented soon"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
