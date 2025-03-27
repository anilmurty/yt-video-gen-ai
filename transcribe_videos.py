import os
import sys
import argparse
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    if 'youtu.be' in url:
        return url.split('/')[-1]
    elif 'youtube.com' in url:
        return url.split('v=')[1].split('&')[0]
    return url

def process_videos(urls):
    """Process multiple videos and create transcriptions."""
    # Create timestamped folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"transcriptions_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize formatter for plain text output
    formatter = TextFormatter()
    
    # Create a summary file
    summary_file = os.path.join(output_dir, "summary.txt")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Transcription Summary - {timestamp}\n")
        f.write("=" * 50 + "\n\n")
    
    for i, url in enumerate(urls, 1):
        print(f"\nProcessing video {i}/{len(urls)}")
        print(f"URL: {url}")
        
        try:
            # Get video ID and fetch transcript
            video_id = get_video_id(url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format transcript as plain text
            formatted_transcript = formatter.format_transcript(transcript)
            
            # Save to file
            transcript_path = os.path.join(output_dir, f"transcript_{i}.txt")
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(formatted_transcript)
                
            print(f"✓ Transcription saved to {transcript_path}")
            
            # Update summary file
            with open(summary_file, 'a', encoding='utf-8') as f:
                f.write(f"Video {i}: {url}\n")
                f.write(f"Status: Success\n")
                f.write(f"Output: transcript_{i}.txt\n")
                f.write("-" * 50 + "\n")
            
        except Exception as e:
            error_msg = str(e)
            print(f"✗ Error processing {url}: {error_msg}")
            
            # Update summary file with error
            with open(summary_file, 'a', encoding='utf-8') as f:
                f.write(f"Video {i}: {url}\n")
                f.write(f"Status: Failed\n")
                f.write(f"Error: {error_msg}\n")
                f.write("-" * 50 + "\n")
            continue
            
    print(f"\nAll transcriptions saved in folder: {output_dir}")
    print(f"Summary file: {summary_file}")

def main():
    parser = argparse.ArgumentParser(description='Get YouTube video transcripts')
    parser.add_argument('urls', nargs='+', help='YouTube video URLs')
    args = parser.parse_args()
    
    if len(args.urls) > 5:
        print("Error: Maximum 5 videos allowed")
        sys.exit(1)
        
    process_videos(args.urls)

if __name__ == "__main__":
    main() 