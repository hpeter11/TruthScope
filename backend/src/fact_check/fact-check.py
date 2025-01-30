import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

# Try loading API key from .env (preferred method)
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("R1-KEY")

# Validate API Key
if not DEEPSEEK_API_KEY:
    raise ValueError("API Key not found. Set it in .env or JSON config.")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def test_deepseek_reasoner():
    """Send a test query to DeepSeek-R1 and print the response."""
    
    messages = [
        {"role": "system", "content": "You are an AI that reasons logically based on evidence."},
        {"role": "user", "content": "Is water wet?"}
    ]
    
    try:
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=False  # No streaming
        )

        # Extract reasoning chain and final answer
        reasoning_content = response.choices[0].message.reasoning_content
        final_answer = response.choices[0].message.content

        print("\n=== DeepSeek-R1 API Test ===")
        print("Chain of Thought Reasoning:\n", reasoning_content)
        print("Final Answer:\n", final_answer)
        
    except Exception as e:
        print(f"Error occurred while calling DeepSeek-R1: {e}")

# Run the test
if __name__ == "__main__":
    test_deepseek_reasoner()