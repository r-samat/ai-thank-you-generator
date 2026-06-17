import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "In one sentence, what is the capital of Kazakhstan?"}
    ]
)

print(response.choices[0].message.content)