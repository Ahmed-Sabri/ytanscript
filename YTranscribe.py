import yt_dlp
import whisper
import os
import torch
import re
import time

# Force CPU usage
torch.cuda.is_available = lambda : False

def download_audio(url, output_file):
    print(f"Downloading audio from {url}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_file,
        'keepvideo': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    if not os.path.exists(output_file):
        if os.path.exists(f"{output_file}.mp3"):
            print(f"Renaming {output_file}.mp3 to {output_file}")
            os.rename(f"{output_file}.mp3", output_file)
    
    print(f"Audio downloaded: {os.path.exists(output_file)}")

def transcribe_audio(audio_file, output_file, language='en'):
    print(f"Starting transcription of {audio_file}")
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    
    print("Loading Whisper model...")
    model = whisper.load_model("large")
    
    print("Transcribing audio...")
    start_time = time.time()
    result = model.transcribe(audio_file, language=language, verbose=True)
    end_time = time.time()
    print(f"Transcription completed in {end_time - start_time:.2f} seconds")
    
    print("Writing output...")
    with open(output_file, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(result["segments"], start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = clean_text(segment["text"])
            srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    
    print(f"Subtitles saved to {output_file}")

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = '. '.join(sentence.capitalize() for sentence in text.split('. '))
    return text.strip()

def main():
    video_url = input("Enter the YouTube video URL: ")
    language = input("Enter the language code (e.g., 'en' for English, 'fr' for French): ")
    audio_file = "temp_audio.mp3"
    subtitle_file = "output_subtitle.srt"

    try:
        print("Starting download process...")
        download_audio(video_url, audio_file)

        if not os.path.exists(audio_file):
            print(f"Error: Audio file {audio_file} not found after download.")
            print("Current directory contents:")
            print(os.listdir())
            return

        print("Starting transcription process...")
        transcribe_audio(audio_file, subtitle_file, language)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if os.path.exists(audio_file):
            print(f"Removing temporary audio file: {audio_file}")
            os.remove(audio_file)

if __name__ == "__main__":
    main()
