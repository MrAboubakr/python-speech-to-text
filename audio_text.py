import os
import speech_recognition as sr
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog

# Add an output folder if it doesn't exist
output_folder = "output_files"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def split_audio(audio_file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_file(audio_file_path)
    chunks = []
    for start_ms in range(0, len(audio), chunk_length_ms):
        chunk = audio[start_ms:start_ms + chunk_length_ms]
        chunk_filename = os.path.join(output_folder, f"chunk_{start_ms // 1000}.wav")
        chunk.export(chunk_filename, format="wav")
        chunks.append(chunk_filename)
    return chunks

def audio_to_text(audio_file_path, lang="en"):
    recognizer = sr.Recognizer()

    audio_file_path = audio_file_path.strip()

    if not os.path.exists(audio_file_path):
        print(f"Error: The file {audio_file_path} does not exist.")
        return

    try:
        audio_chunks = split_audio(audio_file_path)
    except Exception as e:
        print(f"Error splitting audio: {e}")
        return

    full_transcript = []

    for chunk in audio_chunks:
        try:
            with sr.AudioFile(chunk) as source:
                audio_data = recognizer.record(source)

            text = recognizer.recognize_google(audio_data, language=lang)
            print(f"Transcription for {chunk} completed.")
            full_transcript.append(text)

        except sr.UnknownValueError:
            print(f"Could not understand the audio in {chunk}.")
        except sr.RequestError as e:
            print(f"Error processing {chunk}: {e}")
        except Exception as e:
            print(f"Error with chunk {chunk}: {e}")
        finally:
            os.remove(chunk)  # Remove chunk after processing

    transcript_text = "\n".join(full_transcript)

    # Save the transcript to the output folder
    text_file_name = os.path.join(output_folder, os.path.splitext(os.path.basename(audio_file_path))[0] + ".txt")
    try:
        with open(text_file_name, "w") as text_file:
            text_file.write(transcript_text)
        print(f"Text saved to {text_file_name}")
    except Exception as e:
        print(f"Error saving the transcript: {e}")

def select_media_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Media File",
        filetypes=[("Audio Files", "*.wav;*.mp3;*.m4a"),
                  ("Video Files", "*.mp4;*.avi;*.mkv"),
                  ("All Supported Files", "*.wav;*.mp3;*.m4a;*.mp4;*.avi;*.mkv")]
    )
    return file_path

def main():
    media_file_path = select_media_file()
    if not media_file_path:
        print("No file selected, exiting...")
        return

    lang = input("Enter the language (default is 'en' for English): ").strip() or "en"

    audio_to_text(media_file_path, lang)

if __name__ == "__main__":
    main()
