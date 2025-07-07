from flask import render_template, request, jsonify, Blueprint
from json import dumps as jdumps
from pathlib import Path


anki_bp = Blueprint('anki', __name__, template_folder='templates')
def open_rel(filename):
    """Open a file relative to the current script's directory."""
    return open(Path(__file__).parent.resolve() / filename)

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
        open_rel("data.json").write(jdumps(content, indent=2))
        return jsonify({"status": "success", "message": "Data updated successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "No data provided"}), 400