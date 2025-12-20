import streamlit as st
from datetime import date
import database as db
from vaccination_guidelines import categorize_vaccinations, get_age_string, generate_vaccination_schedule
import json


def load_vaccine_data():
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
    st.markdown("""
    <style>
    /* =====================================================
       FORCE STREAMLIT BUTTON TEXT COLOR TO WHITE (FIX)
       ===================================================== */

    /* Target the actual container Streamlit uses for button labels */
    button div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Fallback: force all text inside buttons to white */
    button * {
        color: #ffffff !important;
    }

    /* Prevent hover/active states from reverting color */
    button:hover div[data-testid="stMarkdownContainer"] p,
    button:active div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* =====================================================
       EXISTING STYLES (UNCHANGED)
       ===================================================== */

    .purple-card p,
    .purple-card h1,
    .purple-card h2,
    .purple-card h3,
    .purple-card h4 {
        color: #ffffff !important;
    }

    h2, h3, p {
        color: #000000 !important;
    }

    /* Tabs should remain black */
    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<h1 style="color:#667eea;margin-top:0;">Vaccination Schedule</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="margin-bottom:1.5rem;">Track your child\'s vaccination schedule based on recommended guidelines</p>',
        unsafe_allow_html=True
    )

    children = db.get_all_children()
    if not children:
        st.info("Please add a child profile first to see vaccination schedule.")
        return

    if 'selected_child_id' not in st.session_state:
        st.session_state.selected_child_id = children[0]['id']

    child_options = {c['name']: c['id'] for c in children}

    selected_name = st.selectbox(
        "Select Child",
        options=list(child_options.keys()),
        index=list(child_options.values()).index(st.session_state.selected_child_id)
    )

    st.session_state.selected_child_id = child_options[selected_name]
    child = db.get_child(st.session_state.selected_child_id)
    vaccinations = db.get_vaccinations(st.session_state.selected_child_id)

    dob = child['date_of_birth']
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="purple-card" style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        padding:20px;border-radius:10px;text-align:center;">
            <p style="font-size:18px;font-weight:500;margin:0;">Age</p>
            <p style="font-size:32px;font-weight:700;margin-top:10px;">{get_age_string(dob)}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="purple-card" style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        padding:20px;border-radius:10px;text-align:center;">
            <p style="font-size:18px;font-weight:500;margin:0;">Guideline</p>
            <p style="font-size:32px;font-weight:700;margin-top:10px;">{child['country_guideline']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        completed = len([v for v in vaccinations if v['status'] == 'completed'])
        st.markdown(f"""
        <div class="purple-card" style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        padding:20px;border-radius:10px;text-align:center;">
            <p style="font-size:18px;font-weight:500;margin:0;">Completed</p>
            <p style="font-size:32px;font-weight:700;margin-top:10px;">{completed}/{len(vaccinations)}</p>
        </div>
        """, unsafe_allow_html=True)

    if not vaccinations:
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

    categories = categorize_vaccinations(vaccinations)

    tab1, tab2, tab3, tab4 = st.tabs(["Overdue", "Upcoming", "Pending", "Completed"])

    with tab1:
        if categories['overdue']:
            for vacc in categories['overdue']:
                render_vaccine_card(vacc, "overdue")
        else:
            st.success("No overdue vaccines")

    with tab2:
        if categories['upcoming']:
            for vacc in categories['upcoming']:
                render_vaccine_card(vacc, "upcoming")
        else:
            st.info("No upcoming vaccines")

    with tab3:
        if categories['pending']:
            for vacc in categories['pending']:
                render_vaccine_card(vacc, "pending")
        else:
            st.info("No future vaccines")

    with tab4:
        if categories['completed']:
            for vacc in categories['completed']:
                render_vaccine_card(vacc, "completed")
        else:
            st.info("No completed vaccines")


def render_vaccine_card(vacc, status_type):
    due_date = vacc['due_date']
    if isinstance(due_date, str):
        due_date = date.fromisoformat(due_date)

    days_diff = (due_date - date.today()).days

    if status_type == "overdue":
        bg, border, emoji, text = "#ffebee", "#f44336", "🔴", f"Overdue by {abs(days_diff)} days"
    elif status_type == "upcoming":
        bg, border, emoji, text = "#fff8e1", "#ff9800", "🟠", f"Due in {days_diff} days"
    elif status_type == "completed":
        bg, border, emoji, text = "#e8f5e9", "#4caf50", "✅", f"Completed"
    else:
        bg, border, emoji, text = "#e3f2fd", "#2196f3", "🔵", f"Due on {due_date.strftime('%d %B %Y')}"

    st.markdown(f"""
    <div style="background:{bg};padding:18px;border-radius:10px;border-left:6px solid {border};margin-bottom:12px;">
        <h4 style="margin:0;color:#000;">💉 {vacc['vaccine_name']}</h4>
        <p style="margin:6px 0;color:#000;">{emoji} {text}</p>
        <p style="margin:0;color:#666;font-size:0.85rem;">📅 {due_date.strftime('%A, %B %d, %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    if status_type != "completed":
        with col2:
            if st.button("✓ Mark Completed", key=f"done_{vacc['id']}", use_container_width=True):
                db.update_vaccination_status(vacc['id'], 'completed', date.today().isoformat())
                st.rerun()
    else:
        with col2:
            if st.button("↶ Mark Pending", key=f"undo_{vacc['id']}", use_container_width=True):
                db.update_vaccination_status(vacc['id'], 'pending', None)
                st.rerun()
