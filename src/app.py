import random
from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')


@app.route('/')
def hello_world():
    return render_template('page.html')


random_int = random.randint(1, 100)


@app.route('/random')
def random_number():
    return {'randomNumber': random_int}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
