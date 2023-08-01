from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


app = FastAPI()


def get_youtube_data(video_url):
    try:
        yt = YouTube(video_url)
        video_title = yt.title
       
        video_transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)
        #text_transcript = "\n".join([item['text'] for item in video_transcript])
        text_transcript = " ".join([item['text'] for item in video_transcript])
        return video_title, text_transcript
    except Exception as e:
        raise HTTPException(status_code=404, detail="Invalid YouTube video URL or transcript unavailable")

@app.get("/extract/")
async def extract_youtube_data(video_url: str):
    video_title, text_transcript = get_youtube_data(video_url)
    return {
        "video_title": video_title,
        "text_transcript": text_transcript
    }



@app.get("/")
def read_root():
    return {"Hello": "World!"}
