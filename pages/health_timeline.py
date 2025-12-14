import streamlit as st
from datetime import date, datetime
import plotly.graph_objects as go
import database as db
from vaccination_guidelines import get_age_string

def render():
    st.title("Health Timeline")
    
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
        key="timeline_child_select"
    )
    st.session_state.selected_child_id = child_options[selected_name]
    
    child = db.get_child(st.session_state.selected_child_id)
    vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
    health_events = db.get_health_events(st.session_state.selected_child_id)
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Add Health Event", type="primary", use_container_width=True):
            st.session_state.show_add_event = True
    
    if st.session_state.get('show_add_event', False):
        render_add_event_form(st.session_state.selected_child_id)
    
    filter_options = ["All", "Vaccines", "Illness", "Symptom", "Doctor Visit"]
    selected_filter = st.selectbox("Filter by Category", filter_options)
    
    st.markdown("---")
    
    timeline_items = []
    
    completed_vaccines = [v for v in vaccinations if v['status'] == 'completed']
    for vacc in completed_vaccines:
        administered_date = vacc.get('administered_date')
        if administered_date:
            if isinstance(administered_date, str):
                administered_date = date.fromisoformat(administered_date)
            timeline_items.append({
                'date': administered_date,
                'type': 'Vaccines',
                'title': f"Vaccine: {vacc['vaccine_name']}",
                'description': vacc.get('notes', ''),
                'icon': 'vaccine',
                'color': '#4caf50',
                'details': {
                    'Administered by': vacc.get('administered_by', 'Not recorded'),
                    'Batch Number': vacc.get('batch_number', 'Not recorded')
                }
            })
    
    for event in health_events:
        event_date = event['event_date']
        if isinstance(event_date, str):
            event_date = date.fromisoformat(event_date)
        
        event_type = event['event_type']
        if event_type == 'illness':
            color = '#f44336'
            type_label = 'Illness'
        elif event_type == 'symptom':
            color = '#ff9800'
            type_label = 'Symptom'
        else:
            color = '#2196f3'
            type_label = 'Doctor Visit'
        
        timeline_items.append({
            'date': event_date,
            'type': type_label,
            'title': event['title'],
            'description': event.get('description', ''),
            'icon': event_type,
            'color': color,
            'id': event['id'],
            'details': {
                'Severity': event.get('severity', 'Not specified'),
                'Symptoms': event.get('symptoms', 'Not recorded'),
                'Treatment': event.get('treatment', 'Not recorded'),
                'Doctor': event.get('doctor_name', 'Not recorded'),
                'Hospital/Clinic': event.get('hospital_clinic', 'Not recorded')
            }
        })
    
    if selected_filter != "All":
        timeline_items = [item for item in timeline_items if item['type'] == selected_filter]
    
    timeline_items.sort(key=lambda x: x['date'], reverse=True)
    
    if timeline_items:
        st.subheader(f"Timeline ({len(timeline_items)} events)")
        
        render_timeline_chart(timeline_items[:20])
        
        st.markdown("---")
        st.subheader("Detailed View")
        
        for item in timeline_items:
            render_timeline_card(item)
    else:
        st.info("No health events recorded yet. Add health events to build your child's health timeline.")
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #17a2b8;">
        <strong>Tip:</strong> Keep track of all health events including illnesses, symptoms, and doctor visits. 
        This helps you and your healthcare provider understand your child's complete health history.
    </div>
    """, unsafe_allow_html=True)

def render_add_event_form(child_id):
    with st.form(key="add_health_event_form"):
        st.subheader("Add Health Event")
        
        col1, col2 = st.columns(2)
        with col1:
            event_type = st.selectbox(
                "Event Type",
                ["illness", "symptom", "doctor_visit"],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        with col2:
            event_date = st.date_input("Event Date", value=date.today(), max_value=date.today())
        
        title = st.text_input("Title", placeholder="e.g., Cold and Fever, Regular Checkup")
        description = st.text_area("Description", placeholder="Brief description of the event")
        
        col1, col2 = st.columns(2)
        with col1:
            severity = st.selectbox("Severity", ["Mild", "Moderate", "Severe", "N/A"])
        with col2:
            symptoms = st.text_input("Symptoms", placeholder="e.g., Fever, Cough, Runny nose")
        
        treatment = st.text_input("Treatment Given", placeholder="e.g., Paracetamol, Rest")
        
        col1, col2 = st.columns(2)
        with col1:
            doctor_name = st.text_input("Doctor Name (Optional)")
        with col2:
            hospital_clinic = st.text_input("Hospital/Clinic (Optional)")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Save Event", type="primary", use_container_width=True):
                if not title:
                    st.error("Please enter a title for the event.")
                else:
                    db.add_health_event(
                        child_id=child_id,
                        event_type=event_type,
                        event_date=event_date.isoformat(),
                        title=title,
                        description=description,
                        severity=severity if severity != "N/A" else None,
                        symptoms=symptoms,
                        treatment=treatment,
                        doctor_name=doctor_name,
                        hospital_clinic=hospital_clinic
                    )
                    st.session_state.show_add_event = False
                    st.success("Health event added successfully!")
                    st.rerun()
        with col2:
            if st.form_submit_button("Cancel", use_container_width=True):
                st.session_state.show_add_event = False
                st.rerun()

def render_timeline_chart(items):
    if not items:
        return
    
    dates = [item['date'] for item in items]
    types = [item['type'] for item in items]
    titles = [item['title'] for item in items]
    colors = [item['color'] for item in items]
    
    fig = go.Figure()
    
    type_y = {'Vaccines': 3, 'Illness': 2, 'Symptom': 1, 'Doctor Visit': 0}
    
    for i, item in enumerate(items):
        fig.add_trace(go.Scatter(
            x=[item['date']],
            y=[type_y.get(item['type'], 0)],
            mode='markers+text',
            marker=dict(size=15, color=item['color']),
            text=[item['title'][:20] + '...' if len(item['title']) > 20 else item['title']],
            textposition='top center',
            name=item['type'],
            showlegend=False,
            hovertemplate=f"<b>{item['title']}</b><br>Date: {item['date']}<br>Type: {item['type']}<extra></extra>"
        ))
    
    fig.update_layout(
        height=250,
        margin=dict(t=30, b=30, l=80, r=20),
        xaxis_title="Date",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=['Doctor Visit', 'Symptom', 'Illness', 'Vaccines']
        ),
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_timeline_card(item):
    with st.container():
        st.markdown(f"""
        <div style="background-color: #fff; padding: 15px; border-radius: 8px; 
                    border-left: 4px solid {item['color']}; margin-bottom: 10px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span style="background-color: {item['color']}; color: white; padding: 2px 8px; 
                                 border-radius: 4px; font-size: 12px; font-weight: bold;">
                        {item['type']}
                    </span>
                    <h4 style="margin: 8px 0 5px 0; color: #333;">{item['title']}</h4>
                    <p style="margin: 0; color: #666; font-size: 14px;">
                        {item['date'].strftime('%B %d, %Y')}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if item.get('description'):
            st.write(item['description'])
        
        details = item.get('details', {})
        relevant_details = {k: v for k, v in details.items() if v and v != 'Not recorded'}
        
        if relevant_details:
            with st.expander("View Details"):
                for key, value in relevant_details.items():
                    st.write(f"**{key}:** {value}")
        
        if 'id' in item:
            if st.button("Delete", key=f"delete_event_{item['id']}", type="secondary"):
                db.delete_health_event(item['id'])
                st.success("Event deleted!")
                st.rerun()
