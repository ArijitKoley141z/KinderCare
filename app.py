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
    .stMainBlockContainer { padding-top: 0; }
    .stApp { background-color: #f8f9fa; }
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

def render_header():
    st.markdown("""
    <div class="header-bar">
        <div class="header-content">
            <a href="#" class="logo">👶 KinderCare</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navbar():
    pages_nav = [
        ("Home", "🏠"),
        ("Dashboard", "📊"),
        ("Vaccination Schedule", "💉"),
        ("Vaccination Timeline", "📈"),
        ("Health Timeline", "📅"),
        ("Diseases & Remedies", "🏥"),
        ("Assistant", "🤖"),
    ]
    
    nav_html = '<div class="navbar"><div class="navbar-content"><div class="nav-links">'
    
    for page, icon in pages_nav:
        active_class = "active" if st.session_state.current_page == page else ""
        nav_html += f'<button class="nav-btn {active_class}" onclick="window.location.hash=\'{page}\'">{icon} {page}</button>'
    
    nav_html += '</div><div class="auth-btns">'
    nav_html += '<button class="btn-login" onclick="window.location.hash=\'Login\'">Login</button>'
    nav_html += '<button class="btn-signup" onclick="window.location.hash=\'Sign Up\'">Sign Up</button>'
    nav_html += '</div></div></div>'
    
    st.markdown(nav_html, unsafe_allow_html=True)

def load_css():
    with open("assets/styles.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css()
render_header()
render_navbar()

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

pages_nav = [
    ("Home", "🏠"),
    ("Dashboard", "📊"),
    ("Vaccination Schedule", "💉"),
    ("Vaccination Timeline", "📈"),
    ("Health Timeline", "📅"),
    ("Diseases & Remedies", "🏥"),
    ("Assistant", "🤖"),
]

cols = [col1, col2, col3, col4, col5, col6, col7]

for idx, (page, icon) in enumerate(pages_nav):
    with cols[idx]:
        if st.button(f"{icon}\n{page}", key=f"nav_{page}", width='stretch',
                     type="primary" if st.session_state.current_page == page else "secondary"):
            st.session_state.current_page = page
            st.rerun()

col_login, col_signup = st.columns([1, 1])
with col_login:
    if st.button("Login", key="nav_login", width='stretch', type="secondary"):
        st.session_state.current_page = "Login"
        st.rerun()
with col_signup:
    if st.button("Sign Up", key="nav_signup", width='stretch', type="primary"):
        st.session_state.current_page = "Sign Up"
        st.rerun()

st.markdown("---")
st.markdown('<div class="main-container">', unsafe_allow_html=True)

if st.session_state.current_page == "Home":
    from pages import home
    home.render()
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
elif st.session_state.current_page == "Diseases & Remedies":
    from pages import diseases_remedies
    diseases_remedies.render()
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
