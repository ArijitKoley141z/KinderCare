import streamlit as st
import database as db

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
    
    /* Navbar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.2rem 2rem;
        background-color: #ffffff;
        border-bottom: 1px solid #e0e0e0;
        margin: -1rem -1rem 2rem -1rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    
    .navbar-left {
        font-size: 1.5rem;
        font-weight: 800;
        color: #667eea;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .navbar-right {
        display: flex;
        gap: 0.8rem;
        align-items: center;
        flex-wrap: wrap;
        justify-content: flex-end;
    }
    
    .nav-btn {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 0.6rem 1rem;
        border-radius: 6px;
        border: none;
        background: transparent;
    }
    
    .nav-btn:hover {
        color: #667eea;
        background-color: #f5f5f5;
    }
    
    .nav-btn.active {
        color: #667eea;
        font-weight: 700;
        background-color: #f0f5ff;
    }
    
    .nav-btn.login {
        color: #667eea;
        border: 2px solid #667eea;
        padding: 0.5rem 1rem;
        margin-left: 0.5rem;
    }
    
    .nav-btn.login:hover {
        background-color: #667eea;
        color: white;
    }
    
    .nav-btn.signup {
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.6rem 1rem;
    }
    
    .nav-btn.signup:hover {
        background-color: #764ba2;
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

nav_items = [
    ("Home", "nav_Home"),
    ("Diseases & Remedies", "nav_DR"),
    ("About us", "nav_About"),
    ("Login", "nav_Login", "login"),
    ("Sign Up", "nav_SignUp", "signup")
]

navbar_html = """
<div class="navbar">
    <div class="navbar-left">
        👶 KinderCare
    </div>
    <div class="navbar-right">
"""

for item in nav_items:
    page_name = item[0]
    key = item[1]
    btn_class = item[2] if len(item) > 2 else ""
    
    active_class = "active" if st.session_state.current_page == page_name else ""
    class_attr = f"nav-btn {active_class} {btn_class}"
    
    navbar_html += f'<button class="{class_attr}" onclick="document.querySelector(\'button[key={key}]\').click()" style="cursor: pointer;">{page_name}</button>'

navbar_html += """
    </div>
</div>
"""

st.markdown(navbar_html, unsafe_allow_html=True)

if st.button("Home", key="nav_Home"):
    st.session_state.current_page = "Home"
    st.rerun()

if st.button("Diseases & Remedies", key="nav_DR"):
    st.session_state.current_page = "Diseases & Remedies"
    st.rerun()

if st.button("About us", key="nav_About"):
    st.session_state.current_page = "About us"
    st.rerun()

if st.button("Login", key="nav_Login"):
    st.session_state.current_page = "Login"
    st.rerun()

if st.button("Sign Up", key="nav_SignUp"):
    st.session_state.current_page = "Sign Up"
    st.rerun()

st.markdown("""
<style>
    [data-testid="stButton"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

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
