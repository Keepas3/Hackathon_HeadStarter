

from sentence_transformers import SentenceTransformer
import openai
import requests
import json
import numpy as np

openrouter_api_key = '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'

# Load a Hugging Face model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Specify the model name you want to use

def get_embedding(sentence):
    return model.encode(sentence)

def get_cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# Function to split the text into paragraphs
def split_into_paragraphs(text):
    paragraphs = text.split('\n\n')
    # Filter out any empty paragraphs or ones that are too short to be meaningful
    return [para for para in paragraphs if len(para) > 40]



model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  # Specify the model name you want to use

prompt = """Based on the context below. Given you are writing for a interviewer for a job position, write a useful concise and short key points in your own words

CONTEXT:
"""

# prompt: iterate through my audio.txt file and append it to the prompt string

with open('Hackathon/Audio1.txt', 'r') as f:
  for line in f:
    prompt += line + "\n"


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

llm_response = response.json().get("choices")[0].get('message').get("content")
print(llm_response)
