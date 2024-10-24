from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World APi"}
    
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, adjust as needed
    allow_headers=["*"],  # Allows all headers, adjust as needed
)

@app.get("/transcript/")
async def get_transcript(url: str = Query(..., description="YouTube video URL")):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    try:
        # First, attempt to get the regular transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        # If regular transcript is not available, try fetching auto-generated transcript
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except Exception as inner_e:
            raise HTTPException(status_code=500, detail=f"Could not retrieve transcript: {str(inner_e)}")
    
    return {"transcript": transcript}
