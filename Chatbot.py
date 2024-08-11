from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()
GEN_API_KEY = os.getenv("Gemini_API_key")

genai.configure(api_key=GEN_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        history=[
            {"role": "model", "parts": "You are a friendly chatbot"},
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )

if 'satisfaction_rating' not in  st.session_state:
    st.session_state.satisfaction_rating = 0
    st.session_state.rating_total = 0
    st.session_state.num_of_queries = 0
    st.session_state.current_rating=0


def generate_output(text):
    response = st.session_state.chat.send_message(text, stream=True)
    response.resolve()
    return response

def update_rating():
    rating = st.session_state.current_rating
    st.session_state.satisfaction_rating = st.session_state.satisfaction_rating+rating
    st.session_state.rating_total = st.session_state.rating_total+5


st.title("Chatbot with Output Insights")

st.caption("To end the conversation, write 'exit' and press the button")

st.divider()

st.header("Start Conversation")
if 'text_input_key' not in st.session_state:
    st.session_state.text_input_key = 'text_input_1'
    st.session_state.all_text=""

inp = st.text_input("What do you think?",key=st.session_state.text_input_key)
send = st.button("Send")

if send and inp:
    if inp.lower() == "exit":
        st.write("Conversation ended")
    else:
        output = generate_output(inp)
        st.write(output.text)
        if "conversation" not in st.session_state:
            st.session_state.conversation = []
        st.session_state.conversation.append({"user": inp, "bot": output.text})
        st.session_state.num_of_queries=len(st.session_state.conversation)

        st.slider(
        "Rate the response (out of 5)", 
        min_value=1, 
        max_value=5, 
        value=3, 
        key="current_rating",
        on_change=update_rating
        )


    st.session_state.text_input_key = f'text_input_{int(st.session_state.text_input_key.split("_")[-1]) + 1}'

        
if "conversation" in st.session_state:
    st.header("Conversation History")
    for exchange in st.session_state.conversation:
        st.write(f"**You**: {exchange['user']}")
        st.write(f"**Bot**: {exchange['bot']}")
        st.divider()
        st.session_state.all_text=st.session_state.all_text+exchange['user']+" "+exchange['bot']+" "


