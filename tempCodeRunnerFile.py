from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re

app = Flask(__name__)

# Define patterns and corresponding responses
patterns_responses = [
    (r"\bhi\b|\bhey\b|\bhello\b", ["Hello!", "Hi there!", "Hey!"]),
    (r"my name is (.*)", ["Hello {}, nice to meet you!", "Hi {}, how can I help you?"]),
    (r"what is your name?", ["I'm a chatbot!", "My name is Chatbot."]),
    (r"how are you?", ["I'm doing well, thank you!", "I'm great!"]),
    (r"sorry (.*)", ["It's okay!", "No problem."]),
    (r"quit", ["Bye, take care!"]),
]

# Function to match user input with patterns and provide response
def chatbot_response(user_input):
    response = None

    # Check if the user wants to quit
    if user_input.lower() == 'quit':
        return "Bye, take care!"

    # Iterate through patterns and responses
    for pattern, responses in patterns_responses:
        match = re.match(pattern, user_input, re.IGNORECASE)
        if match:
            response = responses[0].format(*match.groups())
            return response

    # Perform sentiment analysis if no predefined response matches
    sentiment = TextBlob(user_input).sentiment.polarity
    if sentiment > 0:
        response = "That's great to hear!"
    elif sentiment < 0:
        response = "I'm sorry to hear that."
    else:
        response = "I'm not sure how to respond. Can you please rephrase?"

    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['user_input']
    response = chatbot_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
