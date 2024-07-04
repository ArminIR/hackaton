from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import noisereduce as nr
import numpy as np
import io
from scipy.io import wavfile

app = Flask(__name__)

def reduce_noise(audio_data, sample_rate):
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)
    return reduced_noise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    language = request.form.get('language', 'en-US')
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=10)  # Listen with a 10-second timeout
        
        # Convert audio to numpy array
        audio_data = np.frombuffer(audio.get_raw_data(), np.int16)
        sample_rate = audio.sample_rate
        
        # Reduce noise
        reduced_noise_audio = reduce_noise(audio_data, sample_rate)
        
        # Convert back to audio data
        reduced_noise_audio_io = io.BytesIO()
        wavfile.write(reduced_noise_audio_io, sample_rate, reduced_noise_audio)
        reduced_noise_audio_io.seek(0)
        audio = sr.AudioData(reduced_noise_audio_io.read(), sample_rate, 2)
        
        words = recognizer.recognize_google(audio, language=language)
        return jsonify({'success': True, 'words': words})
    
    except sr.WaitTimeoutError:
        return jsonify({'success': False, 'error': 'Listening timed out while waiting for phrase to start'})
    except sr.RequestError:
        return jsonify({'success': False, 'error': 'API unavailable'})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Unable to recognize speech'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
