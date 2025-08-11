from flask import render_template, request, jsonify, Blueprint, send_from_directory
from json import dumps as jdumps
from json import load as jload
from pathlib import Path
from hashlib import sha256

# cors for localhost:5173
from flask_cors import CORS as FlaskCORS
CORS_ALLOW_ORIGINS = ['http://localhost:5173', 'http://localhost:5000']
CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']

tipo_bp = Blueprint('tipovacka', __name__, static_folder='browser', static_url_path='')
FlaskCORS(tipo_bp, origins=CORS_ALLOW_ORIGINS, headers=CORS_ALLOW_HEADERS)

tip_allow_change = False  # allow changes of tips by user

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
    data = recalculate_points(data)
    open_rel('points.json', 'w', jdumps(data, indent=4))
    return jsonify({'status': 'success'}), 200
@tipo_bp.route('/post_users/<token>', methods=['POST'])
def post_users(token=None):
    if token != "5be75b7c6d652dd5e38d3034e9cd6fb9abf5df80d0687771391d5d1ba611a158": # sha256(open_rel('users.json').read().strip().encode()).hexdigest(): idea for potential security
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 403
    if not tip_allow_change:
        return jsonify({'status': 'error', 'message': 'Changes are not allowed'}), 403
    data = request.json
    open_rel('users.json', 'w', jdumps(data, indent=4))
    return jsonify({'status': 'success'}), 200
@tipo_bp.route('/get_tips_permission', methods=['GET'])
def get_tips_permission():
    return jsonify({'allowed': tip_allow_change})
@tipo_bp.route('/set_tips_permission/<allowed>', methods=['POST'])
def set_tips_permission(allowed: str):
    global tip_allow_change
    tip_allow_change = allowed.lower() == 'true'
    return jsonify({'status': 'success'})

def recalculate_points(data: list):
    tips = jload(open_rel('users.json'))
    data_editable = data.copy()
    for i, match in enumerate(data):
        for user in match['points'].keys():
            tip = tips[user][match['teams']].split(":")
            result = match['result'].split(":")
            if "-" in tip[0] or "-" in tip[1] or "-" in result[0] or "-" in result[1]:
                data_editable[i]['points'][user] = 0
            elif tip[0] == result[0] and tip[1] == result[1]:
                data_editable[i]['points'][user] = 30
            elif (tip[0] > tip[1] and result[0] > result[1]) or (tip[0] < tip[1] and result[0] < result[1]) or (tip[0] == tip[1] and result[0] == result[1]):
                data_editable[i]['points'][user] = 20 - abs(int(tip[0]) - int(result[0])) - abs(int(tip[1]) - int(result[1]))
            else:
                data_editable[i]['points'][user] = 0
    return data_editable
            