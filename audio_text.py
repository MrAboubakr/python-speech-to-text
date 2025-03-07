from flask import Flask, request, jsonify
import speech_recognition as sr
import os

app = Flask(__name__)

# Ensure the output directory exists
OUTPUT_DIR = "output_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    filename = os.path.join(OUTPUT_DIR, audio_file.filename)
    
    try:
        # Save the file temporarily
        audio_file.save(filename)

        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Open the audio file
        with sr.AudioFile(filename) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)  # Using Google's STT engine
        
        # Save transcription result to a file
        output_text_file = filename.replace('.wav', '.txt')  # Assuming WAV input
        with open(output_text_file, "w", encoding="utf-8") as f:
            f.write(text)

        return jsonify({
            "message": "Transcription successful",
            "transcribed_text": text,
            "output_file": output_text_file
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Optional: Clean up files after processing
        os.remove(filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
