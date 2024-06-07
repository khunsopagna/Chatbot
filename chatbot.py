import tkinter as tk
from tkinter import scrolledtext, INSERT
from textblob import TextBlob
import re
import mysql.connector

# Define patterns and corresponding responses
patterns_responses = [
    (r"\bhi\b|\bhey\b|\bhello\b", ["Hello!", "Hi there!", "Hey!"]),
    (r"my name is (.*)", ["Hello {}, nice to meet you!", "Hi {}, how can I help you?"]),
    (r"what is your name?", ["I'm a chatbot!", "My name is Chatbot."]),
    (r"how are you?", ["I'm doing well, thank you!", "I'm great!"]),
    (r"sorry (.*)", ["It's okay!", "No problem."]),
    (r"quit", ["Bye, take care!"]),
]

# Connect to the database
connection = mysql.connector.connect(host='127.0.0.1', user='root', password='', database='chatbott_db')
cursor = connection.cursor()

# Function to match user input with patterns and provide response
def chatbot_response(user_input, user_id):
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
    if sentiment > 0.5:
        response = "That's fantastic to hear!"
    elif sentiment > 0:
        response = "That's great to hear!"
    elif sentiment == 0:
        response = "I'm not sure how to respond. Can you please rephrase?"
    elif sentiment > -0.5:
        response = "I'm sorry to hear that."
    else:
        response = "That sounds really tough. I'm here for you."

    # Insert user feedback and emotion data into the database if the input reflects a sentiment
    if sentiment != 0:
        insert_query = "INSERT INTO user_feedback (user_id, feedback_text, emotion_score) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, user_input, sentiment))
        connection.commit()

    return response

# Function to handle user input and display chatbot responses
def send_message(event=None):
    user_input = entry.get()
    if user_input:
        conversation.config(state=tk.NORMAL)
        conversation.insert(tk.END, "You: " + user_input + "\n", "user")
        response = chatbot_response(user_input, user_id)
        conversation.insert(tk.END, "Chatbot: " + response + "\n", "chatbot")
        conversation.see(INSERT)
        conversation.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Chatbot")

# Set background color and window size
root.configure(bg="#f2f2f2")
root.geometry("500x500")

# Create conversation display
conversation = scrolledtext.ScrolledText(root, width=70, height=20, state=tk.DISABLED, bg="#fff", font=("Arial", 12))
conversation.tag_config("user", foreground="#003366", font=("Arial", 12, "bold"))
conversation.tag_config("chatbot", foreground="#006600", font=("Arial", 12, "italic"))
conversation.pack(pady=10)

# Create input field
entry = tk.Entry(root, width=40, bg="#fff", font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10)

# Create send button
send_button = tk.Button(root, text="Send", command=send_message, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10, bd=0)
send_button.pack(side=tk.RIGHT, padx=10)

# Bind Enter key to send message
root.bind('<Return>', send_message)

# Sample user_id for testing
user_id = 1

# Function to display the chatbot's introductory message
def display_intro_message():
    intro_message = ("Hello! I'm a chatbot here to assist you. "
                     "You can ask me anything, share how you're feeling, "
                     "or simply chat with me. How can I help you today?")
    conversation.config(state=tk.NORMAL)
    conversation.insert(tk.END, "Chatbot: " + intro_message + "\n", "chatbot")
    conversation.config(state=tk.DISABLED)

# Display the introductory message when the GUI starts
display_intro_message()

# Start the GUI
root.mainloop()

