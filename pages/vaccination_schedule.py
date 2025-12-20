import streamlit as st
from datetime import date
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string, generate_vaccination_schedule
import json


def load_vaccine_data():
    """Load vaccine data from JSON files"""
    data = {"India (UIP)": None, "WHO": None}
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
    """Main render function for vaccination schedule page"""
    st.set_page_config(layout="wide")
    
    # Apply custom CSS styling
    st.markdown("""
    <style>
        /* Purple cards - white text */
        .purple-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }
        .purple-card p {
            color: white !important;
            margin: 0;
        }
        .purple-card h4 {
            color: white !important;
            margin: 10px 0 0 0;
        }
        
        /* Vaccine cards - black text */
        .vaccine-card {
            padding: 18px;
            border-radius: 10px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 6px solid;
        }
        .vaccine-card h4, .vaccine-card p {
            color: #000000 !important;
            margin: 0;
        }
        .vaccine-card-title {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .vaccine-card-status {
            font-size: 0.95rem;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .vaccine-card-date {
            font-size: 0.85rem;
            color: #666666 !important;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* Tabs - black text */
        button[data-baseweb="tab"] {
            color: #000000 !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #000000 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #000000 !important;
        }
        button[data-baseweb="tab"][aria-selected="false"] {
            color: #000000 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page title
    st.markdown(
        '<h1 style="color:#667eea;margin-bottom:10px;">📋 Vaccination Schedule</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="color:#000;margin-bottom:20px;font-size:1.1rem;">Track and manage your child\'s vaccination schedule</p>',
        unsafe_allow_html=True
    )
    
    # Get all children
    children = db.get_all_children()
    if not children:
        st.info("👶 Please add a child profile first to see the vaccination schedule.")
        return
    
    # Child selection
    if 'selected_child_id' not in st.session_state:
        st.session_state.selected_child_id = children[0]['id']
    
    child_options = {c['name']: c['id'] for c in children}
    selected_name = st.selectbox(
        "👤 Select Child",
        options=list(child_options.keys()),
        index=list(child_options.values()).index(st.session_state.selected_child_id),
        key="vaccine_child_select"
    )
    st.session_state.selected_child_id = child_options[selected_name]
    
    # Get child and vaccination data
    child = db.get_child(st.session_state.selected_child_id)
    vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
    
    # Parse date of birth
    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)
    
    # Display info cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="purple-card">
            <p style="font-size: 0.9rem; margin-bottom: 8px;">🎂 Age</p>
            <h4 style="font-size: 1.8rem;">{get_age_string(dob)}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="purple-card">
            <p style="font-size: 0.9rem; margin-bottom: 8px;">📖 Guideline</p>
            <h4 style="font-size: 1.8rem;">{child['country_guideline']}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        completed = len([v for v in vaccinations if v['status'] == 'completed'])
        st.markdown(f"""
        <div class="purple-card">
            <p style="font-size: 0.9rem; margin-bottom: 8px;">✅ Completed</p>
            <h4 style="font-size: 1.8rem;">{completed}/{len(vaccinations)}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate schedule if none exists
    if not vaccinations:
        st.info("📊 Generating vaccination schedule based on guidelines...")
        schedule = generate_vaccination_schedule(dob, child['country_guideline'])
        for vacc in schedule:
            db.add_vaccination(
                child_id=st.session_state.selected_child_id,
                vaccine_name=vacc['vaccine_name'],
                vaccine_code=vacc['vaccine_code'],
                due_date=vacc['due_date'].isoformat(),
                status='pending'
            )
        st.rerun()
    
    # Categorize vaccinations
    categories = categorize_vaccinations(vaccinations)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        f"🔴 Overdue ({len(categories['overdue'])})",
        f"🟠 Upcoming ({len(categories['upcoming'])})",
        f"🔵 Pending ({len(categories['pending'])})",
        f"✅ Completed ({len(categories['completed'])})"
    ])
    
    # Overdue tab
    with tab1:
        st.markdown("<h3 style='color:#f44336; margin-top:0;'>🔴 Overdue Vaccines</h3>", unsafe_allow_html=True)
        if categories['overdue']:
            for vacc in categories['overdue']:
                render_vaccine_card(vacc, "overdue")
        else:
            st.success("✅ No overdue vaccines!")
    
    # Upcoming tab
    with tab2:
        st.markdown("<h3 style='color:#ff9800; margin-top:0;'>🟠 Upcoming Vaccines</h3>", unsafe_allow_html=True)
        if categories['upcoming']:
            for vacc in categories['upcoming']:
                render_vaccine_card(vacc, "upcoming")
        else:
            st.info("📌 No upcoming vaccines in the next 30 days")
    
    # Pending tab
    with tab3:
        st.markdown("<h3 style='color:#2196f3; margin-top:0;'>🔵 Future Vaccines</h3>", unsafe_allow_html=True)
        if categories['pending']:
            for vacc in categories['pending']:
                render_vaccine_card(vacc, "pending")
        else:
            st.info("📌 No future vaccines scheduled")
    
    # Completed tab
    with tab4:
        st.markdown("<h3 style='color:#4caf50; margin-top:0;'>✅ Completed Vaccines</h3>", unsafe_allow_html=True)
        if categories['completed']:
            for vacc in categories['completed']:
                render_vaccine_card(vacc, "completed")
        else:
            st.info("📝 No completed vaccines yet")
    
    # Display guideline information
    st.markdown("---")
    vaccine_data = load_vaccine_data()
    guideline = child['country_guideline']
    
    if guideline in vaccine_data and vaccine_data[guideline]:
        data = vaccine_data[guideline]
        st.markdown(f"<h3 style='color:#667eea;'>📚 {guideline} Guideline Information</h3>", unsafe_allow_html=True)
        st.markdown(f"**Source:** {data.get('source', 'Unknown')}")
        st.markdown(f"**Description:** {data.get('description', '')}")


def render_vaccine_card(vacc, status_type):
    """Render individual vaccine card"""
    due_date = vacc['due_date']
    if isinstance(due_date, str):
        due_date = date.fromisoformat(due_date)
    
    days_diff = (due_date - date.today()).days
    
    # Define styling based on status
    if status_type == "overdue":
        bg_color = "#ffebee"
        border_color = "#f44336"
        status_emoji = "🔴"
        status_text = f"Overdue by {abs(days_diff)} days"
    elif status_type == "upcoming":
        bg_color = "#fff8e1"
        border_color = "#ff9800"
        status_emoji = "🟠"
        status_text = f"Due in {days_diff} days"
    elif status_type == "pending":
        bg_color = "#e3f2fd"
        border_color = "#2196f3"
        status_emoji = "🔵"
        status_text = f"Due on {due_date.strftime('%d %B %Y')}"
    else:  # completed
        bg_color = "#e8f5e9"
        border_color = "#4caf50"
        status_emoji = "✅"
        administered = vacc.get('administered_date', 'Unknown')
        status_text = f"Completed on {administered}"
    
    # Render vaccine card HTML
    st.markdown(f"""
    <div class="vaccine-card" style="background-color: {bg_color}; border-left-color: {border_color};">
        <div class="vaccine-card-title">
            💉 {vacc['vaccine_name']}
        </div>
        <div class="vaccine-card-status">
            {status_emoji} {status_text}
        </div>
        <div class="vaccine-card-date">
            📅 {due_date.strftime('%A, %B %d, %Y')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        pass
    
    if status_type in ["overdue", "upcoming", "pending"]:
        with col3:
            if st.button("✓ Mark Completed", key=f"mark_completed_{vacc['id']}", use_container_width=True):
                db.update_vaccination_status(vacc['id'], 'completed', date.today().isoformat())
                st.success(f"✅ {vacc['vaccine_name']} marked as completed!")
                st.rerun()
    elif status_type == "completed":
        with col3:
            if st.button("↶ Mark Pending", key=f"mark_pending_{vacc['id']}", use_container_width=True):
                db.update_vaccination_status(vacc['id'], 'pending', None)
                st.info(f"↶ {vacc['vaccine_name']} moved back to pending")
                st.rerun()
