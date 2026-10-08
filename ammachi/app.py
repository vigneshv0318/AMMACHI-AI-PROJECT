import streamlit as st
from auth import login_page
from modules import vision, voice, culture
import util

st.set_page_config(page_title="Ammachi Tamil Tutor", page_icon="👵", layout="wide")

# ... (CSS load) ...
util.load_css()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def main():
    if not st.session_state['authenticated']:
        login_page()
    else:
        st.sidebar.title("👵 Ammachi's Class")
        
        menu = ["Vision Node (Handwriting)", "Cultural Discovery (Agent)", "Voice Node (Fluency)"]
        choice = st.sidebar.radio("Choose Activity", menu)
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout"):
            st.session_state['authenticated'] = False
            st.rerun()

        if choice == "Vision Node (Handwriting)":
            vision.vision_node()
        elif choice == "Cultural Discovery (Agent)":
            culture.culture_node()
        elif choice == "Voice Node (Fluency)":
            voice.voice_node()

if __name__ == "__main__":
    main()
