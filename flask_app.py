from flask import Flask, render_template
from anki.anki import anki_bp  # importujeme blueprint z anki.py

app = Flask(__name__)
app.register_blueprint(anki_bp, url_prefix='/anki')  # zaregistrujeme ho

@app.route('/')
def index():
    return render_template('app.html')

if __name__ == '__main__':
    app.run(debug=True)