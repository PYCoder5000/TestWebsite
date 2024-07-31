from flask import Flask, render_template, request, redirect, url_for, session, flash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import random
import boto3
import re
app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.secret_key = "RaptoringRaptors"
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1233281019776340049/ogLfkroHdPaDE9rLiEfspn2VBcmh-Ox1Tn1UKyFbEiYkoxFlap8M2A-RzKecHtLtU_mv'
@app.route('/')
def hello_world():
    return render_template('page.html')
random_int = random.randint(1, 100)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('WebStackDbStack3CD8F8E5-AccountsBE8A900E-6FQFLCPFKBFD')
ses = boto3.client('ses', region_name='us-east-1')
s = URLSafeTimedSerializer(app.secret_key + "BUTNO")
PRE = r"[a-z]{1, }[0-9]{1, }"
@app.route('/random')
def random_number():
    return {'randomNumber': random_int}
@app.route('/discord', methods=['GET', 'POST'])
def discord():
    if request.method == 'POST':
        message = request.form['message']
        if message:
            for i in range(146):
                send_to_discord(message + f" Repetition: {i}")
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
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not re.match(PRE, password):
            return "Please make sure that you include at least 1 LOWERCASE letter and then follow it with at least 1 NUMBER!"
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        table.put_item(
            Item={
                'userId': username,
                'email': email,
                'password': hashed_password,
                'verified': False,
            }
        )
        token = s.dumps(email, salt='email-confirm')
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('verify.html', confirm_url=confirm_url)

        ses.send_email(
            Source='chrisbobacat@gmail.com',
            Destination={
                'ToAddresses': [
                    email,
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Please confirm your email'
                },
                'Body': {
                    'Html': {
                        'Data': html
                    }
                }
            }
        )
        flash('A confirmation email has been sent to you. Please check your email to complete the registration.')
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except (SignatureExpired, BadTimeSignature):
        return '<h1>The confirmation link is invalid or has expired.</h1>'

    table.update_item(
        Key={
            'email': email
        },
        UpdateExpression="set verified = :v",
        ExpressionAttributeValues={
            ':v': True
        },
        ReturnValues="UPDATED_NEW"
    )

    return '<h1>Your email has been confirmed!</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        
        response = table.get_item(
            Key={
                'email': request.form['email']
            }
        )
        user = response.get('Item')
        
        if user and check_password_hash(user['password'], password):
            if user.get('verified', False):
                session['username'] = user['userId']
                return redirect(url_for('profile'))
            else:
                flash('Please verify your email before logging in.')
                return redirect(url_for('login'))
        else:
            flash('Login failed. Please check your username, email, and password.')
            return redirect(url_for('login'))
    
    return render_template('login.html')
@app.route('/profile')
def profile():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
