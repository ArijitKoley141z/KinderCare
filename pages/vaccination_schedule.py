import streamlit as st
from datetime import date, datetime
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string, generate_vaccination_schedule

def render():
    st.title("Vaccination Schedule")
    
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
        key="schedule_child_select"
    )
    st.session_state.selected_child_id = child_options[selected_name]
    
    child = db.get_child(st.session_state.selected_child_id)
    vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
    
    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Age", get_age_string(dob))
    with col2:
        st.metric("Guideline", child['country_guideline'])
    with col3:
        completed = len([v for v in vaccinations if v['status'] == 'completed'])
        st.metric("Completed", f"{completed}/{len(vaccinations)}")
    
    st.markdown("---")
    
    if not vaccinations:
        st.warning("No vaccination schedule found. Generating schedule based on guidelines...")
        schedule = generate_vaccination_schedule(dob, child['country_guideline'])
        for vacc in schedule:
            db.add_vaccination(
                child_id=st.session_state.selected_child_id,
                vaccine_name=vacc['vaccine_name'],
                vaccine_code=vacc['vaccine_code'],
                due_date=vacc['due_date'].isoformat(),
                status='pending'
            )
        st.success("Vaccination schedule generated!")
        st.rerun()
    
    categories = categorize_vaccinations(vaccinations)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overdue", "Upcoming", "Pending", "Completed"])
    
    with tab1:
        st.subheader(f"Overdue Vaccines ({len(categories['overdue'])})")
        if categories['overdue']:
            for vacc in categories['overdue']:
                render_vaccine_card(vacc, "overdue")
        else:
            st.success("No overdue vaccines!")
    
    with tab2:
        st.subheader(f"Upcoming Vaccines ({len(categories['upcoming'])})")
        if categories['upcoming']:
            for vacc in categories['upcoming']:
                render_vaccine_card(vacc, "upcoming")
        else:
            st.info("No upcoming vaccines in the next 30 days.")
    
    with tab3:
        st.subheader(f"Future Vaccines ({len(categories['pending'])})")
        if categories['pending']:
            for vacc in categories['pending']:
                render_vaccine_card(vacc, "pending")
        else:
            st.info("No future vaccines scheduled.")
    
    with tab4:
        st.subheader(f"Completed Vaccines ({len(categories['completed'])})")
        if categories['completed']:
            for vacc in categories['completed']:
                render_vaccine_card(vacc, "completed")
        else:
            st.info("No completed vaccines yet.")
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #d1ecf1; padding: 15px; border-radius: 5px; border-left: 4px solid #17a2b8;">
        <strong>Note:</strong> Always consult with your child's pediatrician before administering any vaccine. 
        The schedule shown is based on official guidelines but may need adjustment based on your child's individual health needs.
    </div>
    """, unsafe_allow_html=True)

def render_vaccine_card(vacc, status_type):
    due_date = vacc['due_date']
    if isinstance(due_date, str):
        due_date = date.fromisoformat(due_date)
    
    days_diff = (due_date - date.today()).days
    
    if status_type == "overdue":
        bg_color = "#ffebee"
        border_color = "#f44336"
        status_text = f"Overdue by {abs(days_diff)} days"
    elif status_type == "upcoming":
        bg_color = "#fff8e1"
        border_color = "#ff9800"
        status_text = f"Due in {days_diff} days"
    elif status_type == "completed":
        bg_color = "#e8f5e9"
        border_color = "#4caf50"
        administered = vacc.get('administered_date', 'Unknown')
        status_text = f"Completed on {administered}" if administered else "Completed"
    else:
        bg_color = "#e3f2fd"
        border_color = "#2196f3"
        status_text = f"Due in {days_diff} days"
    
    with st.container():
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; 
                    border-left: 4px solid {border_color}; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #333;">{vacc['vaccine_name']}</h4>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">
                        Due Date: {due_date.strftime('%B %d, %Y')}
                    </p>
                    <p style="margin: 5px 0 0 0; color: {border_color}; font-size: 14px; font-weight: bold;">
                        {status_text}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if status_type != "completed":
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("Mark Complete", key=f"complete_{vacc['id']}", width='stretch'):
                    st.session_state[f"show_complete_form_{vacc['id']}"] = True
            
            if st.session_state.get(f"show_complete_form_{vacc['id']}", False):
                with st.form(key=f"complete_form_{vacc['id']}"):
                    st.subheader(f"Complete: {vacc['vaccine_name']}")
                    
                    administered_date = st.date_input(
                        "Date Administered",
                        value=date.today(),
                        max_value=date.today()
                    )
                    
                    administered_by = st.text_input("Administered By (Doctor/Clinic)")
                    batch_number = st.text_input("Batch Number (Optional)")
                    notes = st.text_area("Notes (Optional)")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Save", type="primary", width='stretch'):
                            db.update_vaccination_status(
                                vacc['id'],
                                status='completed',
                                administered_date=administered_date.isoformat(),
                                notes=notes,
                                administered_by=administered_by,
                                batch_number=batch_number
                            )
                            st.session_state[f"show_complete_form_{vacc['id']}"] = False
                            st.success(f"{vacc['vaccine_name']} marked as completed!")
                            st.rerun()
                    with col2:
                        if st.form_submit_button("Cancel", width='stretch'):
                            st.session_state[f"show_complete_form_{vacc['id']}"] = False
                            st.rerun()
