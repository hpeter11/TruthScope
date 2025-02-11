import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=key)

response = genai.GenerativeModel("gemini-1.5-flash").generate_content("Who won the superbowl?")

print(response.text)