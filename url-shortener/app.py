import streamlit as st
from flask import Flask, redirect, request, jsonify
import random
import string
import threading
import requests
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# SQLite database file name
DATABASE_FILE = 'url_database.db'

def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                short_url TEXT PRIMARY KEY,
                long_url TEXT NOT NULL
            )
        ''')
        conn.commit()

# Function to add a URL to the database
def add_url_to_db(short_url, long_url):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (short_url, long_url))
        conn.commit()

# Function to retrieve a URL from the database
def get_long_url_from_db(short_url):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
        result = cursor.fetchone()
    return result[0] if result else None

# Function to generate a short URL code
def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Route for the short URL redirection
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = get_long_url_from_db(short_url)
    if long_url:
        return redirect(long_url)
    return f"URL not found for {short_url}", 404

# Route to add a long URL and return the short URL
@app.route('/add_url', methods=['POST'])
def add_url_route():
    data = request.get_json()
    long_url = data.get("long_url")
    short_url = generate_short_url()
    add_url_to_db(short_url, long_url)  # Store in the SQLite database
    return jsonify({"short_url": short_url})

# Streamlit app
def run_streamlit_app():
    st.title("URL Shortener")

    # Initialize session state for long URL
    if 'long_url' not in st.session_state:
        st.session_state.long_url = ""

    # Input for the long URL
    st.session_state.long_url = st.text_input("Enter the long URL:", value=st.session_state.long_url)

    col1, col2 = st.columns([3, 1])  
    with col1:
        pass  
    with col2:
        if st.button("Clear"):
            st.session_state.long_url = ""  

    if st.button("Generate Short URL"):
        if st.session_state.long_url:
            # Call the Flask API to generate a short URL
            response = requests.post("http://localhost:5000/add_url", json={"long_url": st.session_state.long_url})
            if response.status_code == 200:
                short_url = response.json().get("short_url")
                st.success(f"Short URL: http://localhost:5000/{short_url}")
            else:
                st.error("Error generating short URL.")
        else:
            st.error("Please enter a valid URL.")

# Function to run both Flask and Streamlit apps
def run_flask():
    app.run(port=5000)

# Main entry point for the application
if __name__ == "__main__":
    init_db()
    threading.Thread(target=run_flask, daemon=True).start()
    run_streamlit_app()
