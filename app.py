from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/hodi',methods=['post'])
def index():
    data =request.json
    email=data['email']
    username = data['username']
    print(f'''hello {email} {username}''')
    return jsonify({'answer': 'hodi'})

@app.route('/hodi',methods=['get'])
def indexx():
    return jsonify({"welcome browser":'da'}) 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)