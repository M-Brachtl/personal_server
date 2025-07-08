from flask import render_template, request, jsonify, Blueprint, send_from_directory
from json import dumps as jdumps
from pathlib import Path


tipo_bp = Blueprint('tipovacka', __name__, static_folder='frontend', static_url_path='')
def open_rel(filename, method='r', content=None):
    """Open a file relative to the current script's directory."""
    if method == 'r':
        return open(Path(__file__).parent.resolve() / filename)
    elif method == 'w':
        return open(Path(__file__).parent.resolve() / filename, 'w').write(content)
    
# Catch-all route pro SPA routing (Vue)
@tipo_bp.route('/', defaults={'path': ''})
@tipo_bp.route('/<path:path>')
def serve_vue(path):
    if path != "" and (tipo_bp.static_folder / path).exists():
        return send_from_directory(tipo_bp.static_folder, path)
    else:
        return send_from_directory(tipo_bp.static_folder, 'index.html')