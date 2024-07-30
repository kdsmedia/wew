from flask import Flask, render_template, jsonify, request
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def check_tiktok_status(username):
    url = f'https://www.tiktok.com/@{username}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='video-feed-item')

        status = 'Aktif' if posts else 'Tidak Aktif'
        last_post_date = 'Tidak ada posting' if not posts else 'Posting terbaru ditemukan'
        
        return {
            'username': username,
            'last_post_date': last_post_date,
            'status': status
        }
    except requests.RequestException as e:
        return {
            'username': username,
            'status': 'Tidak Dapat Mengakses Profil',
            'error': str(e)
        }

@app.route('/check_status', methods=['GET'])
def check_status():
    username = request.args.get('username')
    if username:
        data = check_tiktok_status(username)
        return jsonify(data)
    else:
        return jsonify({'error': 'Username tidak diberikan'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
