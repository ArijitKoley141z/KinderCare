import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string
from notifications import get_in_app_notifications

def render():
    st.title("Dashboard")
    
    children = db.get_all_children()
    
    if not children:
        st.info("Welcome! Please add a child profile in the Settings page to get started.")
        if st.button("Go to Settings", type="primary"):
            st.session_state.current_page = "Settings"
            st.rerun()
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
        st.markdown("### Notifications")
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
            <p style="font-size: 36px; margin: 10px 0; font-weight: bold;">{progress:.0f}%</p>
            <p style="margin: 0;">{completed} of {total} vaccines completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        overdue_count = len(categories['overdue'])
        upcoming_count = len(categories['upcoming'])
        
        if overdue_count > 0:
            bg_color = "linear-gradient(135deg, #eb3349 0%, #f45c43 100%)"
            status_text = f"{overdue_count} Overdue"
        elif upcoming_count > 0:
            bg_color = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
            status_text = f"{upcoming_count} Upcoming"
        else:
            bg_color = "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)"
            status_text = "All up to date!"
        
        st.markdown(f"""
        <div style="background: {bg_color}; 
                    padding: 20px; border-radius: 10px; color: white;">
            <h3 style="margin: 0; color: white;">Status</h3>
            <p style="font-size: 24px; margin: 10px 0; font-weight: bold;">{status_text}</p>
            <p style="margin: 0;">Guideline: {child['country_guideline']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vaccination Status Overview")
        
        status_data = {
            'Status': ['Completed', 'Overdue', 'Upcoming', 'Pending'],
            'Count': [
                len(categories['completed']),
                len(categories['overdue']),
                len(categories['upcoming']),
                len(categories['pending'])
            ]
        }
        
        colors = ['#38ef7d', '#f45c43', '#f5576c', '#4facfe']
        
        fig = go.Figure(data=[go.Pie(
            labels=status_data['Status'],
            values=status_data['Count'],
            hole=.4,
            marker_colors=colors
        )])
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2),
            margin=dict(t=20, b=20, l=20, r=20),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Upcoming Vaccines Timeline")
        
        upcoming = categories['upcoming'] + categories['overdue']
        upcoming_sorted = sorted(upcoming, key=lambda x: x['due_date'] if isinstance(x['due_date'], date) 
                                  else date.fromisoformat(x['due_date']))[:5]
        
        if upcoming_sorted:
            timeline_data = []
            for v in upcoming_sorted:
                due = v['due_date']
                if isinstance(due, str):
                    due = date.fromisoformat(due)
                days_diff = (due - date.today()).days
                timeline_data.append({
                    'Vaccine': v['vaccine_name'],
                    'Days': days_diff,
                    'Status': 'Overdue' if days_diff < 0 else 'Upcoming'
                })
            
            fig = go.Figure()
            for item in timeline_data:
                color = '#f45c43' if item['Status'] == 'Overdue' else '#38ef7d'
                fig.add_trace(go.Bar(
                    y=[item['Vaccine']],
                    x=[item['Days']],
                    orientation='h',
                    marker_color=color,
                    text=f"{abs(item['Days'])} days {'ago' if item['Days'] < 0 else 'away'}",
                    textposition='outside'
                ))
            
            fig.update_layout(
                showlegend=False,
                xaxis_title="Days from Today",
                height=300,
                margin=dict(t=20, b=40, l=20, r=20),
                barmode='stack'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No upcoming vaccines in the next 30 days!")
    
    st.markdown("---")
    st.subheader("Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("View Schedule", use_container_width=True):
            st.session_state.current_page = "Vaccination Schedule"
            st.rerun()
    
    with col2:
        if st.button("Health Timeline", use_container_width=True):
            st.session_state.current_page = "Health Timeline"
            st.rerun()
    
    with col3:
        if st.button("Ask Assistant", use_container_width=True):
            st.session_state.current_page = "Assistant"
            st.rerun()
    
    with col4:
        if st.button("Settings", use_container_width=True):
            st.session_state.current_page = "Settings"
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107;">
        <strong>Medical Disclaimer:</strong> This application provides general vaccination tracking and health information. 
        It is not a substitute for professional medical advice, diagnosis, or treatment. 
        Always consult your child's pediatrician for personalized medical guidance.
    </div>
    """, unsafe_allow_html=True)
