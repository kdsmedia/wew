from flask import Flask, render_template, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_status', methods=['GET'])
def check_status():
    username = request.args.get('username')
    if username:
        # Contoh data dummy, ganti dengan logika untuk mendapatkan data TikTok secara nyata
        data = {
            'username': username,
            'active': datetime.now().strftime('%d/%m/%Y - %H:%M:%S'),
            'status': 'on'
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Username tidak diberikan'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
