from flask import Flask, redirect, url_for
from flask_dance.contrib.discord import make_discord_blueprint, discord
import requests

app = Flask(__name__)
app.secret_key = 'supersekrit'
app.config['DISCORD_OAUTH_CLIENT_ID'] = 'your-client-id'
app.config['DISCORD_OAUTH_CLIENT_SECRET'] = 'your-client-secret'
app.config['DISCORD_OAUTH_REDIRECT_URI'] = '/discord/login/callback'

# Webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1279633587494322258/E-cVxbD0uuBBDI1HtbAM2crWXK7ymnilujVwExR5yEHH-IDIMKBhzN-tFLzeE8Xgid6p'

discord_bp = make_discord_blueprint(scope='identify email')
app.register_blueprint(discord_bp, url_prefix='/discord')

def send_log(message):
    payload = {'content': message}
    requests.post(WEBHOOK_URL, json=payload)

@app.route('/')
def home():
    if not discord.is_logged_in:
        return redirect(url_for('discord.login'))
    user_info = discord.get('/users/@me').json()
    send_log(f'User authorized: {user_info["username"]}')
    return f'Hello, {user_info["username"]}!'

if __name__ == "__main__":
    app.run(debug=True)
