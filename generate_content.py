import os
import sys
import argparse
from datetime import datetime
import openai
from pathlib import Path

def read_transcript(file_path):
    """Read transcript file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def analyze_and_generate(transcripts, api_key, word_limit):
    """Use GPT to analyze transcripts and generate fresh content."""
    openai.api_key = api_key
    
    # Calculate output token limit (assuming average word length of 2 tokens)
    output_tokens = word_limit * 2
    
    # Prepare the prompt
    prompt = f"""You are an expert content creator. Analyze the following video transcripts and create a fresh, engaging narrative that captures the essence of the content. 
    The new content should:
    1. Maintain the key information and insights
    2. Be well-structured and coherent
    3. Have a natural, conversational tone
    4. Include relevant details and examples
    5. Be engaging and easy to follow
    6. Be approximately {word_limit} words in length

    Original Transcripts:
    """
    
    # Add each transcript to the prompt
    for i, transcript in enumerate(transcripts, 1):
        prompt += f"\nTranscript {i}:\n{transcript}\n"
    
    prompt += f"\nPlease generate a fresh narrative based on these transcripts. The output should be approximately {word_limit} words:"
    
    try:
        # Call OpenAI API with cost-effective model
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are an expert content creator who excels at synthesizing information and creating engaging narratives. Keep your response to approximately {word_limit} words."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=output_tokens  # Only limit output tokens
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        if "model" in str(e).lower():
            print("\nTrying fallback model...")
            try:
                # Fallback to gpt-3.5-turbo if gpt-4o-mini is not available
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are an expert content creator who excels at synthesizing information and creating engaging narratives. Keep your response to approximately {word_limit} words."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=output_tokens  # Only limit output tokens
                )
                return response.choices[0].message.content
            except Exception as e2:
                print(f"Fallback model also failed: {str(e2)}")
                return None
        return None

def process_transcripts(input_dir, api_key, word_limit):
    """Process all transcripts in the input directory and generate new content."""
    # Create merged-gen-output directory inside the input directory
    output_dir = os.path.join(input_dir, "merged-gen-output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all transcript files
    transcript_files = sorted(Path(input_dir).glob("transcript_*.txt"))
    
    if not transcript_files:
        print("No transcript files found in the input directory.")
        return
    
    # Read all transcripts
    transcripts = []
    for file in transcript_files:
        try:
            content = read_transcript(file)
            transcripts.append(content)
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
    
    if not transcripts:
        print("No valid transcripts found.")
        return
    
    # Generate new content
    print("\nAnalyzing transcripts and generating fresh content...")
    new_content = analyze_and_generate(transcripts, api_key, word_limit)
    
    if new_content:
        # Save the generated content
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"generated_content_{timestamp}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Generated Content\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Word limit: {word_limit}\n\n")
            f.write(new_content)
            
            # Add word count information
            word_count = len(new_content.split())
            f.write(f"\n\nWord count: {word_count}")
        
        print(f"\n✓ Generated content saved to: {output_file}")
        print(f"Word count: {word_count}")
    else:
        print("\n✗ Failed to generate content.")

def main():
    parser = argparse.ArgumentParser(description='Generate fresh content from YouTube video transcripts')
    parser.add_argument('input_dir', help='Directory containing transcript files')
    parser.add_argument('--api-key', help='OpenAI API key', required=True)
    parser.add_argument('--word-limit', type=int, default=500, help='Approximate word limit for generated content (default: 500)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        sys.exit(1)
    
    if args.word_limit < 100:
        print("Error: Word limit must be at least 100 words.")
        sys.exit(1)
    elif args.word_limit > 2000:
        print("Warning: Large word limits may result in higher API costs.")
    
    process_transcripts(args.input_dir, args.api_key, args.word_limit)

if __name__ == "__main__":
    main() 