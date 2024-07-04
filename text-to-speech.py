from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        lang = request.form['lang']
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = "output.mp3"
        tts.save(audio_file)
        return send_file(audio_file, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
