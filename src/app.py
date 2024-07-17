import random
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1233281019776340049/ogLfkroHdPaDE9rLiEfspn2VBcmh-Ox1Tn1UKyFbEiYkoxFlap8M2A-RzKecHtLtU_mv'
@app.route('/')
def hello_world():
    return render_template('page.html')


random_int = random.randint(1, 100)


@app.route('/random')
def random_number():
    return {'randomNumber': random_int}
@app.route('/discord', methods=['GET', 'POST'])
def discord():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            send_to_discord(message)
            return redirect(url_for('discord'))
    return render_template('discord.html')

def send_to_discord(message):
    data = {
        'content': message
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
