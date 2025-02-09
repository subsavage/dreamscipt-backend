import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)

def get_story_chain():
    """Returns the Gemini model for text generation."""
    return genai.GenerativeModel("gemini-pro")

def generate_story(prompt):
    """Generates a story continuation using Gemini AI."""
    model = get_story_chain()
    response = model.generate_content(prompt)
    return response.text if response else "Error: No response from AI."
