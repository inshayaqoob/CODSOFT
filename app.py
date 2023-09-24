# Import necessary libraries
import streamlit as st

# Define a dictionary with predefined rules and responses
rules = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! How can I assist you?",
    "hey": "Hey! How can I help?",
    "goodbye": "Goodbye! Have a great day!"
}

# Define a function to handle user input
def chatbot_response(user_input):
    user_input = user_input.lower()  # Convert user input to lowercase for case-insensitive matching
    response = "I'm not sure how to respond to that."

    # Check if the user input matches any of the predefined rules
    for key in rules:
        if key in user_input:
            response = rules[key]
            break

    return response

# Create a Streamlit app
st.title("Simple Rule-Based Chatbot")
st.write("Enter a message, and the chatbot will respond!")

# Create a text input widget for user input
user_input = st.text_input("You:")

# Add a button to submit the user input
if st.button("Submit"):
    # Get the chatbot's response
    response = chatbot_response(user_input)
    st.text("Chatbot: " + response)
