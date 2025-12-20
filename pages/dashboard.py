import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string
from notifications import get_in_app_notifications
import pandas as pd

def render():
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
    
    st.markdown('<h2 style="color: #667eea; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;">📊 Vaccination Analytics</h2>', unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        status_data = {
            'Status': ['Completed', 'Upcoming', 'Overdue', 'Pending'],
            'Count': [len(categories['completed']), len(categories['upcoming']), len(categories['overdue']), len(categories['pending'])]
        }
        fig_pie = go.Figure(data=[go.Pie(
            labels=status_data['Status'],
            values=status_data['Count'],
            marker=dict(colors=['#81C784', '#64B5F6', '#EF5350', '#FFB74D']),
            textposition='inside',
            textinfo='label+percent'
        )])
        fig_pie.update_layout(
            title="Vaccination Status Overview",
            height=400,
            showlegend=True,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_chart2:
        # Calculate progress bar visualization data
        progress_bar_data = {
            'Category': ['Progress'],
            'Completed': [len(categories['completed'])],
            'Upcoming': [len(categories['upcoming'])],
            'Overdue': [len(categories['overdue'])],
            'Pending': [len(categories['pending'])]
        }
        df_progress = pd.DataFrame(progress_bar_data)
        
        fig_bar = go.Figure(data=[
            go.Bar(name='Completed', x=df_progress['Category'], y=df_progress['Completed'], marker_color='#81C784'),
            go.Bar(name='Upcoming', x=df_progress['Category'], y=df_progress['Upcoming'], marker_color='#64B5F6'),
            go.Bar(name='Overdue', x=df_progress['Category'], y=df_progress['Overdue'], marker_color='#EF5350'),
            go.Bar(name='Pending', x=df_progress['Category'], y=df_progress['Pending'], marker_color='#FFB74D')
        ])
        fig_bar.update_layout(
            barmode='stack',
            title="Vaccination Completion Status",
            yaxis_title="Number of Vaccines",
            height=400,
            showlegend=True,
            margin=dict(t=40, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown('<h2 style="color: #667eea; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;">💉 Vaccination Categories</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: #E8F5E9; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #81C784;">
            <h4 style="color: #2E7D32; margin: 0 0 0.5rem 0;">✓ Completed</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #81C784; margin: 0;">{len(categories['completed'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #E3F2FD; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #64B5F6;">
            <h4 style="color: #1565C0; margin: 0 0 0.5rem 0;">➜ Upcoming</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #64B5F6; margin: 0;">{len(categories['upcoming'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        overdue = len(categories['overdue'])
        st.markdown(f"""
        <div style="background: #FFEBEE; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #EF5350;">
            <h4 style="color: #C62828; margin: 0 0 0.5rem 0;">⚠️ Overdue</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #EF5350; margin: 0;">{overdue}</p>
        </div>
        """, unsafe_allow_html=True)
    
    col4 = st.columns(1)[0]
    with col4:
        st.markdown(f"""
        <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #FFB74D;">
            <h4 style="color: #E65100; margin: 0 0 0.5rem 0;">⏳ Pending</h4>
            <p style="font-size: 1.5rem; font-weight: bold; color: #FFB74D; margin: 0;">{len(categories['pending'])}</p>
        </div>
        """, unsafe_allow_html=True)
