import streamlit as st
import streamlit.components.v1 as components
import requests
import util
import urllib.parse

def render_google_login(client_id):
    # This component renders the Google Sign-In button and sends the credential back to Streamlit
    # via a query parameter or a postMessage. For Streamlit, query params are easiest for a simple fix.
    
    html_code = f"""
    <div id="g_id_onload"
         data-client_id="{client_id}"
         data-context="signin"
         data-ux_mode="popup"
         data-callback="handleCredentialResponse"
         data-auto_prompt="false">
    </div>
    <div class="g_id_signin"
         data-type="standard"
         data-shape="rectangular"
         data-theme="outline"
         data-text="signin_with"
         data-size="large"
         data-logo_alignment="left">
    </div>

    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <script>
        function handleCredentialResponse(response) {{
            // Send the token to the parent (Streamlit)
            const token = response.credential;
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: token
            }}, '*');
        }}
    </script>
    """
    
    # Render the component and catch the token
    # We use a custom component key to track the value
    token = components.html(html_code, height=50)
    return token
