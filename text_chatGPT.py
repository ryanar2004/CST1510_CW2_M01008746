from groq import Groq

client = Groq(api_key='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')

prompt = "Hey there, can you help me with my IT support questions?"

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": "You are an IT assistant."},
        {"role": "user", "content": prompt}
    ]
)

reply = completion.choices[0].message["content"]
print(reply)
