import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def render_header():
    """Render the persistent header with title, subtitle, and hero image"""
    st.markdown("""
<style>
    [data-testid="stButton"] button {
        color: #667eea !important;
        background-color: transparent !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1rem !important;
    }
    
    [data-testid="stButton"] button:hover {
        color: #764ba2 !important;
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

    col_text, col_image = st.columns([1.2, 1])

    with col_text:
        st.markdown("""
<h1 style="font-size: 3.5rem; font-weight: 800; color: #667eea; margin: 0.5rem 0 0 0; text-align: left; padding: 0;">
    KinderCare
</h1>
<h2 style="font-size: 1.8rem; font-weight: 600; color: #333; margin: 0 0 0.5rem 0; text-align: left; padding: 0;">
    Your Child's Health & Vaccination<br>Companion
</h2>
<p style="font-size: 1.1rem; color: #666; text-align: left; margin: 0.5rem 0 2rem 0; padding: 0;">
    Track vaccinations, monitor health milestones, and connect with healthcare experts
</p>
""", unsafe_allow_html=True)

    with col_image:
        # Load and encode image as base64 to avoid fullscreen icon
        try:
            img = Image.open("home_hero.jpg")
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            st.markdown(f'<img src="data:image/jpeg;base64,{img_str}" style="width: 100%; max-width: 500px;">', unsafe_allow_html=True)
        except:
            pass
