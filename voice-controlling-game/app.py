import pygame
import speech_recognition as sr
import pyttsx3
import random
import time

# Initialize speech recognition
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level 0 to 1

# Function to recognize voice input
def recognize_speech():
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None

# Function to provide voice feedback
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Simple game for enhancing basic skills (math problems)
class VoiceControlledGame:
    def __init__(self):
        self.score = 0
        self.running = True
        self.questions = [
            {"question": "What is 5 plus 3?", "answer": "8"},
            {"question": "What is 7 minus 4?", "answer": "3"},
            {"question": "Spell the word 'cat'", "answer": "c a t"},
            {"question": "What is 2 times 6?", "answer": "12"}
        ]

    # Function to ask questions and check answers
    def ask_question(self):
        question = random.choice(self.questions)
        speak(question["question"])
        print(question["question"])
        user_answer = recognize_speech()
        if user_answer is not None and user_answer == question["answer"]:
            speak("Correct!")
            print("Correct!")
            self.score += 1
        else:
            speak("Incorrect!")
            print("Incorrect!")

    # Main game loop
    def play_game(self):
        speak("Welcome to the voice-controlled learning game!")
        print("Game started. Say 'stop' to end the game.")
        while self.running:
            self.ask_question()
            speak("Do you want to continue?")
            print("Say 'yes' to continue or 'no' to stop.")
            user_input = recognize_speech()
            if user_input == "no" or user_input == "stop":
                self.running = False

        speak(f"Game over. Your score is {self.score}")
        print(f"Game over. Your score is {self.score}")

# Run the game
if __name__ == "__main__":
    game = VoiceControlledGame()
    game.play_game()
