import os
import sys
import argparse
from pathlib import Path
import openai
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import requests
from PIL import Image
import io
import re
import time
from elevenlabs import generate, save, set_api_key, voices
import numpy as np

def list_available_voices(elevenlabs_api_key):
    """List all available ElevenLabs voices."""
    try:
        set_api_key(elevenlabs_api_key)
        all_voices = voices()
        print("\nAvailable voices:")
        for voice in all_voices:
            print(f"- {voice.name}: {voice.voice_id}")
    except Exception as e:
        print(f"Error fetching voices: {str(e)}")

def split_into_segments(content, max_words=50):
    """Split content into segments for image generation."""
    sentences = re.split(r'[.!?]+', content)
    segments = []
    current_segment = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        words = sentence.split()
        if current_word_count + len(words) > max_words and current_segment:
            segments.append(' '.join(current_segment) + '.')
            current_segment = []
            current_word_count = 0
            
        current_segment.append(sentence)
        current_word_count += len(words)
    
    if current_segment:
        segments.append(' '.join(current_segment) + '.')
    
    return segments

def generate_image(prompt, api_key):
    """Generate an image using DALL-E."""
    try:
        openai.api_key = api_key
        response = openai.Image.create(
            prompt=f"Create a high-quality, engaging image that represents: {prompt}",
            n=1,
            size="1024x1024"
        )
        
        # Download the image
        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
        return image
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def generate_audio(text, elevenlabs_api_key, voice_id):
    """Generate audio using ElevenLabs API."""
    try:
        set_api_key(elevenlabs_api_key)
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        return audio
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return None

def create_video(content, openai_api_key, elevenlabs_api_key, voice_id, output_dir):
    """Create a video from the content with AI narration and images."""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Split content into segments
    segments = split_into_segments(content)
    
    # Generate audio for the entire content
    print("\nGenerating audio narration...")
    audio_data = generate_audio(content, elevenlabs_api_key, voice_id)
    if audio_data:
        audio_path = os.path.join(output_dir, "narration.mp3")
        save(audio_data, audio_path)
        print("✓ Audio generated successfully")
    else:
        print("✗ Failed to generate audio")
        return
    
    # Generate images for each segment
    print("\nGenerating images for each segment...")
    images = []
    for i, segment in enumerate(segments, 1):
        print(f"Generating image {i}/{len(segments)}...")
        image = generate_image(segment, openai_api_key)
        if image:
            image_path = os.path.join(output_dir, f"image_{i:03d}.png")
            image.save(image_path)
            images.append(image_path)
            print(f"✓ Image {i} generated successfully")
        else:
            print(f"✗ Failed to generate image {i}")
        # Add delay to avoid rate limits
        time.sleep(2)
    
    if not images:
        print("No images were generated successfully.")
        return
    
    # Create video
    print("\nCreating video...")
    try:
        # Load audio
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        
        # Calculate duration for each image
        image_duration = duration / len(images)
        
        # Create video clips from images
        video_clips = []
        for img_path in images:
            clip = ImageClip(img_path).set_duration(image_duration)
            video_clips.append(clip)
        
        # Concatenate clips and add audio
        final_clip = concatenate_videoclips(video_clips)
        final_clip = final_clip.set_audio(audio_clip)
        
        # Write video file
        output_path = os.path.join(output_dir, "final_video.mp4")
        final_clip.write_videofile(output_path, fps=24)
        
        print(f"\n✓ Video created successfully: {output_path}")
        
        # Clean up
        final_clip.close()
        audio_clip.close()
        
    except Exception as e:
        print(f"Error creating video: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Create video with AI narration and images')
    
    # Only require content_file and API keys if not listing voices
    if '--list-voices' not in sys.argv:
        parser.add_argument('content_file', help='Path to the generated content file')
        parser.add_argument('--openai-key', required=True, help='OpenAI API key')
    
    parser.add_argument('--elevenlabs-key', required=True, help='ElevenLabs API key')
    parser.add_argument('--voice-id', help='ElevenLabs voice ID (run with --list-voices to see available voices)')
    parser.add_argument('--list-voices', action='store_true', help='List available ElevenLabs voices')
    
    args = parser.parse_args()
    
    # If --list-voices is specified, show available voices and exit
    if args.list_voices:
        list_available_voices(args.elevenlabs_key)
        sys.exit(0)
    
    # Read content file
    try:
        with open(args.content_file, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading content file: {str(e)}")
        sys.exit(1)
    
    # Set default voice ID if not provided
    voice_id = args.voice_id if args.voice_id else "21m00Tcm4TlvDq8ikWAM"  # Default to "Rachel"
    
    # Create video_output directory in the same folder as the content file
    content_path = Path(args.content_file)
    output_dir = content_path.parent / "video_output"
    
    create_video(content, args.openai_key, args.elevenlabs_key, voice_id, output_dir)

if __name__ == "__main__":
    main() 