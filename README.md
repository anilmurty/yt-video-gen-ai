# YouTube Video Generator

A tool that processes YouTube videos by transcribing content, generating fresh narratives using AI, and creating new videos with AI-generated narration and visuals.

## Features

1. **Video Transcription**
   - Download and transcribe YouTube videos
   - Handle multiple videos (up to 5) simultaneously
   - Save transcripts in timestamped folders
   - Generate summary reports

2. **Content Generation**
   - Analyze transcripts using GPT models
   - Generate fresh, engaging narratives
   - Maintain key information while creating unique content
   - Configurable word limit for output

3. **Video Creation**
   - Generate AI narration using ElevenLabs voices
   - Create relevant images using DALL-E
   - Combine audio and images into a cohesive video
   - Support for custom voice selection

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd yt-video-gen
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Transcribe Videos
```bash
python transcribe_videos.py "video_url1" "video_url2" "video_url3"
```
- Supports up to 5 YouTube video URLs
- Creates a timestamped folder with transcripts

### 2. Generate Fresh Content
```bash
python generate_content.py "transcriptions_YYYYMMDD_HHMMSS" --api-key "your-openai-api-key" --word-limit 500
```
- Analyzes transcripts and generates new content
- Optional word limit parameter (default: 500)
- Saves output in merged-gen-output directory

### 3. Create Video
First, list available voices:
```bash
python create_video.py --elevenlabs-key "your-elevenlabs-key" --list-voices
```

Then create the video:
```bash
python create_video.py "path/to/generated_content.txt" --openai-key "your-openai-key" --elevenlabs-key "your-elevenlabs-key" --voice-id "chosen-voice-id"
```

Options:
- `--voice-id`: Choose a specific ElevenLabs voice (optional)
- Output is saved in video_output directory within the content folder

## Requirements

- Python 3.8+
- OpenAI API key (for content generation and image creation)
- ElevenLabs API key (for voice generation)
- YouTube Data API access
- Internet connection for API calls

## Project Structure

```
yt-video-gen/
├── transcribe_videos.py    # Video transcription script
├── generate_content.py     # Content generation script
├── create_video.py        # Video creation script
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Output Structure

```
transcriptions_YYYYMMDD_HHMMSS/
├── transcript_1.txt
├── transcript_2.txt
├── summary.txt
└── merged-gen-output/
    ├── generated_content_YYYYMMDD_HHMMSS.txt
    └── video_output/
        ├── narration.mp3
        ├── image_001.png
        ├── image_002.png
        └── final_video.mp4
```

## Notes

- API keys should be kept secure and not committed to version control
- Large word limits may result in higher API costs
- Generated videos are saved with transcripts for easy reference
- Image generation includes rate limiting to avoid API restrictions

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[Your chosen license] 