import streamlit as st
from groq import Groq

client = Groq(api_key='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')

st.title("Chat with your AI buddy, ChatGPT 🤖!")


if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])


prompt = st.chat_input("Ask me anything about IT support!")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=st.session_state.messages
    )

 
    reply = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
