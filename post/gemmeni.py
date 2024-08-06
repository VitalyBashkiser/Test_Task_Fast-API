import google.generativeai as genai
from decouple import config


HARM_PROBABILITY = ["LOW", "MEDIUM", "HIGH"]

genai.configure(api_key=config("GOOGLE_API_KEY"))

MODEL = genai.GenerativeModel("gemini-1.5-flash")
