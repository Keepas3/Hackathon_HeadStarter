With this project, this can help students understand better by reading the text so that they can get a better understanding of the video.
This can apply to interview questions to programming tutorials. These texts can be a summary of how you should tackle them. 

Built With:
Python
Visual Studio Code
HTML
CSS

Imported:
In transcription.py -
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from textblob import TextBlob
In chatbot.py
from sentence_transformers import SentenceTransformer
import openai
import requests
import json
import numpy as np

Purpose:
Audio1.txt is an example of a transcript taken by captions from a youtube video. https://www.youtube.com/watch?v=clMJ8BwCGa0

Transcription.py uses transcription with importation of pytube from youtube. As well as importing YouTubeTranscriptApi and textBlob. 
Pytube give access to youtube videos and lets you retrieve basic information about the video content.
YoutubeTranscriptApi allows access to using youtube's captions or transcripts and allows the code to read it.
textBlob is an api that processes the String data and allows the AI to analyze it.

def seconds_to_minutes_seconds(seconds): is a method that converts the timestamps from minutes to seconds from the transcript.
def transcribe_and_save(video_url, output_file): is a method that takes in the parameters of a video_url and gets the video's transcript to be sent to a file of the user's choosing.
First, the code chunks the transcript into timestamps for dialogue in the video. Then, writes the transcript with the timestamps to the file.


Chatbot.py reads the textfile from the user's input and summarizes the transcript into key points. 
How it works is by using API connected to a natural language model
