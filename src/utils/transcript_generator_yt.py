from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def generate_transcript_from_videoID(video_id:str)->str | None:
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id=video_id)

        transcript = " ".join(chunk.text for chunk in transcript_list)

        return transcript
    except TranscriptsDisabled:
        print("No Captions Available for this video...")
        return None


