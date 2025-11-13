import os
from openai import OpenAI

client = OpenAI(
    api_key = "API_key_입력",
)

chat_completion = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "Say this is a test.",
        }
    ],
    model = "gpt-4o",
)

print(chat_completion.choices[0].message.content)