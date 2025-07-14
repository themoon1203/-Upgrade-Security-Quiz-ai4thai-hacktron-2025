from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api1', methods=['GET', 'POST'])
def api1():
    data = None
    if request.method == 'POST':
        data = request.json

    print('API1: Received request from User %s' % (
        'with data: ' + str(data) if data else 'without data'
    ))

    target_url = 'http://api2:5001/api2'

    if data:
        response = requests.post(target_url, json=data)
    else:
        response = requests.get(target_url)

    print('API1: Got response from API2: %s' % response.text)

    return jsonify({'answer': response.json().get('answer')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)