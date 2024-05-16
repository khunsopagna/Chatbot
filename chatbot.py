import nltk
from nltk.chat.util import Chat, reflections
from transformers import pipeline

# Ensure you have the necessary NLTK data files
nltk.download('punkt')

# Define pairs of patterns and responses
pairs = [
    (r"my name is (.*)", ["Hello %1, How are you today?"]),
    (r"hi|hey|hello", ["Hello", "Hey there"]),
    (r"what is your name?", ["I am a chatbot created by you"]),
    (r"how are you?", ["I'm doing good, thank you!", "I'm fine, thank you. How can I assist you today?"]),
    (r"sorry (.*)", ["It's okay", "No problem"]),
    (r"(.*) age?", ["I am a computer program, so I don't have an age"]),
    (r"quit", ["Bye, take care!"]),
]

# Create Chat object with predefined pairs
chatbot = Chat(pairs, reflections)

# Initialize sentiment analysis pipeline
# Initialize sentiment analysis pipeline
sentiment_analysis = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english', revision='af0f99b')


# Function to detect emotion using transformers
def detect_emotion(text):
    result = sentiment_analysis(text)[0]
    label = result['label']
    if label == 'POSITIVE':
        return "positive"
    elif label == 'NEGATIVE':
        return "negative"
    else:
        return "neutral"

# Function to get chatbot response
def chatbot_response(text):
    emotion = detect_emotion(text)
    if emotion == "positive":
        return "That's great to hear!"
    elif emotion == "negative":
        return "I'm sorry to hear that. How can I help you?"
    else:
        # If the sentiment is neutral, use predefined responses
        response = chatbot.respond(text)
        if response:
            return response[0]
        else:
            # If no predefined response is matched, provide a generic response
            return "I'm not sure how to respond. Can you please rephrase?"

if __name__ == "__main__":
    print("Hi, I'm your chatbot. Type something to start a conversation. Type 'quit' to end the chat.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            print("Chatbot: Bye, take care!")
            break
        response = chatbot_response(user_input)
        print(f"Chatbot: {response}")
