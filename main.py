# main.py

import streamlit as st
import re
import random
import json

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("bot.json")

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_string()

def random_string():
    random_list = [
        "Please try writing something more descriptive.",
        "Oh! It appears you wrote something I don't understand yet",
        "Do you mind trying to rephrase that?",
        "I'm terribly sorry, I didn't quite catch that.",
        "I can't answer that yet, please try asking something else."
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]

def main():
    # Set background image using custom CSS
    st.markdown(
        """
        <style>
        body {
            background-image: url("chatbot_background.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        .stApp {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title('Lets help you!')
    
    col1, col2 = st.columns([2, 1])

    with col1:
        user_input = st.text_area('User Input', height=200, placeholder='Type your message here...')
        if st.button('Submit'):
            bot_response = get_response(user_input)
            st.text('Bot Response:')
            st.write(bot_response)
            st.text('')  # Add an empty line
            user_input = ''  # Clear user input after submission

    with col2:
        st.image("chatbot_icon.jpg", use_column_width='auto')
        st.text('')  # Add an empty line
        

if __name__ == "__main__":
    main()
