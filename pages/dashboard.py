import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string
from notifications import get_in_app_notifications
import pandas as pd


def render():
    st.markdown("""
    <style>
        .category-card {
            height: 140px;
            padding: 1.5rem;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 style="color: #667eea; margin-top: 0;">Dashboard</h1>', unsafe_allow_html=True)

    user_id = st.session_state.get('user_id')
    children = db.get_all_children(user_id=user_id) if user_id else []

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
        <div style="background: linear-gradient(135deg,#667eea,#764ba2);
                    padding:20px;border-radius:10px;color:white;">
            <h3 style="margin:0;">Child Profile</h3>
            <p style="font-size:24px;font-weight:bold;margin:10px 0;">{child['name']}</p>
            <p style="margin:0;">Age: {age}</p>
        </div>
        """, unsafe_allow_html=True)

    categories = categorize_vaccinations(vaccinations)

    with col2:
        total = len(vaccinations)
        completed = len(categories['completed'])
        progress = (completed / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#11998e,#38ef7d);
                    padding:20px;border-radius:10px;color:white;">
            <h3 style="margin:0;">Vaccination Progress</h3>
            <p style="font-size:24px;font-weight:bold;margin:10px 0;">{completed}/{total}</p>
            <p style="margin:0;">Completed: {progress:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        upcoming = len(categories['upcoming'])
        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#ff9a56,#ff6a88);
                    padding:20px;border-radius:10px;color:white;">
            <h3 style="margin:0;">Upcoming Vaccines</h3>
            <p style="font-size:24px;font-weight:bold;margin:10px 0;">{upcoming}</p>
            <p style="margin:0;">Pending</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<h2 style="color:#667eea;margin-top:2rem;">💉 Vaccination Categories</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="category-card" style="background:#E8F5E9;border-left:4px solid #81C784;">
            <h4 style="color:#2E7D32;margin-bottom:8px;">✓ Completed</h4>
            <p style="font-size:1.6rem;font-weight:bold;color:#81C784;margin:0;">
                {len(categories['completed'])}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="category-card" style="background:#E3F2FD;border-left:4px solid #64B5F6;">
            <h4 style="color:#1565C0;margin-bottom:8px;">➜ Upcoming</h4>
            <p style="font-size:1.6rem;font-weight:bold;color:#64B5F6;margin:0;">
                {len(categories['upcoming'])}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="category-card" style="background:#FFEBEE;border-left:4px solid #EF5350;">
            <h4 style="color:#C62828;margin-bottom:8px;">⚠️ Overdue</h4>
            <p style="font-size:1.6rem;font-weight:bold;color:#EF5350;margin:0;">
                {len(categories['overdue'])}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="category-card" style="background:#FFF3E0;border-left:4px solid #FFB74D;">
            <h4 style="color:#E65100;margin-bottom:8px;">⏳ Pending</h4>
            <p style="font-size:1.6rem;font-weight:bold;color:#FFB74D;margin:0;">
                {len(categories['pending'])}
            </p>
        </div>
        """, unsafe_allow_html=True)
