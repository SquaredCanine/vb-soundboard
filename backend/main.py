from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

AUDIO_ROOT = Path(__file__).parent / "audio"
CATEGORIES = ["songs", "bits"]

app = FastAPI(title="VB Soundboard API", version="1.0.0")


class AudioFile(BaseModel):
    id: str
    name: str
    url: str


class AudioLibrary(BaseModel):
    songs: list[AudioFile]
    bits: list[AudioFile]


def find_mp3_files(category: str) -> list[Path]:
    folder = AUDIO_ROOT / category
    if not folder.is_dir():
        return []
    return sorted(folder.glob("*.mp3"))


def make_id(category: str, file: Path) -> str:
    return f"{category}-{file.stem}"


def to_audio_file(category: str, file: Path) -> AudioFile:
    audio_id = make_id(category, file)
    return AudioFile(id=audio_id, name=file.stem, url=f"/audio/{audio_id}")


@app.get("/audio", response_model=AudioLibrary, operation_id="listAudio")
def list_audio():
    return AudioLibrary(
        songs=[to_audio_file("songs", file) for file in find_mp3_files("songs")],
        bits=[to_audio_file("bits", file) for file in find_mp3_files("bits")],
    )


@app.get(
    "/audio/{id}",
    operation_id="getAudioFile",
    response_class=FileResponse,
    responses={200: {"content": {"audio/mpeg": {}}}, 404: {"description": "Audio file not found"}},
)
def get_audio_file(id: str):
    # Only files found by scanning the folders can be returned, so the id can't point outside AUDIO_ROOT
    for category in CATEGORIES:
        for file in find_mp3_files(category):
            if make_id(category, file) == id:
                return FileResponse(file, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio file not found")
