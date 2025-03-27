# YouTube Video Transcriber

This script fetches transcripts from YouTube videos using the YouTube Transcript API.

## Prerequisites

- Python 3.8 or higher

## Installation

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with up to 3 YouTube URLs as arguments:

```bash
python transcribe_videos.py "https://youtube.com/watch?v=VIDEO1" "https://youtube.com/watch?v=VIDEO2" "https://youtube.com/watch?v=VIDEO3"
```

The script will:
1. Create a timestamped folder (e.g., `transcriptions_20240315_143022`)
2. Fetch transcripts directly from YouTube
3. Save transcripts as text files

## Output

For each video, you'll get:
- `transcript_1.txt`
- `transcript_2.txt`
- `transcript_3.txt`

Each file contains the transcript from the corresponding video.

## Notes

- This script only works for videos that have captions available on YouTube
- If a video doesn't have captions, it will be skipped with an error message
- The script supports both standard YouTube URLs (youtube.com) and shortened URLs (youtu.be) 