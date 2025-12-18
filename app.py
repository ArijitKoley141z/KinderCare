import streamlit as st
import database as db

st.set_page_config(
    page_title="Smart Child Vaccination & Health Assistant",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stButton>button {
        border-radius: 8px;
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
    st.session_state.current_page = "Home"

if 'selected_child_id' not in st.session_state:
    children = db.get_all_children()
    st.session_state.selected_child_id = children[0]['id'] if children else None

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

st.markdown("""
<div style="background: linear-gradient(90deg, #1e88e5 0%, #43a047 50%, #ff7043 100%); padding: 1rem 0; margin: -5rem -5rem 2rem -5rem; padding-left: 5rem; padding-right: 5rem;">
    <h1 style="text-align: center; color: white; margin: 0; font-size: 2rem; font-weight: 700;">
        Smart Child Vaccination & Health Assistant
    </h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

pages_nav = [
    ("Home", "🏠"),
    ("Dashboard", "📊"),
    ("Vaccination Schedule", "💉"),
    ("Vaccination Timeline", "📈"),
    ("Health Timeline", "📅"),
    ("Diseases & Remedies", "🏥"),
    ("Assistant", "🤖"),
    ("Settings", "⚙️")
]

cols = [col1, col2, col3, col4, col5, col6, col7]

for idx, (page, icon) in enumerate(pages_nav[:-1]):
    with cols[idx]:
        if st.button(f"{icon}\n{page}", key=f"nav_{page}", width='stretch',
                     type="primary" if st.session_state.current_page == page else "secondary"):
            st.session_state.current_page = page
            st.rerun()

with col7:
    children = db.get_all_children()
    if children and st.session_state.selected_child_id:
        child = db.get_child(st.session_state.selected_child_id)
        if child:
            st.info(f"👶 {child['name']}")

st.markdown("---")

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
elif st.session_state.current_page == "Settings":
    from pages import settings
    settings.render()
