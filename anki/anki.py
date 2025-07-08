from flask import render_template, request, jsonify, Blueprint
from json import dumps as jdumps
from pathlib import Path


anki_bp = Blueprint('anki', __name__, template_folder='templates')
def open_rel(filename, method='r', content=None):
    """Open a file relative to the current script's directory."""
    if method == 'r':
        return open(Path(__file__).parent.resolve() / filename)
    elif method == 'w':
        return open(Path(__file__).parent.resolve() / filename, 'w').write(content)

@anki_bp.route('/')
def hello_world():
    return render_template('anki.html')

@anki_bp.route('/get_data')
def get_data():
    # Simulovaná data pro tabulku
    data = open_rel("data.json").read()
    return data
@anki_bp.route('/update_data', methods=['POST'])
def update_data():
    content = request.json
    if content:
        open_rel("data.json", method='w', content=jdumps(content, indent=2))
        return jsonify({"status": "success", "message": "Data updated successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "No data provided"}), 400