from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api2', methods=['GET', 'POST'])
def api2():
    data = None
    if request.method == 'POST':
        data = request.json

    print('API2: Received request from API1 %s' % (
        'with data: ' + str(data) if data else 'without data'
    ))

    return jsonify({'answer': 'Hello from make me happy' if not data else data.get('message')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)