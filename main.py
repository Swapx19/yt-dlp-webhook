from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import subprocess
import uuid
import os

app = FastAPI()

@app.post("/download")
async def download_video(req: Request):
    data = await req.json()
    video_url = data.get("videoUrl")
    filename = f"{uuid.uuid4()}.mp4"

    try:
        subprocess.run(["yt-dlp", "-f", "best[ext=mp4]", "-o", filename, video_url], check=True)
        return FileResponse(filename, media_type="video/mp4", filename=filename)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(filename):
            os.remove(filename)
