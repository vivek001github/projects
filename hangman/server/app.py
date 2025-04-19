import streamlit as st
import random
import requests
import nltk
from nltk.corpus import words

# Ensure the NLTK corpus is downloaded
nltk.download("words")

# Function to get a random word
def get_random_word():
    api_url = "https://random-word-api.herokuapp.com/word?number=1"
    response = requests.get(api_url)
    if response.status_code == 200:
        word = response.json()[0].upper()
        return word
    return "ERROR"

# Hangman images
HANGMAN_PICS = [
    "https://upload.wikimedia.org/wikipedia/commons/8/8b/Hangman-0.png",
    "https://upload.wikimedia.org/wikipedia/commons/3/30/Hangman-1.png",
    "https://upload.wikimedia.org/wikipedia/commons/7/70/Hangman-2.png",
    "https://upload.wikimedia.org/wikipedia/commons/9/97/Hangman-3.png",
    "https://upload.wikimedia.org/wikipedia/commons/2/27/Hangman-4.png",
    "https://upload.wikimedia.org/wikipedia/commons/6/6b/Hangman-5.png",
    "https://upload.wikimedia.org/wikipedia/commons/d/d6/Hangman-6.png"
]

# Initialize session state if not set
if "word" not in st.session_state:
    st.session_state.word = get_random_word()
    st.session_state.guessed_letters = []
    st.session_state.wrong_guesses = 0
    st.session_state.wrong_letters = []
    st.session_state.hint = ""
    st.session_state.hint_requested = False

# Function to reset the game
def reset_game():
    st.session_state.word = get_random_word()
    st.session_state.guessed_letters = []
    st.session_state.wrong_guesses = 0
    st.session_state.wrong_letters = []
    st.session_state.hint = ""
    st.session_state.hint_requested = False

st.title("Hangman Game")
st.write("Try to guess the word before the hangman is fully drawn!")

# Hint button
toggle_hint = st.button("Get Hint")
if toggle_hint and not st.session_state.hint_requested:
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{st.session_state.word.lower()}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "meanings" in data[0]:
            meanings = data[0]["meanings"]
            if meanings:
                definition = meanings[0]["definitions"][0]["definition"]
                st.session_state.hint = f"Hint: {definition}"
            else:
                st.session_state.hint = f"Hint: This word is related to {st.session_state.word[0]} and often used in sentences like 'This is an important concept in language and communication.'"
        else:
            st.session_state.hint = f"Hint: This word starts with '{st.session_state.word[0]}' and is commonly associated with daily conversations."
    else:
        st.session_state.hint = f"Hint: This word starts with '{st.session_state.word[0]}' and is often used in an educational or descriptive context."
    st.session_state.hint_requested = True

if st.session_state.hint_requested:
    st.write(f"**Hint:** {st.session_state.hint}")

# Quit button
if st.button("Quit Game"):
    reset_game()

# Input for guessing a letter
letter = st.text_input("Enter a letter:", max_chars=1, key="letter_input").upper()
if st.button("Guess") and letter:
    if letter in st.session_state.guessed_letters:
        st.warning("You already guessed that letter!")
    else:
        st.session_state.guessed_letters.append(letter)
        if letter not in st.session_state.word:
            st.session_state.wrong_guesses += 1
            st.session_state.wrong_letters.append(letter)
            remaining_guesses = len(HANGMAN_PICS) - 1 - st.session_state.wrong_guesses
            st.warning(f"Wrong guess! You have {remaining_guesses} guesses remaining.")

# Display Hangman image in center
st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <img src="{HANGMAN_PICS[min(st.session_state.wrong_guesses, len(HANGMAN_PICS)-1)]}" width="200">
    </div>
""", unsafe_allow_html=True)

# Update display word after guesses
display_word = " ".join([char if char in st.session_state.guessed_letters else "_" for char in st.session_state.word])
st.write(f"**Word:** {display_word}")

# Display wrong guesses
if st.session_state.wrong_letters:
    st.write(f"**Wrong guesses:** {', '.join(st.session_state.wrong_letters)}")

# Check game status
if "_" not in display_word:
    st.success(f"Congratulations! You guessed the word: {st.session_state.word}")
    if st.button("Play Again"):
        reset_game()
elif st.session_state.wrong_guesses >= len(HANGMAN_PICS) - 1:
    st.error(f"Game Over! The word was: {st.session_state.word}")
    if st.button("Try Again"):
        reset_game()
