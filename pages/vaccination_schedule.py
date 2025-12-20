import streamlit as st
from datetime import date, datetime
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string, generate_vaccination_schedule
import json
import os

def load_vaccine_data():
    """Load vaccine data from JSON files"""
    data = {
        "India (UIP)": None,
        "WHO": None
    }
    
    try:
        with open("data/vaccines_uip_india.json", "r") as f:
            data["India (UIP)"] = json.load(f)
    except FileNotFoundError:
        pass
    
    try:
        with open("data/vaccines_who.json", "r") as f:
            data["WHO"] = json.load(f)
    except FileNotFoundError:
        pass
    
    return data

def render():
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">📋 Vaccination Schedule</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #000; margin-bottom: 1.5rem;">Track your child\'s vaccination schedule based on recommended guidelines</p>', unsafe_allow_html=True)
    
    children = db.get_all_children()
    
    if not children:
        st.info("Please add a child profile first to see vaccination schedule.")
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
        st.subheader(f"🔴 Overdue Vaccines ({len(categories['overdue'])})")
        if categories['overdue']:
            for vacc in categories['overdue']:
                render_vaccine_card(vacc, "overdue")
        else:
            st.success("✅ No overdue vaccines!")
    
    with tab2:
        st.subheader(f"🟠 Upcoming Vaccines ({len(categories['upcoming'])})")
        if categories['upcoming']:
            for vacc in categories['upcoming']:
                render_vaccine_card(vacc, "upcoming")
        else:
            st.info("No upcoming vaccines in the next 30 days.")
    
    with tab3:
        st.subheader(f"🟡 Future Vaccines ({len(categories['pending'])})")
        if categories['pending']:
            for vacc in categories['pending']:
                render_vaccine_card(vacc, "pending")
        else:
            st.info("No future vaccines scheduled.")
    
    with tab4:
        st.subheader(f"🟢 Completed Vaccines ({len(categories['completed'])})")
        if categories['completed']:
            for vacc in categories['completed']:
                render_vaccine_card(vacc, "completed")
        else:
            st.info("No completed vaccines yet.")
    
    st.markdown("---")
    
    vaccine_data = load_vaccine_data()
    guideline = child['country_guideline']
    
    if guideline in vaccine_data and vaccine_data[guideline]:
        st.markdown(f'<h2 style="color: #667eea; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;">📚 {guideline} Guideline Information</h2>', unsafe_allow_html=True)
        data = vaccine_data[guideline]
        st.markdown(f"**Source:** {data.get('source', 'Unknown')}")
        st.markdown(f"**Description:** {data.get('description', '')}")
    
    st.markdown("""
    <div class="info-box" style="background: #f0f7ff; border-left: 4px solid #667eea; padding: 1.5rem; border-radius: 8px;">
        <h3 style="color: #667eea; margin: 0 0 0.5rem 0;">📌 Important Note</h3>
        <p style="color: #333; margin: 0;">Always consult with your child's pediatrician before administering any vaccine. The schedule shown is based on official guidelines but may need adjustment based on your child's individual health needs.</p>
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
        icon = "🔴"
        status_text = f"Overdue by {abs(days_diff)} days"
    elif status_type == "upcoming":
        bg_color = "#fff8e1"
        border_color = "#ff9800"
        icon = "🟠"
        status_text = f"Due in {days_diff} days"
    elif status_type == "completed":
        bg_color = "#e8f5e9"
        border_color = "#4caf50"
        icon = "🟢"
        administered = vacc.get('administered_date', 'Unknown')
        status_text = f"Completed on {administered}" if administered else "Completed"
    else:
        bg_color = "#e3f2fd"
        border_color = "#2196f3"
        icon = "🟡"
        status_text = f"Due on {due_date.strftime('%B %d, %Y')}"
    
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; border-left: 5px solid {border_color}; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h4 style="margin: 0; color: #333;">{icon} {vacc['vaccine_name']}</h4>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9rem;">{status_text}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
