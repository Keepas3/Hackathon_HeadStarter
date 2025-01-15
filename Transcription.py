from pytubefix import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from textblob import TextBlob
import os
from datetime import datetime
#from gensim.summarization import summarize
"""import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize"""


def seconds_to_minutes_seconds(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def transcribe_and_save(video_url):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        project_directory = os.path.dirname(os.path.abspath(__file__)) 
        output_file = os.path.join(project_directory, f"Audio_{timestamp}.txt")
        # Get YouTube video

        print("Starting transcription process...")
        yt = YouTube(video_url)
        print(f"Fetched video: {yt.title}")
        # Get transcript
        transcripts = YouTubeTranscriptApi.get_transcript(yt.video_id)
        print("Transcript fetched successfully. Total transcripts: ", len(transcripts))        # Chunk transcript into timeframes

        timeframes = []
        for transcript in transcripts:
            start_time = transcript['start']
            duration = transcript['duration']
            end_time = start_time + duration
            text = transcript['text']
            timeframes.append((start_time, end_time, text))
            print(f"Added transcript chunk: {text[:30]}...") # Print the first 30 characters of each chunk
        # Write timeframes to file
        with open(output_file, 'w', encoding='utf-8') as file:
            for start_time, end_time, text in timeframes:
                start_time_formatted = seconds_to_minutes_seconds(start_time)
                end_time_formatted = seconds_to_minutes_seconds(end_time)
                file.write(f"{start_time_formatted} - {end_time_formatted}: {text}\n")
                print(f"Written to file: {start_time_formatted} - {end_time_formatted}: {text[:30]}...") # Debug written text

        print("Timeframes saved to:", output_file)

    except Exception as e:
        print("Error:", str(e))





"""def summarize_text(text):
    # Read text from file
    with open(text, "r", encoding="utf-8") as file:
        text_content = file.read()
    
    # Tokenize the text into sentences
    sentences = sent_tokenize(text_content)
    
    # Tokenize the sentences into words
    words = word_tokenize(text_content)
    
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Calculate word frequency
    word_freq = FreqDist(filtered_words)
    
    # Get the most common words
    most_common_words = [word for word, _ in word_freq.most_common(10)]  # You can adjust the number of words
    
    # Get the sentences containing the most common words
    summary_sentences = []
    for sentence in sentences:
        if any(word in sentence for word in most_common_words):
            summary_sentences.append(sentence)
    
    # Combine the summary sentences into a single string
    summary = ' '.join(summary_sentences)
    
    return summary

summary = summarize_text("C:\\Users\\fungb\\Notepad++\\Audio.txt")

# Print the summary
print(summary)"""
        
# Example usage
video_url = "https://www.youtube.com/watch?v=clMJ8BwCGa0"
transcribe_and_save(video_url)
#summarize_text(inputfile2, outputfile2)

