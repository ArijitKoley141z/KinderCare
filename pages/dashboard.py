import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string
from notifications import get_in_app_notifications

def render():
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">Dashboard</h1>', unsafe_allow_html=True)
    
    children = db.get_all_children()
    
    if not children:
        st.info("Welcome! Please add a child profile in the Settings page to get started.")
        return
    
    if 'selected_child_id' not in st.session_state or st.session_state.selected_child_id is None:
        st.session_state.selected_child_id = children[0]['id']
    
    child_options = {c['name']: c['id'] for c in children}
    selected_name = st.selectbox(
        "Select Child",
        options=list(child_options.keys()),
        index=list(child_options.values()).index(st.session_state.selected_child_id) 
              if st.session_state.selected_child_id in child_options.values() else 0
    )
    st.session_state.selected_child_id = child_options[selected_name]
    
    child = db.get_child(st.session_state.selected_child_id)
    vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
    
    notifications = get_in_app_notifications(st.session_state.selected_child_id)
    if notifications:
        st.markdown('<h2 style="color: #667eea; margin-bottom: 1rem; font-weight: 700;">🔔 Notifications</h2>', unsafe_allow_html=True)
        for notif in notifications:
            if notif['type'] == 'error':
                st.error(f"**{notif['title']}**: {notif['message']}")
            elif notif['type'] == 'warning':
                st.warning(f"**{notif['title']}**: {notif['message']}")
            else:
                st.info(f"**{notif['title']}**: {notif['message']}")
    
    st.markdown("---")
    
    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    age = get_age_string(dob)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white;">
            <h3 style="margin: 0; color: white;">Child Profile</h3>
            <p style="font-size: 24px; margin: 10px 0; font-weight: bold;">{child['name']}</p>
            <p style="margin: 0;">Age: {age}</p>
        </div>
        """, unsafe_allow_html=True)
    
    categories = categorize_vaccinations(vaccinations)
    
    with col2:
        total = len(vaccinations)
        completed = len(categories['completed'])
        progress = (completed / total * 100) if total > 0 else 0
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 20px; border-radius: 10px; color: white;">
            <h3 style="margin: 0; color: white;">Vaccination Progress</h3>
            <p style="font-size: 24px; margin: 10px 0; font-weight: bold;">{completed}/{total}</p>
            <p style="margin: 0;">Completed: {progress:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        upcoming = len(categories['upcoming'])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%); 
                    padding: 20px; border-radius: 10px; color: white;">
            <h3 style="margin: 0; color: white;">Upcoming Vaccines</h3>
            <p style="font-size: 24px; margin: 10px 0; font-weight: bold;">{upcoming}</p>
            <p style="margin: 0;">Pending</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h2 style="color: #667eea; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;">💉 Vaccination Categories</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: #e8f5e9; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #4caf50;">
            <h4 style="color: #2e7d32; margin: 0 0 0.5rem 0;">Completed</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #4caf50; margin: 0;">{len(categories['completed'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #fff3e0; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #ff9800;">
            <h4 style="color: #e65100; margin: 0 0 0.5rem 0;">Upcoming</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #ff9800; margin: 0;">{len(categories['upcoming'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #f3e5f5; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #9c27b0;">
            <h4 style="color: #6a1b9a; margin: 0 0 0.5rem 0;">Pending</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #9c27b0; margin: 0;">{len(categories['pending'])}</p>
        </div>
        """, unsafe_allow_html=True)
