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

st.markdown("""
<style>
    .nav-tabs {
        display: flex;
        gap: 0;
        border-bottom: 2px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    .nav-tab {
        padding: 1rem 1.5rem;
        cursor: pointer;
        border: none;
        background: transparent;
        font-size: 1rem;
        font-weight: 600;
        color: #666;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
        flex: 1;
        text-align: center;
    }
    .nav-tab:hover {
        color: #667eea;
        background-color: #f9f9f9;
    }
    .nav-tab.active {
        color: #667eea;
        border-bottom-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Create navigation using custom HTML for better visibility
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    is_active = st.session_state.current_page == "Home"
    if st.button("🏠 Home", key="nav_Home", use_container_width=True, type="primary" if is_active else "secondary"):
        st.session_state.current_page = "Home"
        st.rerun()

with nav_col2:
    is_active = st.session_state.current_page == "Diseases & Remedies"
    if st.button("🏥 Diseases", key="nav_DR", use_container_width=True, type="primary" if is_active else "secondary"):
        st.session_state.current_page = "Diseases & Remedies"
        st.rerun()

with nav_col3:
    is_active = st.session_state.current_page == "About us"
    if st.button("ℹ️ About", key="nav_About", use_container_width=True, type="primary" if is_active else "secondary"):
        st.session_state.current_page = "About us"
        st.rerun()

with nav_col4:
    is_active = st.session_state.current_page == "Login"
    if st.button("🔐 Login", key="nav_Login", use_container_width=True, type="primary" if is_active else "secondary"):
        st.session_state.current_page = "Login"
        st.rerun()

with nav_col5:
    is_active = st.session_state.current_page == "Sign Up"
    if st.button("✍️ Sign Up", key="nav_SignUp", use_container_width=True, type="primary" if is_active else "secondary"):
        st.session_state.current_page = "Sign Up"
        st.rerun()

st.markdown("""
<style>
    /* Primary buttons (active tabs) */
    [data-testid="baseButton-primary"] button {
        color: white !important;
        background-color: #667eea !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1rem !important;
    }
    
    [data-testid="baseButton-primary"] button:hover {
        background-color: #764ba2 !important;
    }
    
    [data-testid="baseButton-primary"] button:active,
    [data-testid="baseButton-primary"] button:focus {
        background-color: #667eea !important;
        box-shadow: none !important;
    }
    
    /* Secondary buttons (inactive tabs) */
    [data-testid="baseButton-secondary"] button {
        color: #666 !important;
        background-color: #f5f5f5 !important;
        border: 2px solid #e0e0e0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        padding: 0.5rem 1rem !important;
    }
    
    [data-testid="baseButton-secondary"] button:hover {
        color: #667eea !important;
        background-color: #f0f7ff !important;
        border-color: #667eea !important;
    }
    
    [data-testid="baseButton-secondary"] button:active,
    [data-testid="baseButton-secondary"] button:focus {
        background-color: #f5f5f5 !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

if st.session_state.current_page == "Home":
    col_text, col_image = st.columns([1.2, 1])

    with col_text:
        st.markdown("""
<h1 style="font-size: 5rem; font-weight: 800; color: #667eea; margin: 8rem 0 0 0; text-align: left; padding: 0;">
    KinderCare
</h1>
<h2 style="font-size: 2.5rem; font-weight: 600; color: #333; margin: 0 0 0.5rem 0; text-align: left; padding: 0;">
    Your Child's Health & Vaccination<br>Companion
</h2>
<p style="font-size: 1.4rem; color: #666; text-align: left; margin: 0.5rem 0 2rem 0; padding: 0;">
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
            st.write("Image not found")

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
