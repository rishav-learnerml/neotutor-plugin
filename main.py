# main.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# your imports (keep paths as in your project)
from src.rag.rag import RAG
from src.utils.get_polished_answer import get_polished_answer
from src.utils.transcript_generator_yt import generate_transcript_from_videoID

app = FastAPI()

# CORS - during dev you can allow all; in prod restrict origins including your chrome-extension://... id
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # add your deployed frontend domain(s)
    # "https://yourdomain.com",
    # chrome extension origin (optional, for locked-down config):
    # "chrome-extension://cplncdddlpnnlgebeadfjnjbnmmcmedj"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set to `origins` in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# simple health check for Render
@app.get("/healthz")
def health():
    return {"status": "ok"}

# Request for processing a video by video_id
class VideoProcessRequest(BaseModel):
    video_id: str

# Request for querying a video by video_id
class QueryRequest(BaseModel):
    video_id: str
    query: str

# Store vector stores in memory for demo purposes
vector_stores = {}

@app.post("/process_video")
def process_video(req: VideoProcessRequest):
    transcript = generate_transcript_from_videoID(req.video_id)
    if transcript is None:
        raise HTTPException(status_code=404, detail="Transcript not available for this video.")
    rag = RAG(transcript)
    rag.index_documents()
    # Store the vector store in memory using video_id as key
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
    # Read port from environment (Render supplies PORT)
    port = int(os.environ.get("PORT", 8000))
    # host must be 0.0.0.0 for external access
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
