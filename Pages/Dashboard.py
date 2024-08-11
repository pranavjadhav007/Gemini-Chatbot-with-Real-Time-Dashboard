from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
import streamlit as st
import re

st.title("Dashboard")
st.write("This is a dashboard for analyzing text data. (Interact for 2-3 times with the Chatbot to activate the dashboard)")

if "inputs_tok" not in st.session_state:
    st.session_state.num_of_queries = 0
    st.session_state.inputs_tok=[]
    nltk.download('stopwords')
    nltk.download('punkt')

if st.session_state.num_of_queries!=0:
    st.session_state.num_of_queries=len(st.session_state.conversation)
    value_q=st.session_state.num_of_queries
    st.subheader(f"Number of queries: {value_q}")

    stop_english=stopwords.words('english')
    text=st.session_state.all_text
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    st.session_state.inputs_tok=word_tokenize(cleaned_text)
    out=[]
    out = [word.capitalize() for word in st.session_state.inputs_tok if word.lower() not in stop_english]
    word_count = Counter(out)
    sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    df = pd.DataFrame(list(sorted_word_count.items()), columns=['Common Topic', 'Frequency'])
    df = df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)


    col1, col2 = st.columns(2)
    if st.session_state.rating_total==0:
        satisfaction_percentage=0
    else:
        satisfaction_percentage = (st.session_state.satisfaction_rating/st.session_state.rating_total)*100

    with col1:
        st.subheader(f"Customer Satisfaction")
    with col2:
        st.markdown(
            f"""
            <style>
            .circle-wrap {{
                margin: 0 auto;
                width: 150px;
                height: 150px;
                background: #f2f2f2;
                border-radius: 50%;
                display: grid;
                place-items: center;
            }}
            .circle {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: conic-gradient(
                    #4caf50 {satisfaction_percentage * 3.6}deg,
                    #ddd 0deg
                );
                display: grid;
                place-items: center;
                font-size: 20px;
                font-weight: bold;
                color: black;
            }}
            </style>
            <div class="circle-wrap">
                <div class="circle">
                    {satisfaction_percentage}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Common Topic")
    st.bar_chart(df[:7], x="Common Topic", y="Frequency", horizontal=True)
