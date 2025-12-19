import streamlit as st
import database as db
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(
    page_title="KinderCare - Child Health & Vaccination",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stAppViewContainer"] { background-color: #ffffff; }
    
    body {
        background-color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Main content */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

db.init_database()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

if 'selected_child_id' not in st.session_state:
    children = db.get_all_children()
    st.session_state.selected_child_id = children[0]['id'] if children else None

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

nav_home, nav_diseases, nav_about, nav_login, nav_signup = st.columns([1, 1, 1, 1, 1])

with nav_home:
    if st.button("Home", key="nav_Home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()

with nav_diseases:
    if st.button("Diseases & Remedies", key="nav_DR", use_container_width=True):
        st.session_state.current_page = "Diseases & Remedies"
        st.rerun()

with nav_about:
    if st.button("About us", key="nav_About", use_container_width=True):
        st.session_state.current_page = "About us"
        st.rerun()

with nav_login:
    if st.button("Login", key="nav_Login", use_container_width=True):
        st.session_state.current_page = "Login"
        st.rerun()

with nav_signup:
    if st.button("Sign Up", key="nav_SignUp", use_container_width=True):
        st.session_state.current_page = "Sign Up"
        st.rerun()

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
<h2 style="font-size: 1.8rem; font-weight: 600; color: #333; margin: 0 0 2rem 0; text-align: left; padding: 0;">
    Your Child's Health & Vaccination<br>Companion
</h2>
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
        st.write("Image not found")

st.markdown('<div class="main">', unsafe_allow_html=True)

if st.session_state.current_page == "Home":
    from pages import home
    home.render()
elif st.session_state.current_page == "Diseases & Remedies":
    from pages import diseases_remedies
    diseases_remedies.render()
elif st.session_state.current_page == "About us":
    from pages import about_us
    about_us.render()
elif st.session_state.current_page == "Dashboard":
    from pages import dashboard
    dashboard.render()
elif st.session_state.current_page == "Vaccination Schedule":
    from pages import vaccination_schedule
    vaccination_schedule.render()
elif st.session_state.current_page == "Vaccination Timeline":
    from pages import vaccination_timeline
    vaccination_timeline.render()
elif st.session_state.current_page == "Health Timeline":
    from pages import health_timeline
    health_timeline.render()
elif st.session_state.current_page == "Assistant":
    from pages import assistant
    assistant.render()
elif st.session_state.current_page == "Login":
    from pages import login
    login.render()
elif st.session_state.current_page == "Sign Up":
    from pages import signup
    signup.render()

st.markdown('</div>', unsafe_allow_html=True)
