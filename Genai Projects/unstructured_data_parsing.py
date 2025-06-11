import requests
import json
import os
import dot
from dotenv import load_dotenv

# === Configuration ===

load_dotenv()


EURI_API_KEY= os.getenv("EURI_API_KEY")
EURI_CHAT_URL=os.getenv("EURI_CHAT_URL")
EURI_EMBED_URL=os.getenv("EURI_EMBED_URL")
MODEL = "gpt-4.1-nano"

# === Prompt Template for Key Information Extraction ===
def build_prompt(text):
    return f"""
You are an intelligent information extractor. Extract the key entities from the following text and return them in structured JSON format.

Text:
\"\"\"{text}\"\"\"

Extract the following fields if present:
- Full Name
- Email
- Phone Number
- Date
- Address
- Company
- Designation
- Skills
- Education
- Experience
- Any other useful metadata

Respond in clean JSON format only.
"""

# === Function to Extract Info ===
def extract_info(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EURI_API_KEY}"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional key information extractor."},
            {"role": "user", "content": build_prompt(text)}
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }

    response = requests.post(EURI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        try:
            result = data['choices'][0]['message']['content']
            print("📦 Extracted Information:")
            print(result)
        except Exception as e:
            print("❌ Error extracting response:", e)
    else:
        print(f"❌ Request failed with status {response.status_code}")
        print(response.text)


# === Example Input ===
if __name__ == "__main__":
    unstructured_text = """
    Hello, my name is John Doe. I completed my Bachelor in Computer Science from MIT in 2019.
    I have 4 years of experience working at Google as a Software Engineer. You can contact me at john.doe@gmail.com
    or call me at +1-987 654 3210. I specialize in Python, Flask, and NLP-based projects.
    """

    extract_info(unstructured_text)
