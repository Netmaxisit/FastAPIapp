from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

app = FastAPI()

class VideoURL(BaseModel):
    url: str

def extract_video_id(url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    from urllib.parse import urlparse, parse_qs

    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        if 'v' in parse_qs(parsed_url.query):
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path:
            path_parts = parsed_url.path.split('/')
            if len(path_parts) > 1:
                return path_parts[1]
    return ""

@app.post("/transcript/")
async def get_transcript(video_url: VideoURL):
    video_id = extract_video_id(video_url.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = JSONFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        return {"transcript": formatted_transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

