import requests

def generate_transcript_from_videoID(video_id: str, lang: str = "en") -> str | None:
    """
    Fetch YouTube transcript using tactiq-apps API via requests.
    Returns transcript as plain text or None if not available.
    """
    url = "https://tactiq-apps-prod.tactiq.io/transcript"
    payload = {
        "videoUrl": f"https://www.youtube.com/watch?v={video_id}",
        "langCode": lang,
    }

    try:
        res = requests.post(url, json=payload, timeout=15)
        res.raise_for_status()
        data = res.json()

        if "captions" not in data or not data["captions"]:
            print("No captions found in response.")
            return None

        transcript = " ".join(c["text"] for c in data["captions"] if c["text"] and c["text"] != "No text")

        if transcript.strip():
            return transcript
        else:
            print("Transcript exists but is empty.")
            return None

    except requests.RequestException as e:
        print("Transcript fetch error:", e)
        return None
