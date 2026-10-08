import streamlit as st
import util
import requests
import json
import re

def culture_node():
    st.header("Module 2: Cultural Discovery Agent")
    st.caption("Agentic Workflow: Language -> Retrieval -> Challenge -> Reward")
    
    # Initialize Session
    if "culture_msgs" not in st.session_state:
        st.session_state.culture_msgs = []
        # Initial greeting from agent will be triggered by user "Starting"
    
    col_lang, col_stat = st.columns([2, 1])
    
    with col_lang:
        language = st.selectbox("Select Native Language", ["Tamil", "Telugu", "Hindi"])
        if st.button("Start Discovery"):
            st.session_state.culture_msgs = []
            st.session_state.culture_msgs.append({"role": "user", "content": f"Start session for {language}. Retrieve festivals."})
            # We trigger the first response automatically
            with st.spinner("Agent is retrieving cultural context..."):
               send_to_agent("Start session", language)

    with col_stat:
        st.subheader("🛂 Passport")
        if "user_points" not in st.session_state:
            st.session_state.user_points = 0
            st.session_state.user_stamps = []
            
        st.metric("Game Points", st.session_state.user_points)
        if st.session_state.user_stamps:
            st.write("Unlocked Stamps:")
            for stamp in st.session_state.user_stamps:
                st.markdown(f"✅ **{stamp}**")
        else:
            st.write("No stamps yet.")

    st.divider()

    # Chat Interface
    for message in st.session_state.culture_msgs:
        if message["role"] == "user" and "Start session" in message["content"]:
            continue # Don't show system trigger messages
            
        with st.chat_message(message["role"], avatar="🐯" if message["role"] == "assistant" else "🧒"):
            content = message["content"]
            
            # Media Parsing
            img_match = re.search(r'\[IMAGE: (.*?)\]', content)
            if img_match:
                img_url = img_match.group(1)
                # Validation: ensure it's a real link, not a placeholder "url" or "null"
                if img_url.startswith("http"):
                    st.image(img_url, caption="Cultural Snapshot")
                content = content.replace(img_match.group(0), "")
                
            vid_match = re.search(r'\[VIDEO: (.*?)\]', content)
            if vid_match:
                vid_url = vid_match.group(1)
                # Validation
                if vid_url.startswith("http"):
                    st.video(vid_url)
                content = content.replace(vid_match.group(0), "")
                
            # Clean reward tags from display
            content = re.sub(r'\[REWARD:.*?\]', '', content)
            content = re.sub(r'\[STAMP:.*?\]', '', content)
            
            st.markdown(content)

    if prompt := st.chat_input("Answer the challenge..."):
        st.session_state.culture_msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧒"):
            st.markdown(prompt)
        
        with st.spinner("Validating answer..."):
            send_to_agent(prompt, language)

def send_to_agent(message, language):
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.culture_msgs if "Start session" not in m["content"]]
    
    username = "student" # Default for now
    
    payload = {
        "message": message,
        "history": json.dumps(history),
        "username": username,
        "language": language
    }
    
    try:
        res = requests.post(f"{util.API_URL}/culture/chat", data=payload, timeout=60)
        if res.status_code == 200:
            data = res.json()
            response_text = data['response']
            
            # Update Stats
            st.session_state.user_points = data['points']
            st.session_state.user_stamps = data['stamps']
            
            st.session_state.culture_msgs.append({"role": "assistant", "content": response_text})
            st.rerun()
        else:
            st.error(f"Agent Error: {res.text}")
    except Exception as e:
        st.error(f"Error: {e}")
