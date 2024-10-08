from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
    
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

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
async def get_transcript(url: str = Query(..., description="YouTube video URL")):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = JSONFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        return {"transcript": formatted_transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
