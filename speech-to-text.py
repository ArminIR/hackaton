from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    language = request.form.get('language', 'en-US')
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        words = recognizer.recognize_google(audio, language=language)
        return jsonify({'success': True, 'words': words})
    
    except sr.RequestError:
        return jsonify({'success': False, 'error': 'API unavailable'})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Unable to recognize speech'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
