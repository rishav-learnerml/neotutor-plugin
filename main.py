# main.py
import os
from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

# your imports (keep paths as in your project)
from src.rag.rag import RAG
from src.utils.get_polished_answer import get_polished_answer
from src.utils.transcript_generator_yt import generate_transcript_from_videoID, TranscriptsDisabled  # adapt if your util raises different errors

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("neotutor")

app = FastAPI()

# CORS - during dev allow all; in prod restrict origins
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    # add your frontend domain(s)
    # "https://your-frontend.example",
    # chrome extension origin if you lock down:
    # "chrome-extension://cplncdddlpnnlgebeadfjnjbnmmcmedj"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during dev. Set to `origins` in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health():
    return {"status": "ok"}

class VideoProcessRequest(BaseModel):
    video_id: str
    transcript: Optional[str] = None  # client-supplied transcript (preferred)

class QueryRequest(BaseModel):
    video_id: str
    query: str

# In-memory store for demo; replace with persistent store in prod.
vector_stores = {}

# Environment toggle:
# If ALLOW_SERVER_FETCH is set to "true" (case-insensitive), the server will
# attempt to fetch transcript itself as a fallback. Default = False on Render.
ALLOW_SERVER_FETCH = os.environ.get("ALLOW_SERVER_FETCH", "false").lower() == "true"

@app.post("/process_video")
def process_video(req: VideoProcessRequest, request: Request):
    """
    Process a video: prefer client-supplied transcript; if none supplied:
      - if ALLOW_SERVER_FETCH=True -> attempt to generate transcript server-side (may be blocked)
      - otherwise return 400 instructing client to supply transcript or choose alternate flow
    """
    logger.info("process_video called for video_id=%s (client supplied transcript=%s)", req.video_id, "yes" if req.transcript else "no")

    transcript = req.transcript

    if transcript is None:
        if not ALLOW_SERVER_FETCH:
            # Fail fast when server-side fetching is disabled (safe default on Render)
            # Client should supply transcript from browser or upload audio for ASR.
            raise HTTPException(
                status_code=400,
                detail=(
                    "No transcript provided. Server-side transcript fetching is disabled on this deployment "
                    "to avoid IP-based blocking by YouTube. Please extract captions in-browser and send them "
                    "in the request (`transcript` field), or enable server fetching by setting ALLOW_SERVER_FETCH=true (not recommended on Render)."
                )
            )
        # ALLOW_SERVER_FETCH == True -> attempt fallback
        try:
            transcript = generate_transcript_from_videoID(req.video_id)
        except Exception as e:
            # Be specific for youtube_transcript_api RequestBlocked
            # The youtube_transcript_api raises youtube_transcript_api._errors.RequestBlocked in many cases.
            logger.exception("Server-side transcript generation failed for %s: %s", req.video_id, e)
            # Return an informative 502/503 to the client
            raise HTTPException(
                status_code=502,
                detail=(
                    "Server-side transcript generation failed. YouTube may be blocking requests from this host. "
                    "Error: " + str(e)
                )
            )

    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not available for this video.")

    # Indexing (this might be CPU / time consuming; consider making async/job queue in production)
    try:
        rag = RAG(transcript)
        rag.index_documents()
        vector_stores[req.video_id] = rag.vector_store
        logger.info("Indexed video %s successfully", req.video_id)
    except Exception as e:
        logger.exception("Indexing failed for %s: %s", req.video_id, e)
        raise HTTPException(status_code=500, detail="Indexing failed: " + str(e))

    return {"message": "Transcript indexed and vector embeddings generated.", "video_id": req.video_id}

@app.post("/process_query")
def process_query(req: QueryRequest):
    if req.video_id not in vector_stores:
        raise HTTPException(status_code=404, detail="Transcript not indexed for this video. Please process the video first.")
    try:
        answer = get_polished_answer(vector_stores[req.video_id], req.query)
    except Exception as e:
        logger.exception("Error generating polished answer: %s", e)
        raise HTTPException(status_code=500, detail="Error generating answer: " + str(e))

    if answer is None:
        raise HTTPException(status_code=400, detail="Could not generate answer. Ensure transcript is indexed.")
    return {"answer": answer}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info("Starting server on port %d (ALLOW_SERVER_FETCH=%s)", port, ALLOW_SERVER_FETCH)
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
