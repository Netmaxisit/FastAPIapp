from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import asyncpg

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

async def connect_to_database():
    connection_uri = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    return await asyncpg.connect(dsn=connection_uri)


@app.on_event("startup")
async def startup_event():
    app.state.db = await connect_to_database()
    print("Connected to PostgreSQL database!")


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.db.close()

@app.get("/")
async def read_root():
    try:
        await app.startup() 
        # Your actual route logic here
        return {"Hello": "World!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
