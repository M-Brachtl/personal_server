
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, jsonify
from json import dumps as jdumps

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    # Simulovaná data pro tabulku
    data = open('/home/MB2457/mysite/data.json').read()
    return data
@app.route('/update_data', methods=['POST'])
def update_data():
    content = request.json
    if content:
        open('/home/MB2457/mysite/data.json', 'w').write(jdumps(content, indent=2))
        return jsonify({"status": "success", "message": "Data updated successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "No data provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)