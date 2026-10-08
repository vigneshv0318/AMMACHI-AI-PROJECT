import requests
import streamlit as st
import util
from PIL import Image

TAMIL_LETTERS = [
    ("அ", "a"), ("ஆ", "aa"), ("இ", "i"), ("ஈ", "ii"), ("உ", "u"), 
    ("ஊ", "uu"), ("எ", "e"), ("ஏ", "ee"), ("ஐ", "ai"), ("ஒ", "o"), 
    ("ஓ", "oo"), ("ஔ", "au"), ("ஃ", "akku")
]


def vision_node():
    st.header("Module 1: Handwriting & Image Analysis (Vision Node)")
    
    # Create Tabs
    tab1, tab2 = st.tabs(["👋 Learn to Write (Stroke)", "📝 Check My Writing (Grammar)"])
    
    # --- TAB 1: Trace Mode ---
    with tab1:
        # Letter Selection
        selected_option = st.selectbox(
            "Choose a letter to practice:", 
            options=TAMIL_LETTERS, 
            format_func=lambda x: f"{x[0]} ({x[1]})"
        )
        target_char = selected_option[0]

        st.info(f"Ammachi says: 'Show me how you write {target_char}!'")
        
        # Ghost Letter Display
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<h1 style='text-align: center; color: grey; font-size: 100px;'>{target_char}</h1>", unsafe_allow_html=True)
            st.caption("Start from the bottom-left circle! Upload a VIDEO.")
        
        with col2:
            uploaded_file = st.file_uploader("Upload Video (Trace)", type=['mp4', 'mov', 'avi'], key="trace_upload")
        
        if uploaded_file is not None:
            st.video(uploaded_file)
            
            if st.button("Analyze Stroke Order"):
                with st.spinner("Ammachi is watching your stroke order..."):
                    try:
                        uploaded_file.seek(0)
                        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                        data = {"target_char": target_char, "mode": "trace"}
                        
                        # Set to 90s for vision analysis
                        res = requests.post(f"{util.API_URL}/vision/analyze", files=files, data=data, timeout=90)
                        
                        if res.status_code == 200:
                            data = res.json()
                            st.subheader("Ammachi's Feedback:")
                            util.amma_speak(data['feedback'])
                        else:
                            st.error(f"Aiyayo! My classroom is busy: {res.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- TAB 2: General Grammar Mode ---
    with tab2:
        st.subheader("Check My Handwriting & Grammar")
        st.info("Upload an image or video of a sentence or word. Ammachi will check your spelling!")
        
        grammar_file = st.file_uploader("Upload Image or Video (Grammar)", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'], key="grammar_upload")
        
        if grammar_file is not None:
            # Display content
            if grammar_file.type.startswith('video'):
                st.video(grammar_file)
            else:
                st.image(grammar_file)
                
            if st.button("Check Grammar & Spelling"):
                with st.spinner("Ammachi is reading your handwriting..."):
                    try:
                        grammar_file.seek(0)
                        files = {"file": (grammar_file.name, grammar_file, grammar_file.type)}
                        data = {"mode": "general"}
                        
                        # Set to 90s for vision analysis
                        res = requests.post(f"{util.API_URL}/vision/analyze", files=files, data=data, timeout=90)
                        
                        if res.status_code == 200:
                            data = res.json()
                            st.subheader("Ammachi's Corrections:")
                            util.amma_speak(data['feedback'])
                            
                            # --- Ammachi Speaks (Voice Over) ---
                            with st.spinner("Ammachi is speaking..."):
                                try:
                                    audio_res = requests.post(
                                        f"{util.API_URL}/voice/speak", 
                                        data={"text": data['feedback']},
                                        timeout=30
                                    )
                                    if audio_res.status_code == 200:
                                        st.audio(audio_res.content, format="audio/mpeg", autoplay=True)
                                    else:
                                        st.warning(f"Could not generate voice: {audio_res.text}")
                                except Exception as ez:
                                    st.warning(f"Audio generation failed: {ez}")
                        else:
                            st.error(f"Aiyayo! My classroom is busy: {res.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
