from flask import Flask, render_template
from flask_cors import CORS
from anki.anki import anki_bp  # importujeme blueprint z anki.py
from tipovacka.tipovacka import tipo_bp  # importujeme blueprint z tipovacka.py

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:5000', 'http://localhost:4200'])  # povolíme CORS pro tyto domény
app.register_blueprint(anki_bp, url_prefix='/anki')  # zaregistrujeme ho
app.register_blueprint(tipo_bp, url_prefix='/tipovacka')  # zaregistrujeme blueprint pro tipovacka

@app.route('/')
def index():
    return render_template('app.html')

if __name__ == '__main__':
    app.run(debug=True)