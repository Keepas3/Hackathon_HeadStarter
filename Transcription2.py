import os
from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from textblob import TextBlob
from sentence_transformers import SentenceTransformer
import openai
import requests
import json
import numpy as np
from datetime import datetime

openrouter_api_key = os.getenv('openrouter_api_key')

# Load a Hugging Face model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def seconds_to_minutes_seconds(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def transcribe_and_save(video_url):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        project_directory = os.path.dirname(os.path.abspath(__file__)) 
        output_file = os.path.join(project_directory, f"Summary_{timestamp}.txt")
        
        # Get YouTube video
        print("Starting transcription process...")
        yt = YouTube(video_url)
        print(f"Fetched video: {yt.title}")
        
        # Get transcript
        transcripts = YouTubeTranscriptApi.get_transcript(yt.video_id)
        print("Transcript fetched successfully. Total transcripts: ", len(transcripts))        
        
        # Combine transcript into a single string
        full_transcript = " ".join([transcript['text'] for transcript in transcripts])
        
        # Prepare prompt for the OpenAI API
        prompt = f"""Based on the context below. Given you are writing for an interviewer for a job position, write useful, concise, and short key points in your own words.

        CONTEXT:
        {full_transcript}
        """

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
            },
            data=json.dumps({
                "model": "google/gemma-7b-it:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            })
        )

        # Ensure the response is valid
        if response.status_code == 200:
            llm_response = response.json().get("choices", [])[0].get('message', {}).get("content", None)
            if llm_response:
                # Write summary to file
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(llm_response)
                    print(f"Summary written to file: {output_file}")
            else:
                print("Error: No content returned from the model.")
        else:
            print(f"Error: Failed to get a valid response from the model. Status code: {response.status_code}")
        
    except Exception as e:
        print("Error:", str(e))

# Example usage
video_url = "https://www.youtube.com/watch?v=clMJ8BwCGa0"
transcribe_and_save(video_url)
print("Transcription process completed.")
