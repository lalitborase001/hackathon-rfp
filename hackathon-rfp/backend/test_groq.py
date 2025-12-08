import os
from dotenv import load_dotenv
from groq import Groq

# 1) Load variables from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing in .env")

# 2) Create Groq client
client = Groq(api_key=api_key)

# 3) Send a simple test request
chat_completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # one of Groq's models
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Say exactly this line: Groq is working for my Asian Paints RFP hackathon."
        },
    ],
)

# 4) Print the reply
print(chat_completion.choices[0].message.content)
