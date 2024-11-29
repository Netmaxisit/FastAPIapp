from fastapi import FastAPI, Query, HTTPException
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the YouTube Subtitle Fetcher API using youtube-transcript-api!"}

@app.get("/fetch_transcript/")
async def fetch_transcript(
    video_url: str = Query(..., description="The URL of the YouTube video."),
    language_code: str = Query("en", description="Language code for subtitles, e.g., 'en'.")
):
    """
    Fetch subtitles (transcripts) from a YouTube video and return as full plain text.
    
    :param video_url: URL of the YouTube video.
    :param language_code: Language code for the subtitles (default 'en').
    :return: Subtitles as a single plain text response.
    """
    try:
        # Extract the video ID from the URL
        video_id = video_url.split("v=")[-1].split("&")[0]

        # Fetch the transcript for the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])

        # Combine all subtitle texts into a single string
        full_text = " ".join([entry["text"] for entry in transcript])

        # Return the full text as plain text
        return PlainTextResponse(content=full_text)

    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="Subtitles are disabled for this video.")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="No subtitles found for the requested language.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
