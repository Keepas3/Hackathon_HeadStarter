from openai import OpenAI
import os

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('openrouter_api_key')
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
  },
  model="openai/gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Can you list a bunch of AI Summarizers? And tell me if they are apart of open router's models?"
    }
  ]
)
print(completion.choices[0].message.content)