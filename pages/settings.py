import streamlit as st
from datetime import date, datetime
import os
import database as db
from vaccination_guidelines import generate_vaccination_schedule
import layout

def render():
    layout.render_header()
    st.title("Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Child Profiles", "Notifications", "Data Management", "About"])
    
    with tab1:
        render_child_profiles()
    
    with tab2:
        render_notification_settings()
    
    with tab3:
        render_data_management()
    
    with tab4:
        render_about()

def render_child_profiles():
    st.subheader("Manage Child Profiles")
    
    if st.button("Add New Child Profile", type="primary"):
        st.session_state.show_add_child = True
    
    if st.session_state.get('show_add_child', False):
        render_add_child_form()
    
    children = db.get_all_children()
    
    if children:
        st.markdown("---")
        st.subheader("Existing Profiles")
        
        for child in children:
            render_child_profile_card(child)
    else:
        st.info("No child profiles yet. Add a child to get started with vaccination tracking.")

def render_add_child_form():
    with st.form(key="add_child_form"):
        st.subheader("Add New Child")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Child's Name", placeholder="Enter child's name")
        with col2:
            dob = st.date_input(
                "Date of Birth",
                value=date.today(),
                max_value=date.today(),
                min_value=date(2000, 1, 1)
            )
        
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox(
                "Vaccination Guideline",
                ["India (UIP)", "WHO", "CDC (USA)"],
                help="Select the vaccination guidelines to follow"
            )
        with col2:
            gender = st.selectbox("Gender", ["Not specified", "Male", "Female", "Other"])
        
        col1, col2 = st.columns(2)
        with col1:
            blood_group = st.selectbox(
                "Blood Group (Optional)",
                ["Not specified", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            )
        with col2:
            allergies = st.text_input("Known Allergies (Optional)", placeholder="e.g., Penicillin, Eggs")
        
        received_vaccines = st.text_area(
            "Already Received Vaccines (Optional)",
            placeholder="Enter vaccine names separated by commas (e.g., BCG, OPV, Hepatitis B)",
            help="If your child has already received some vaccines, enter their names here. They will be marked as completed."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Add Child", type="primary", width='stretch'):
                if not name:
                    st.error("Please enter the child's name.")
                else:
                    child_id = db.add_child(
                        name=name,
                        date_of_birth=dob.isoformat(),
                        country_guideline=country,
                        gender=gender if gender != "Not specified" else None,
                        blood_group=blood_group if blood_group != "Not specified" else None,
                        allergies=allergies if allergies else None
                    )
                    
                    received_list = []
                    if received_vaccines:
                        received_list = [v.strip().lower() for v in received_vaccines.split(',') if v.strip()]
                    
                    schedule = generate_vaccination_schedule(dob, country)
                    for vacc in schedule:
                        is_received = any(
                            recv in vacc['vaccine_name'].lower() or 
                            vacc['vaccine_name'].lower() in recv or
                            recv in vacc['vaccine_code'].lower()
                            for recv in received_list
                        )
                        
                        vacc_id = db.add_vaccination(
                            child_id=child_id,
                            vaccine_name=vacc['vaccine_name'],
                            vaccine_code=vacc['vaccine_code'],
                            due_date=vacc['due_date'].isoformat(),
                            status='completed' if is_received else 'pending'
                        )
                        
                        if is_received:
                            db.update_vaccination_status(
                                vacc_id,
                                status='completed',
                                administered_date=date.today().isoformat(),
                                notes='Marked as already received during profile creation'
                            )
                    
                    st.session_state.selected_child_id = child_id
                    st.session_state.show_add_child = False
                    completed_count = len([v for v in schedule if any(
                        recv in v['vaccine_name'].lower() or 
                        v['vaccine_name'].lower() in recv or
                        recv in v['vaccine_code'].lower()
                        for recv in received_list
                    )]) if received_list else 0
                    if completed_count > 0:
                        st.success(f"Child profile for {name} created! {completed_count} vaccine(s) marked as completed.")
                    else:
                        st.success(f"Child profile for {name} created with vaccination schedule!")
                    st.rerun()
        with col2:
            if st.form_submit_button("Cancel", width='stretch'):
                st.session_state.show_add_child = False
                st.rerun()

def render_child_profile_card(child):
    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    
    from vaccination_guidelines import get_age_string
    age = get_age_string(dob)
    
    with st.expander(f"{child['name']} - {age}", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Date of Birth:** {dob.strftime('%B %d, %Y')}")
            st.write(f"**Age:** {age}")
            st.write(f"**Guideline:** {child['country_guideline']}")
        with col2:
            st.write(f"**Gender:** {child.get('gender', 'Not specified')}")
            st.write(f"**Blood Group:** {child.get('blood_group', 'Not specified')}")
            st.write(f"**Allergies:** {child.get('allergies', 'None recorded')}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Edit", key=f"edit_{child['id']}", width='stretch'):
                st.session_state[f"edit_child_{child['id']}"] = True
        with col2:
            if st.button("Regenerate Schedule", key=f"regen_{child['id']}", width='stretch'):
                db.delete_all_vaccinations(child['id'])
                schedule = generate_vaccination_schedule(dob, child['country_guideline'])
                for vacc in schedule:
                    db.add_vaccination(
                        child_id=child['id'],
                        vaccine_name=vacc['vaccine_name'],
                        vaccine_code=vacc['vaccine_code'],
                        due_date=vacc['due_date'].isoformat(),
                        status='pending'
                    )
                st.success("Vaccination schedule regenerated!")
                st.rerun()
        with col3:
            if st.button("Delete", key=f"delete_{child['id']}", type="secondary", width='stretch'):
                st.session_state[f"confirm_delete_{child['id']}"] = True
        
        if st.session_state.get(f"confirm_delete_{child['id']}", False):
            st.warning(f"Are you sure you want to delete {child['name']}'s profile? This cannot be undone.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", key=f"confirm_yes_{child['id']}", type="primary"):
                    db.delete_child(child['id'])
                    st.session_state[f"confirm_delete_{child['id']}"] = False
                    if st.session_state.get('selected_child_id') == child['id']:
                        st.session_state.selected_child_id = None
                    st.success("Profile deleted.")
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"confirm_no_{child['id']}"):
                    st.session_state[f"confirm_delete_{child['id']}"] = False
                    st.rerun()
        
        if st.session_state.get(f"edit_child_{child['id']}", False):
            render_edit_child_form(child)

def render_edit_child_form(child):
    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    
    with st.form(key=f"edit_child_form_{child['id']}"):
        st.subheader(f"Edit {child['name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Child's Name", value=child['name'])
        with col2:
            new_dob = st.date_input("Date of Birth", value=dob, max_value=date.today())
        
        col1, col2 = st.columns(2)
        with col1:
            guidelines = ["India (UIP)", "WHO", "CDC (USA)"]
            country = st.selectbox(
                "Vaccination Guideline",
                guidelines,
                index=guidelines.index(child['country_guideline']) if child['country_guideline'] in guidelines else 0
            )
        with col2:
            genders = ["Not specified", "Male", "Female", "Other"]
            current_gender = child.get('gender', 'Not specified') or 'Not specified'
            gender = st.selectbox(
                "Gender",
                genders,
                index=genders.index(current_gender) if current_gender in genders else 0
            )
        
        col1, col2 = st.columns(2)
        with col1:
            blood_groups = ["Not specified", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
            current_bg = child.get('blood_group', 'Not specified') or 'Not specified'
            blood_group = st.selectbox(
                "Blood Group",
                blood_groups,
                index=blood_groups.index(current_bg) if current_bg in blood_groups else 0
            )
        with col2:
            allergies = st.text_input("Known Allergies", value=child.get('allergies', '') or '')
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Save Changes", type="primary", width='stretch'):
                db.update_child(
                    child['id'],
                    name=name,
                    date_of_birth=new_dob.isoformat(),
                    country_guideline=country,
                    gender=gender if gender != "Not specified" else None,
                    blood_group=blood_group if blood_group != "Not specified" else None,
                    allergies=allergies if allergies else None
                )
                st.session_state[f"edit_child_{child['id']}"] = False
                st.success("Profile updated!")
                st.rerun()
        with col2:
            if st.form_submit_button("Cancel", width='stretch'):
                st.session_state[f"edit_child_{child['id']}"] = False
                st.rerun()

def render_notification_settings():
    st.subheader("Notification Preferences")
    
    children = db.get_all_children()
    
    if not children:
        st.info("Add a child profile first to configure notifications.")
        return
    
    if 'selected_child_id' not in st.session_state or st.session_state.selected_child_id is None:
        st.session_state.selected_child_id = children[0]['id']
    
    child_options = {c['name']: c['id'] for c in children}
    selected_name = st.selectbox(
        "Select Child for Notification Settings",
        options=list(child_options.keys()),
        index=list(child_options.values()).index(st.session_state.selected_child_id) 
              if st.session_state.selected_child_id in child_options.values() else 0,
        key="notification_child_select"
    )
    child_id = child_options[selected_name]
    
    settings = db.get_reminder_settings(child_id) or {}
    
    with st.form(key="notification_settings_form"):
        st.markdown("### Email Notifications")
        
        email_enabled = st.checkbox(
            "Enable Email Reminders",
            value=bool(settings.get('email_enabled', False))
        )
        email_address = st.text_input(
            "Email Address",
            value=settings.get('email_address', ''),
            placeholder="your.email@example.com"
        )
        
        st.markdown("### Reminder Timing")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            reminder_7_days = st.checkbox(
                "7 days before",
                value=bool(settings.get('reminder_7_days', True))
            )
        with col2:
            reminder_1_day = st.checkbox(
                "1 day before",
                value=bool(settings.get('reminder_1_day', True))
            )
        with col3:
            reminder_on_day = st.checkbox(
                "On due date",
                value=bool(settings.get('reminder_on_day', True))
            )
        
        st.markdown("### SMS Notifications (Coming Soon)")
        
        sms_enabled = st.checkbox(
            "Enable SMS Reminders",
            value=bool(settings.get('sms_enabled', False)),
            disabled=True
        )
        phone_number = st.text_input(
            "Phone Number",
            value=settings.get('phone_number', ''),
            placeholder="+1234567890",
            disabled=True
        )
        st.info("SMS notifications require Twilio integration. This feature will be available in a future update.")
        
        if st.form_submit_button("Save Notification Settings", type="primary"):
            db.save_reminder_settings(
                child_id=child_id,
                email_enabled=email_enabled,
                email_address=email_address,
                sms_enabled=False,
                phone_number=phone_number,
                reminder_7_days=reminder_7_days,
                reminder_1_day=reminder_1_day,
                reminder_on_day=reminder_on_day
            )
            st.success("Notification settings saved!")
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #117a8b; padding: 15px; border-radius: 5px; border-left: 4px solid #0c5460; color: white;">
        <strong>Email Configuration:</strong> To send email reminders, configure SMTP settings in your environment variables:
        <ul>
            <li>SMTP_SERVER - Your SMTP server address</li>
            <li>SMTP_PORT - SMTP port (default: 587)</li>
            <li>SMTP_USER - SMTP username/email</li>
            <li>SMTP_PASSWORD - SMTP password</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def render_data_management():
    st.subheader("Data Management")
    
    st.markdown("### API Configuration")
    
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        st.success("OpenAI API Key is configured. AI Assistant is available.")
    else:
        st.warning("OpenAI API Key is not configured. Please add OPENAI_API_KEY to your secrets to enable the AI Assistant.")
    
    st.markdown("---")
    st.markdown("### Export Data")
    st.info("Data export functionality will be available in a future update.")
    
    st.markdown("---")
    st.markdown("### Database Information")
    
    children = db.get_all_children()
    total_vaccinations = 0
    total_events = 0
    
    for child in children:
        total_vaccinations += len(db.get_vaccinations(child['id']))
        total_events += len(db.get_health_events(child['id']))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Child Profiles", len(children))
    with col2:
        st.metric("Total Vaccinations", total_vaccinations)
    with col3:
        st.metric("Health Events", total_events)

def render_about():
    st.subheader("About Smart Child Vaccination & Health Assistant")
    
    st.markdown("""
    ### Overview
    
    Smart Child Vaccination & Health Assistant is a comprehensive application designed to help parents 
    track and manage their child's vaccination schedule and health history.
    
    ### Features
    
    - **Personalized Vaccination Scheduler**: Auto-generated schedules based on India UIP, WHO, or CDC guidelines
    - **Health Timeline**: Track vaccinations, illnesses, symptoms, and doctor visits
    - **Smart Reminders**: Get notified about upcoming and overdue vaccines
    - **AI Assistant**: Natural language queries about your child's health and vaccinations
    - **Voice Input**: Hands-free interaction using voice commands
    
    ### Vaccination Guidelines
    
    This application supports three major vaccination guidelines:
    
    1. **India (UIP)**: Universal Immunization Programme - Government of India
    2. **WHO**: World Health Organization recommendations
    3. **CDC (USA)**: Centers for Disease Control and Prevention (United States)
    
    ### Technology Stack
    
    - **Frontend & Backend**: Streamlit (Python)
    - **Database**: SQLite
    - **AI/NLP**: OpenAI GPT-5 & Whisper
    - **Charts**: Plotly
    
    ### Privacy & Security
    
    - All data is stored locally in SQLite database
    - No personal data is shared with third parties
    - API keys are stored securely as environment secrets
    
    ### Medical Disclaimer
    
    This application is for informational and tracking purposes only. It is NOT a substitute for 
    professional medical advice, diagnosis, or treatment. Always consult your child's pediatrician 
    or healthcare provider for personalized medical guidance.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: December 2025
    
    ---
    
    *Designed to demonstrate real-world problem solving, data handling, and AI integration 
    suitable for MNC technical evaluations.*
    """)
