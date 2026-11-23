from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="VB Soundboard API", version="1.0.0")


class AudioFile(BaseModel):
    id: str
    name: str
    url: str


class AudioLibrary(BaseModel):
    songs: list[AudioFile]
    bits: list[AudioFile]


@app.get("/audio", response_model=AudioLibrary, operation_id="listAudio")
def list_audio():
    return AudioLibrary(songs=[], bits=[])


@app.get(
    "/audio/{id}",
    operation_id="getAudioFile",
    responses={200: {"content": {"audio/mpeg": {}}}, 404: {"description": "Audio file not found"}},
)
def get_audio_file(id: str):
    raise HTTPException(status_code=404, detail="Audio file not found")
