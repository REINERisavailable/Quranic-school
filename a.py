import streamlit as st
from g4f.client import Client

# Inject custom CSS to use the Rubik font from Google Fonts and set RTL direction
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Rubik', sans-serif;
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='font-family: \"Almarai\", sans-serif;'>"
            "المساعد الذكي الإسلامي"
            "</h1>", unsafe_allow_html=True)

client = Client()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='font-family: \"Rubik\", sans-serif;'>{message['content']}</div>", unsafe_allow_html=True)

prompt = st.chat_input("السلام عليكم ورحمة الله وبركاته. كيف يمكنني مساعدتك اليوم؟")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div style='font-family: \"Rubik\", sans-serif;'>{prompt}</div>", unsafe_allow_html=True)
    
    system_message = {
        "role": "system",
        "content": "You are a Muslim chatbot. Respond to the user in Arabic with references to the Quran and Sunah. Keep the conversation Islamic."
    }
    
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            system_message,
            *st.session_state["messages"],
            {"role": "user", "content": f"User has sent the following prompt: {prompt} (don't forget to answer in Arabic + Islamic way + with Quran and Sunah references + you are a Muslim chatbot talking to your Muslim brothers and sisters)"}
        ]
    )

    assistant_message = response.choices[0].message.content

    st.session_state["messages"].append({"role": "assistant", "content": assistant_message})

    with st.chat_message("assistant"):
        st.markdown(f"<div style='font-family: \"Rubik\", sans-serif;'>{assistant_message}</div>", unsafe_allow_html=True)
