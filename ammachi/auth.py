import streamlit as st
import requests
import util

def login_page():
    # Handle Google OAuth Redirect Callback
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"]
        st.query_params.clear() # Clean URL
        with st.spinner("👵 Grandmother is verifying your Google account..."):
            try:
                res = requests.post(f"{util.API_URL}/auth/google/exchange", data={"code": auth_code}, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state['authenticated'] = True
                    st.session_state['token'] = data.get('token')
                    st.session_state['username'] = data.get('username')
                    st.success(data.get("message"))
                    st.rerun()
                else:
                    st.error("Google login failed. Please try again.")
            except Exception as e:
                st.error(f"Login error: {e}")

    st.markdown("<h1 style='text-align: center;'>👵 Ammachi's Class</h1>", unsafe_allow_html=True)
    
    auth_mode = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if auth_mode == "Login":
            st.subheader("Welcome Back, Kanna!")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Enter Class", use_container_width=True)

                if submit:
                    try:
                        res = requests.post(f"{util.API_URL}/login", json={"username": username, "password": password}, timeout=10)
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state['authenticated'] = True
                            st.session_state['token'] = data.get('token')
                            st.session_state['username'] = data.get('username')
                            st.success(data.get("message"))
                            st.rerun()
                        else:
                            try:
                                detail = res.json().get("detail", "Wrong username or password.")
                            except:
                                detail = f"Server Error ({res.status_code}): {res.text[:100]}"
                            st.error(detail)
                    except requests.exceptions.ConnectionError:
                        st.error("Grandmother's server is sleeping (Disconnected).")
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            st.divider()
            st.markdown("<p style='text-align: center;'>- OR -</p>", unsafe_allow_html=True)
            if st.button("🚀 Login with Google", key="google_login", use_container_width=True):
                try:
                    res = requests.get(f"{util.API_URL}/auth/google/url", timeout=10)
                    if res.status_code == 200:
                        login_url = res.json().get("url")
                        # Perform redirect
                        st.markdown(f'<meta http-equiv="refresh" content="0; url={login_url}">', unsafe_allow_html=True)
                        st.stop()
                    else:
                        st.error("Could not fetch Google login link.")
                except Exception as e:
                    st.error(f"Auth error: {e}")
        
        else:
            st.subheader("Join Ammachi's Class!")
            with st.form("signup_form"):
                new_user = st.text_input("Pick a Username")
                new_pass = st.text_input("Create a Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Create Account", use_container_width=True)

                if submit_signup:
                    if not new_user or not new_pass:
                        st.error("Please fill in all fields, Kanna!")
                    elif new_pass != confirm_pass:
                        st.error("Passwords don't match, Kanna!")
                    elif len(new_pass) < 4:
                        st.error("Make your password a bit longer (at least 4 characters).")
                    else:
                        try:
                            res = requests.post(f"{util.API_URL}/signup", json={"username": new_user, "password": new_pass}, timeout=10)
                            if res.status_code == 200:
                                data = res.json()
                                st.session_state['authenticated'] = True
                                st.session_state['token'] = data.get('token')
                                st.session_state['username'] = data.get('username')
                                st.success("Account created! Welcome!")
                                st.rerun()
                            else:
                                try:
                                    detail = res.json().get("detail", "Signup failed.")
                                except:
                                    detail = f"Server Error ({res.status_code}): {res.text[:100]}"
                                st.error(detail)
                        except Exception as e:
                            st.error(f"Signup error: {e}")
