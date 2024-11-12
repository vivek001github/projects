import streamlit as st
import random
from gtts import gTTS
from io import BytesIO

# Set the title of the app
st.title("Lingineer MVP")

# 1. User Registration and Basic Profile
st.sidebar.title("User Registration")
if 'username' not in st.session_state:
    st.session_state['username'] = None

if st.session_state['username'] is None:
    st.sidebar.subheader("Sign Up or Login")
    username = st.sidebar.text_input("Enter your name")
    engineering_field = st.sidebar.selectbox("Select your engineering field", ["Mechanical", "Electrical", "Civil", "Software"])
    english_proficiency = st.sidebar.selectbox("Rate your English Proficiency", ["Beginner", "Intermediate", "Advanced"])
    if st.sidebar.button("Submit"):
        st.session_state['username'] = username
        st.session_state['engineering_field'] = engineering_field
        st.session_state['english_proficiency'] = english_proficiency
        st.sidebar.success(f"Welcome, {username}!")
else:
    st.sidebar.write(f"Logged in as {st.session_state['username']}")

# 2. Core Learning Experience
st.subheader("Core Learning Experience")
st.write("Practice English in Engineering Scenarios:")
scenarios = {
    "Team Meeting Simulation": "Practice a conversation about daily tasks and project updates.",
    "Technical Explanation": "Explain technical terms or concepts in your field.",
    "Presentation Practice": "Introduce and summarize a project or technical report."
}
selected_scenario = st.selectbox("Choose a Scenario", list(scenarios.keys()))
st.write(scenarios[selected_scenario])

# Simple content for learning scenariosss
if st.button("Start Scenario"):
    if selected_scenario == "Team Meeting Simulation":
        st.write("Example: 'Today, we are focusing on optimizing the process flow in manufacturing.'")
    elif selected_scenario == "Technical Explanation":
        st.write("Example: 'A hydraulic press uses fluid to generate force. This is based on Pascal's law.'")
    elif selected_scenario == "Presentation Practice":
        st.write("Example: 'The purpose of this project is to enhance system performance by 20%.'")

# 3. Interactive Chat with AI Coach (simplified demo)
st.subheader("Chat with AI Coach")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_message = st.text_input("You: ", "")
if st.button("Send"):
    st.session_state['chat_history'].append(f"You: {user_message}")
    # Simulate AI response - in production, replace with actual AI coach response
    response = f"AI Coach: Let's work on improving that sentence!"
    st.session_state['chat_history'].append(response)

for message in st.session_state['chat_history']:
    st.write(message)

# 4. Pronunciation Practice (Demo)
st.subheader("Pronunciation Practice")
sentence_to_practice = random.choice([
    "The system analysis is critical for design.",
    "Please calibrate the machinery as per specifications.",
    "Safety protocols must be followed."
])
st.write(f"Practice saying: '{sentence_to_practice}'")

if st.button("Record"):
    # Placeholder for audio recording
    st.write("Recording... (Feature to be implemented)")

# Generate and play audio for feedback
audio_data = BytesIO()
tts = gTTS(text=sentence_to_practice, lang='en')
tts.write_to_fp(audio_data)
st.audio(audio_data)

# 5. Progress Tracking
st.subheader("Progress Tracking")
st.write("See your progress over time:")
if 'session_count' not in st.session_state:
    st.session_state['session_count'] = 0

if st.button("Complete Session"):
    st.session_state['session_count'] += 1
    st.write(f"Session completed! Total sessions: {st.session_state['session_count']}")

# Display basic progress dashboard
st.write(f"Total Sessions Completed: {st.session_state['session_count']}")
st.write(f"Scenarios Practiced: {selected_scenario}")

# 6. Settings
st.sidebar.title("Settings")
notifications = st.sidebar.checkbox("Enable Notifications")
if notifications:
    st.sidebar.write("You will receive practice reminders.")

# Navigation (Session Buttons and Actions)
st.sidebar.title("Navigation")
if st.sidebar.button("Start Session"):
    st.write("Session Started.")
if st.sidebar.button("Record"):
    st.write("Recording session.")
if st.sidebar.button("Play"):
    st.write("Playing audio feedback.")
