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
        padding: 1rem 2rem;
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
        gap: 1rem;
        align-items: center;
    }
    
    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
        border-radius: 6px;
    }
    
    .nav-link:hover {
        color: #667eea;
        background-color: #f5f5f5;
    }
    
    .nav-link.active {
        color: #667eea;
        font-weight: 700;
    }
    
    .btn-login {
        color: #667eea;
        border: 2px solid #667eea;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .btn-login:hover {
        background-color: #667eea;
        color: white;
    }
    
    .btn-signup {
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-signup:hover {
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

nav_pages = ["Home", "Diseases & Remedies", "About us"]

navbar_html = f"""
<div class="navbar">
    <div class="navbar-left">
        👶 KinderCare
    </div>
    <div class="navbar-right">
"""

for page in nav_pages:
    active_class = "active" if st.session_state.current_page == page else ""
    navbar_html += f'<span class="nav-link {active_class}" onclick="document.querySelector(\'[key=nav_{page}]\').click()">{page}</span>'

navbar_html += """
    </div>
</div>
"""

st.markdown(navbar_html, unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])

with col1:
    if st.button("Home", key="nav_Home", use_container_width=True, type="primary" if st.session_state.current_page == "Home" else "secondary"):
        st.session_state.current_page = "Home"
        st.rerun()

with col2:
    if st.button("Diseases & Remedies", key="nav_Diseases & Remedies", use_container_width=True, type="primary" if st.session_state.current_page == "Diseases & Remedies" else "secondary"):
        st.session_state.current_page = "Diseases & Remedies"
        st.rerun()

with col3:
    if st.button("About us", key="nav_About us", use_container_width=True, type="primary" if st.session_state.current_page == "About us" else "secondary"):
        st.session_state.current_page = "About us"
        st.rerun()

with col4:
    if st.button("🔐 Login", key="nav_Login", use_container_width=True, type="secondary"):
        st.session_state.current_page = "Login"
        st.rerun()

with col5:
    if st.button("✍️ Sign Up", key="nav_Sign Up", use_container_width=True, type="primary"):
        st.session_state.current_page = "Sign Up"
        st.rerun()

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
