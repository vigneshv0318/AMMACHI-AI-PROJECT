import streamlit as st
import util
import requests
import io

def voice_node():
    st.header("Module 3: Pronunciation & Fluency (Voice Node)")
    
    util.amma_speak("Repeat after me: 'Vazhaipazham' (Banana). Take your time, Kanna! Press the mic to start, and press it again when you are done.")
    
    # New Streamlit Audio Input (available in st > 1.40)
    # This solves the endpointing issue by allowing manual stop
    # Note: st.audio_input returns a BytesIO object of wav data
    audio_value = st.audio_input("Record your voice")
    
    if audio_value is not None:
        # User has recorded and stopped
        st.audio(audio_value, format="audio/wav")
        
        # Auto-submit logic (improving UX to be more "Genei-like")
        with st.spinner("Ammachi is listening..."):
            try:
                # audio_value is a BytesIO-like object.
                files = {"file": ("recording.wav", audio_value, "audio/wav")}
                
                # Increased timeout
                res = requests.post(f"{util.API_URL}/voice/analyze", files=files, timeout=60)
                
                if res.status_code == 200:
                    data = res.json()
                    st.subheader("What Ammachi Heard (Cleaned):")
                    st.write(f"_{data['transcription']}_")
                    
                    st.subheader("Ammachi's Feedback:")
                    util.amma_speak(data['feedback'])
                    
                    # --- Generate Audio Response (The "Gemini" features) ---
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
                    st.error(f"Aiyayo! Connection trouble: {res.text}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
