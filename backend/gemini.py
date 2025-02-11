import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set in environment.")
genai.configure(api_key=api_key)

def generate_summary(query: str, articles: list) -> str:
    """
    Given the user query and a list of articles (each a dict with 'title' and 'content'),
    build a system prompt and call Gemini to generate a summary answer.
    """
    # Build a prompt that lists the query and each article's title and a short excerpt.
    prompt = f"You are given the following user query:\n\"{query}\"\n\n"
    prompt += "Below are several articles retrieved from Wikipedia along with their contents. "
    prompt += "For each article, assess whether its content supports, contradicts, or is irrelevant to the query. Then, "
    prompt += "summarize whether the articles provide corroborating evidence or not.\n\n"
    for article in articles:
        # Use only the first 300 characters of content as excerpt.
        excerpt = article["content"][:300] + "..."
        prompt += f"Title: {article['title']}\nExcerpt: {excerpt}\n\n"
    prompt += "Provide a brief summary answer."
    
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
    return response.text
