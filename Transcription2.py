import os
from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
import requests
import json
import numpy as np
from datetime import datetime

openrouter_api_key = os.getenv('openrouter_api_key')

# Load a Hugging Face model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
#model = "openai/gpt-3.5-turbo"

def seconds_to_minutes_seconds(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"
def transcribe_and_save(video_url):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        project_directory = os.path.dirname(os.path.abspath(__file__)) 
        
        # Get YouTube video
        print("Starting transcription process...")
        yt = YouTube(video_url, use_po_token=True)
        print(f"Fetched video: {yt.title}")

        output_file = os.path.join(project_directory, f"Summary_{yt.title}.txt")
        
        # Get transcript
        transcripts = YouTubeTranscriptApi.get_transcript(yt.video_id, languages=['en'])
        if not transcripts:
            print("Error: No transcripts available for this video.")
            return
        print("Transcript fetched successfully. Total transcripts: ", len(transcripts))        
       # print(transcripts)
        
        # Combine transcript into a single string
        full_transcript = " ".join([transcript['text'] for transcript in transcripts if 'text' in transcript])      
      #  print("Full Transcript:", full_transcript)
        
        # Prepare prompt for the OpenAI API
        prompt = f""" Summarize the transcript

        CONTEXT:
        {full_transcript}
        """
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openrouter_api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-thinking-exp:free",
                "messages": [
                    {"role": "user", 
                    "content": prompt}
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
            print("Response content:", response.content)
        
    except Exception as e:
        print("Error:", str(e))



# Example usage
video_url = input("Enter URL:")
transcribe_and_save(video_url)
print("Transcription process completed.")
