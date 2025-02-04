from flask import Flask, request, jsonify
from textblob import TextBlob
from googleapiclient.discovery import build
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY is not set. Please set it in your environment variables.")

def get_translate_service():
    try:
        return build("translate", "v2", developerKey=GOOGLE_API_KEY)
    except Exception as e:
        raise RuntimeError(f"Error initializing Google Translate API: {e}")

class AICoach:
    def __init__(self):
        try:
            self.translate_service = get_translate_service()
        except Exception as e:
            self.translate_service = None
            print(f"Translation service unavailable: {e}")

    def translate_text(self, input_text, target_language="en"):
        if not self.translate_service:
            return input_text  # Fallback to returning original text if translation is unavailable
        try:
            response = self.translate_service.translations().list(
                q=input_text, target=target_language
            ).execute()
            return response["translations"][0]["translatedText"]
        except Exception as e:
            print(f"Translation error: {e}")
            return input_text  # Fallback to returning original text if translation fails

    def correct_text(self, input_text):
        # Attempt translation
        translated_text = self.translate_text(input_text)
        # Correct grammar and spelling using TextBlob
        corrected_text = str(TextBlob(translated_text).correct())
        # Generate feedback
        feedback = self.generate_feedback(translated_text, corrected_text)
        return corrected_text, feedback

    def generate_feedback(self, original_text, corrected_text):
        feedback = []
        original_words = original_text.split()
        corrected_words = corrected_text.split()

        if original_words != corrected_words:
            feedback.append(
                "The text was corrected for grammatical accuracy. Review the corrections to understand areas for improvement."
            )
        if len(original_text) < 20:
            feedback.append("Try to provide more detailed explanations to express your thoughts clearly.")
        elif len(original_text) > 150:
            feedback.append("Consider breaking long sentences into shorter ones for better readability.")
        feedback.append(
            "Expand your technical vocabulary by exploring industry-specific terms to enhance precision and professionalism."
        )
        return "\n".join(feedback)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the AI Coach API! Use the `/correct_text` endpoint to submit text for correction.", 200

@app.route('/correct_text', methods=['POST'])
def correct_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Invalid input. Please provide text in JSON format.'}), 400

        input_text = data['text']
        ai_coach = AICoach()
        corrected_text, feedback = ai_coach.correct_text(input_text)

        return jsonify({
            'original_text': input_text,
            'corrected_text': corrected_text,
            'feedback': feedback
        }), 200
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
