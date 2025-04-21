from flask import Flask, request, jsonify, render_template
from chatbot import DialogflowChatBot  # assuming your class is in chatbot.py

app = Flask(__name__)
bot = DialogflowChatBot(project_id="manas-vlav")  # initialize once

@app.route('/')
def index():
    return render_template('index.html')  # loads the HTML UI

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = bot.get_response(user_input)
    return jsonify({'reply': response})

if __name__ == '__main__':
    app.run(debug=True)
