# main.py
import os
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# your imports (keep paths as in your project)
from src.rag.rag import RAG
from src.utils.get_polished_answer import get_polished_answer
from src.utils.transcript_generator_yt import generate_transcript_from_videoID

app = FastAPI()

# CORS - during dev allow all; in production restrict
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # Add your deployed frontend(s)
    # "https://your.api.domain",
    # Optionally the chrome extension origin to lock down:
    # "chrome-extension://cplncdddlpnnlgebeadfjnjbnmmcmedj"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- during dev. For prod use allow_origins=origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health():
    return {"status": "ok"}

class VideoProcessRequest(BaseModel):
    video_id: str
    transcript: Optional[str] = None  # client-supplied transcript (optional)

class QueryRequest(BaseModel):
    video_id: str
    query: str

# In-memory store for demo; replace with persistent store in prod.
vector_stores = {}

@app.post("/process_video")
def process_video(req: VideoProcessRequest):
    # Use client-side transcript if supplied (preferred)
    transcript = req.transcript
    if transcript is None:
        # server-side fallback (may be blocked on some hosts like Render)
        transcript = generate_transcript_from_videoID(req.video_id)

    if transcript is None:
        raise HTTPException(status_code=404, detail="Transcript not available for this video.")

    # Build RAG and index (your existing logic)
    rag = RAG(transcript)
    rag.index_documents()
    vector_stores[req.video_id] = rag.vector_store

    return {"message": "Transcript indexed and vector embeddings generated.", "video_id": req.video_id}

@app.post("/process_query")
def process_query(req: QueryRequest):
    if req.video_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Transcript not indexed for this video. Please process the video first.")
    answer = get_polished_answer(vector_stores[req.video_id], req.query)
    if answer is None:
        raise HTTPException(status_code=400, detail="Could not generate answer. Ensure transcript is indexed.")
    return {"answer": answer}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Do not use reload=True in production
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
