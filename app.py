from flask import Flask, request
import random
import os

app = Flask(__name__)

# Store CAPTCHA tokens
tokens = []

# HTML template for CAPTCHA solving page
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudflare CAPTCHA</title>
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <style>
        body { text-align: center; font-family: Arial, sans-serif; background-color: black; color: white; }
        .container { margin-top: 50px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 Solve the CAPTCHA</h2>
        <div class="cf-turnstile" data-sitekey="0x4AAAAAAA8edKY9bI4XxjIA" data-callback="onCaptchaSolved"></div>
        <p id="status">Waiting for CAPTCHA...</p>
    </div>
    <script>
        function onCaptchaSolved(token) {
            fetch('/store_token?token=' + token);
            document.getElementById("status").innerText = "✅ CAPTCHA Solved!";
            setTimeout(() => location.reload(), 20000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def serve_page():
    return html_page

@app.route('/store_token')
def store_token():
    token = request.args.get('token')
    if token:
        tokens.append(token)
    return "Token stored!"

@app.route('/get')
def get_token():
    return tokens.pop(0) if tokens else "No tokens available"

if __name__ == "__main__":
    port = random.randint(5000, 9000)
    print(f"\n🚀 CAPTCHA Server running at: http://localhost:{port}\n")
    os.system(f"termux-open-url http://localhost:{port}")  # Open browser in Termux
    app.run(port=port)
