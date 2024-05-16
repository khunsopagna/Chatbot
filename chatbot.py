import tkinter as tk
from tkinter import scrolledtext, INSERT
from textblob import TextBlob
import re

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

# Function to handle user input and display chatbot responses
def send_message(event=None):
    user_input = entry.get()
    if user_input:
        conversation.config(state=tk.NORMAL)
        conversation.insert(tk.END, "You: " + user_input + "\n", "user")
        conversation.insert(tk.END, "Chatbot: " + chatbot_response(user_input) + "\n", "chatbot")
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
conversation = scrolledtext.ScrolledText(root, width=50, height=20, state=tk.DISABLED, bg="#fff", font=("Arial", 12))
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

# Start the GUI
root.mainloop()
