import streamlit as st
import requests

st.title("🎓 CollegeBot")
st.caption("Ask anything about Bennett University")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about Bennett University..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": prompt}
            )
            answer = response.json()["answer"]
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})