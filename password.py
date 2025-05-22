from flask import Flask, request, render_template_string
import random
import string
import webbrowser
import threading

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Password Generator</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 600px; margin: auto; }
        input[type=number] { width: 60px; }
        .password-box { background: #f4f4f4; padding: 10px; margin-top: 10px; font-family: monospace; word-break: break-all; }
        button.copy-btn { margin-left: 10px; }
        .strength { font-weight: bold; margin-top: 10px; }
        .weak { color: red; }
        .medium { color: orange; }
        .strong { color: green; }
        .password-list { margin-top: 10px; }
        .password-list div { margin-bottom: 5px; background: #eee; padding: 5px; font-family: monospace; }
    </style>
</head>
<body>
    <h2>Random Password Generator</h2>
    <form method="POST">
        Password Length: <input type="number" name="length" min="4" max="50" value="{{ length or 12 }}" required>
        Generate: <input type="number" name="count" min="1" max="10" value="{{ count or 1 }}" required>
        <button type="submit">Generate</button>
    </form>

    {% if passwords %}
        <div class="password-list">
            <h3>Generated Password{{ passwords|length > 1 and 's' or '' }}:</h3>
            {% for pwd in passwords %}
                <div>
                    <span>{{ pwd }}</span>
                    <button class="copy-btn" onclick="copyToClipboard('{{ pwd }}')">Copy</button>
                    <span class="strength {{ strength_class(pwd) }}">{{ password_strength(pwd) }}</span>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('Copied to clipboard!');
            }, function(err) {
                alert('Failed to copy text: ', err);
            });
        }
    </script>
</body>
</html>
'''

def password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length < 8 or score < 2:
        return "Weak"
    elif length >= 8 and score >= 3:
        return "Strong"
    else:
        return "Medium"

def strength_class(password):
    s = password_strength(password)
    return {
        "Weak": "weak",
        "Medium": "medium",
        "Strong": "strong"
    }.get(s, "")

@app.route('/', methods=['GET', 'POST'])
def generate_password():
    passwords = []
    length = 12
    count = 1

    if request.method == 'POST':
        try:
            length = int(request.form['length'])
            count = int(request.form['count'])
            characters = string.ascii_letters + string.digits + string.punctuation
            for _ in range(count):
                pwd = ''.join(random.choice(characters) for _ in range(length))
                passwords.append(pwd)
        except ValueError:
            passwords = []

    return render_template_string(HTML,
                                  passwords=passwords,
                                  length=length,
                                  count=count,
                                  password_strength=password_strength,
                                  strength_class=strength_class)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
