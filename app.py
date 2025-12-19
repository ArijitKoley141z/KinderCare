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
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
        background-color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: -5rem -5rem 2rem -5rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    
    .header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    /* Navigation */
    .nav-container {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
        justify-content: center;
        padding: 1rem 0;
    }
    
    .nav-btn {
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        border: none;
        background-color: white;
        color: #667eea;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        font-size: 0.95rem;
    }
    
    .nav-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .nav-btn.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .nav-btn.auth {
        min-width: 120px;
    }
    
    /* Main content */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    
    /* Hero */
    .hero {
        text-align: center;
        padding: 3rem 1rem;
        margin-bottom: 2rem;
    }
    
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .hero h2 {
        font-size: 1.5rem;
        color: #555;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .hero p {
        font-size: 1.1rem;
        color: #888;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Card Grid */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .card-gradient {
        background: linear-gradient(135deg, var(--gradient-start, #667eea) 0%, var(--gradient-end, #764ba2) 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .card-gradient:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .card h3 {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .card p {
        font-size: 0.9rem;
        opacity: 0.9;
        color: white;
    }
    
    /* Info Box */
    .info-box {
        background-color: #f0f7ff;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 2rem 0;
    }
    
    .info-box h3 {
        color: #667eea;
        margin: 0 0 0.5rem 0;
    }
    
    .info-box p {
        color: #333;
        margin: 0;
        line-height: 1.6;
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

st.markdown('<div class="header"><h1>👶 KinderCare</h1></div>', unsafe_allow_html=True)

pages_nav = [
    ("Home", "🏠"),
    ("Dashboard", "📊"),
    ("Vaccination Schedule", "💉"),
    ("Vaccination Timeline", "📈"),
    ("Health Timeline", "📅"),
    ("Diseases & Remedies", "🏥"),
    ("Assistant", "🤖"),
]

cols = st.columns(len(pages_nav) + 2)

for idx, (page, icon) in enumerate(pages_nav):
    with cols[idx]:
        if st.button(f"{icon} {page}", key=f"nav_{page}", use_container_width=True,
                     type="primary" if st.session_state.current_page == page else "secondary"):
            st.session_state.current_page = page
            st.rerun()

with cols[len(pages_nav)]:
    if st.button("🔐 Login", key="nav_login", use_container_width=True,
                 type="secondary"):
        st.session_state.current_page = "Login"
        st.rerun()

with cols[len(pages_nav) + 1]:
    if st.button("✍️ Sign Up", key="nav_signup", use_container_width=True,
                 type="primary"):
        st.session_state.current_page = "Sign Up"
        st.rerun()

st.markdown('<div class="main">', unsafe_allow_html=True)

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
