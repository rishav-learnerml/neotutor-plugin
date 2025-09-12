from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag.rag import RAG
from src.utils.get_polished_answer import get_polished_answer
from src.utils.transcript_generator_yt import generate_transcript_from_videoID
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # include extension pages origin if needed (extensions use chrome-extension://<id>)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during dev allow all; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request for processing a video by video_id
class VideoProcessRequest(BaseModel):
    video_id: str


# Request for querying a video by video_id
class QueryRequest(BaseModel):
    video_id: str
    query: str

# Store vector stores in memory for demo purposes
vector_stores = {}

rag_store=None

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)