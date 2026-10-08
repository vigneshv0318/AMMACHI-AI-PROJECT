import streamlit as st
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

def load_css():
    st.markdown("""
        <style>
        .main {
            background-color: #fdf6e3; /* Solarized Light-ish, warm tone */
        }
        h1, h2, h3 {
            color: #d35400; /* Burnt Orange */
            font-family: 'Georgia', serif;
        }
        .stButton>button {
            background-color: #e67e22;
            color: white;
            border-radius: 10px;
            font-size: 18px;
        }
        .stChatInput {
            border-radius: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

def amma_speak(text):
    """
    Displays text in a 'speech bubble' style format from Ammachi.
    """
    st.markdown(f"""
        <div style="background-color: #fff3cd; border-left: 6px solid #ffa000; padding: 10px; margin: 10px 0; border-radius: 5px; color: #5d4037;">
            <h3 style="color: #d35400; margin-top: 0;">👵 Ammachi says:</h3>
            <p style="font-size: 18px; line-height: 1.5; margin-bottom: 0;">{text}</p>
        </div>
    """, unsafe_allow_html=True)
