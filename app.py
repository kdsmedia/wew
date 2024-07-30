from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_tiktok_status(username):
    url = f'https://www.tiktok.com/@{username}'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='video-feed-item')

        status = 'Aktif' if posts else 'Tidak Aktif'
        last_post_date = 'Tidak ada posting' if not posts else 'Posting terbaru ditemukan'
        
        return {
            'username': username,
            'last_post_date': last_post_date,
            'status': status
        }
    else:
        return {
            'username': username,
            'status': 'Tidak Dapat Mengakses Profil'
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
    app.run(debug=True)
