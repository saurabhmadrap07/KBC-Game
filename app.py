from flask import Flask, render_template, request, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Questions and answers list
questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    # Add other questions
]

current_question = 0
winner_name = ""

@app.route('/')
def home():
    global current_question
    qr_code = generate_qr_code()
    question_text = questions[current_question]["question"]
    return render_template('index.html', question=question_text, qr_code=qr_code, winner_name=winner_name)

@app.route('/player', methods=['POST'])
def player():
    global current_question
    name = request.form.get('name')
    answer = request.form.get('answer')
    if answer.lower() == questions[current_question]["answer"].lower():
        global winner_name
        winner_name = name
        current_question += 1
        return redirect(url_for('home'))
    return render_template('player.html', message="Wrong Answer!")

def generate_qr_code():
    data = url_for('player', _external=True)
    img = qrcode.make(data)
    buffer = BytesIO()
    img.save(buffer)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_base64

if __name__ == '__main__':
    app.run(debug=True)
