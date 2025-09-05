from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World, welcome to my home page'

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', "Beyster")
    return f'Hello {name}'

if __name__ == '__main__':
    app.run(debug=True, port=5000)