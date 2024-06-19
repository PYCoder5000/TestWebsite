from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is a test website. Do not share it with anyone. This is a test new line. This is a test new stack line.'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
