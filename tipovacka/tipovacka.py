from flask import render_template, request, jsonify, Blueprint, send_from_directory
from json import dumps as jdumps
from json import load as jload
from pathlib import Path
from hashlib import sha256

# cors for localhost:5173
from flask_cors import CORS as FlaskCORS
CORS_ALLOW_ORIGINS = ['http://localhost:5173', 'http://localhost:5000']
CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']

tipo_bp = Blueprint('tipovacka', __name__, static_folder='frontend', static_url_path='')
FlaskCORS(tipo_bp, origins=CORS_ALLOW_ORIGINS, headers=CORS_ALLOW_HEADERS)

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
@tipo_bp.route('/get_users', methods=['GET'])
def get_users():
    with open_rel('users.json') as f:
        users = jload(f)
    return jsonify(users)
@tipo_bp.route('/get_points', methods=['GET'])
def get_points():
    with open_rel('points.json') as f:
        points = jload(f)
    return jsonify(points)
@tipo_bp.route('/post_points/<token>', methods=['POST'])
def post_points(token=None):
    print("Token:", token)
    if token != "5be75b7c6d652dd5e38d3034e9cd6fb9abf5df80d0687771391d5d1ba611a158": # sha256(open_rel('points.json').read().strip().encode()).hexdigest(): idea for potential security
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 403
    data = request.json
    open_rel('points.json', 'w', jdumps(data, indent=4))
    return jsonify({'status': 'success'}), 200
@tipo_bp.route('/post_users/<token>', methods=['POST'])
def post_users(token=None):
    if token != "5be75b7c6d652dd5e38d3034e9cd6fb9abf5df80d0687771391d5d1ba611a158": # sha256(open_rel('users.json').read().strip().encode()).hexdigest(): idea for potential security
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 403
    data = request.json
    open_rel('users.json', 'w', jdumps(data, indent=4))
    return jsonify({'status': 'success'}), 200