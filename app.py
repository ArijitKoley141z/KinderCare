import streamlit as st
import database as db

st.set_page_config(
    page_title="Smart Child Vaccination & Health Assistant",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #1e88e5;
        text-align: center;
        padding: 1rem 0;
    }
    .stButton>button {
        border-radius: 8px;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

db.init_database()

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

if 'selected_child_id' not in st.session_state:
    children = db.get_all_children()
    st.session_state.selected_child_id = children[0]['id'] if children else None

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0.5rem;">
        <h1 style="color: #1e88e5; margin: 0; font-size: 2.2rem; font-weight: 700; line-height: 1.2;">
            Smart Child<br>
            <span style="color: #43a047;">Vaccination</span><br>
            <span style="color: #ff7043;">Health Assistant</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    children = db.get_all_children()
    if children:
        st.markdown("**Current Child:**")
        if st.session_state.selected_child_id:
            child = db.get_child(st.session_state.selected_child_id)
            if child:
                st.info(f"👶 {child['name']}")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; color: #888;">
        <p>Version 1.0.0</p>
        <p>Made with ❤️ for parents</p>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.current_page == "Dashboard":
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
elif st.session_state.current_page == "Settings":
    from pages import settings
    settings.render()
