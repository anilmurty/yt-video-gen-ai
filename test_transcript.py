from youtube_transcript_api import YouTubeTranscriptApi

def test_transcript():
    # Using a short video that we know has captions
    video_id = "jNQXAC9IVRw"  # "Me at the zoo" - first YouTube video ever
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print("Success! Transcript retrieved:")
        print(transcript)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_transcript() 