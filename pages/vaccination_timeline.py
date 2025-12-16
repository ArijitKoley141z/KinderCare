import streamlit as st
from datetime import date, timedelta
import plotly.graph_objects as go
import database as db
from vaccination_guidelines import get_age_string

def render():
    st.title("Vaccination Timeline")
    
    children = db.get_all_children()
    
    if not children:
        st.info("Please add a child profile in the Settings page first.")
        return
    
    if 'selected_child_id' not in st.session_state or st.session_state.selected_child_id is None:
        st.session_state.selected_child_id = children[0]['id']
    
    child_options = {c['name']: c['id'] for c in children}
    selected_name = st.selectbox(
        "Select Child",
        options=list(child_options.keys()),
        index=list(child_options.values()).index(st.session_state.selected_child_id) 
              if st.session_state.selected_child_id in child_options.values() else 0,
        key="vacc_timeline_child_select"
    )
    st.session_state.selected_child_id = child_options[selected_name]
    
    child = db.get_child(st.session_state.selected_child_id)
    vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
    
    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Child", child['name'])
    with col2:
        st.metric("Age", get_age_string(dob))
    with col3:
        completed = len([v for v in vaccinations if v['status'] == 'completed'])
        st.metric("Progress", f"{completed}/{len(vaccinations)} completed")
    
    st.markdown("---")
    
    if not vaccinations:
        st.warning("No vaccination schedule found. Please go to Settings to generate a schedule.")
        return
    
    render_visual_timeline(vaccinations, dob)
    
    st.markdown("---")
    
    render_timeline_list(vaccinations)
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #117a8b; padding: 15px; border-radius: 5px; border-left: 4px solid #0c5460; color: white;">
        <strong>Note:</strong> This timeline shows all scheduled vaccinations for your child based on the selected guidelines. 
        Green indicates completed, red indicates overdue, yellow indicates upcoming (within 30 days), and blue indicates future vaccines.
    </div>
    """, unsafe_allow_html=True)

def render_visual_timeline(vaccinations, dob):
    st.subheader("Visual Timeline")
    
    timeline_data = []
    for vacc in vaccinations:
        due_date = vacc['due_date']
        if isinstance(due_date, str):
            due_date = date.fromisoformat(due_date)
        
        days_from_birth = (due_date - dob).days
        days_from_today = (due_date - date.today()).days
        
        if vacc['status'] == 'completed':
            color = '#4caf50'
            status = 'Completed'
        elif days_from_today < 0:
            color = '#f44336'
            status = 'Overdue'
        elif days_from_today <= 30:
            color = '#ff9800'
            status = 'Upcoming'
        else:
            color = '#2196f3'
            status = 'Scheduled'
        
        timeline_data.append({
            'name': vacc['vaccine_name'],
            'due_date': due_date,
            'days_from_birth': days_from_birth,
            'months_from_birth': days_from_birth / 30.44,
            'status': status,
            'color': color
        })
    
    timeline_data.sort(key=lambda x: x['due_date'])
    
    fig = go.Figure()
    
    for i, item in enumerate(timeline_data):
        fig.add_trace(go.Scatter(
            x=[item['months_from_birth']],
            y=[0],
            mode='markers+text',
            marker=dict(size=20, color=item['color'], symbol='circle'),
            text=[item['name']],
            textposition='top center',
            name=item['name'],
            showlegend=False,
            hovertemplate=(
                f"<b>{item['name']}</b><br>"
                f"Due: {item['due_date'].strftime('%B %d, %Y')}<br>"
                f"Status: {item['status']}<extra></extra>"
            )
        ))
    
    today_months = (date.today() - dob).days / 30.44
    fig.add_vline(x=today_months, line_dash="dash", line_color="purple", 
                  annotation_text="Today", annotation_position="top")
    
    fig.update_layout(
        height=300,
        margin=dict(t=80, b=40, l=40, r=40),
        xaxis_title="Age (Months)",
        yaxis=dict(visible=False),
        hovermode='closest',
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<span style="color: #4caf50;">●</span> Completed', unsafe_allow_html=True)
    with col2:
        st.markdown('<span style="color: #f44336;">●</span> Overdue', unsafe_allow_html=True)
    with col3:
        st.markdown('<span style="color: #ff9800;">●</span> Upcoming (30 days)', unsafe_allow_html=True)
    with col4:
        st.markdown('<span style="color: #2196f3;">●</span> Scheduled', unsafe_allow_html=True)

def render_timeline_list(vaccinations):
    st.subheader("Detailed Timeline")
    
    sorted_vaccs = sorted(vaccinations, key=lambda x: x['due_date'] if isinstance(x['due_date'], date) 
                          else date.fromisoformat(x['due_date']))
    
    for i, vacc in enumerate(sorted_vaccs):
        due_date = vacc['due_date']
        if isinstance(due_date, str):
            due_date = date.fromisoformat(due_date)
        
        days_from_today = (due_date - date.today()).days
        
        if vacc['status'] == 'completed':
            bg_color = '#e8f5e9'
            border_color = '#4caf50'
            status_text = 'Completed'
            icon = '✅'
        elif days_from_today < 0:
            bg_color = '#ffebee'
            border_color = '#f44336'
            status_text = f'Overdue by {abs(days_from_today)} days'
            icon = '❌'
        elif days_from_today <= 30:
            bg_color = '#fff8e1'
            border_color = '#ff9800'
            status_text = f'Due in {days_from_today} days'
            icon = '⏰'
        else:
            bg_color = '#e3f2fd'
            border_color = '#2196f3'
            status_text = f'Scheduled for {due_date.strftime("%B %d, %Y")}'
            icon = '📅'
        
        connector = "│" if i < len(sorted_vaccs) - 1 else " "
        
        st.markdown(f"""
        <div style="display: flex; align-items: stretch; margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; margin-right: 15px;">
                <div style="width: 30px; height: 30px; border-radius: 50%; background-color: {border_color}; 
                            display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                    {i + 1}
                </div>
                <div style="width: 2px; flex-grow: 1; background-color: #ddd; min-height: 20px;"></div>
            </div>
            <div style="flex-grow: 1; background-color: {bg_color}; padding: 15px; border-radius: 8px; 
                        border-left: 4px solid {border_color}; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #333;">{icon} {vacc['vaccine_name']}</h4>
                        <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">
                            Due: {due_date.strftime('%B %d, %Y')}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <span style="background-color: {border_color}; color: white; padding: 4px 12px; 
                                     border-radius: 12px; font-size: 12px; font-weight: bold;">
                            {status_text}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
