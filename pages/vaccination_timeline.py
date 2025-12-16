import streamlit as st
from vaccination_guidelines import INDIA_UIP_SCHEDULE, WHO_SCHEDULE, CDC_SCHEDULE

def render():
    st.title("Vaccination Timeline")
    st.markdown("A simple guide showing when your child needs each vaccine.")
    
    guideline = st.selectbox(
        "Select Vaccination Guideline",
        ["India (UIP)", "WHO", "CDC (USA)"],
        help="Choose the vaccination guideline to view the recommended schedule"
    )
    
    if guideline == "India (UIP)":
        schedule = INDIA_UIP_SCHEDULE
        guideline_info = "Universal Immunization Programme - Government of India"
    elif guideline == "WHO":
        schedule = WHO_SCHEDULE
        guideline_info = "World Health Organization Recommendations"
    else:
        schedule = CDC_SCHEDULE
        guideline_info = "Centers for Disease Control and Prevention (USA)"
    
    st.info(f"**{guideline}**: {guideline_info}")
    
    st.markdown("---")
    
    age_groups = {}
    for vacc in schedule:
        age_label = vacc['age_label']
        weeks = vacc['age_weeks']
        if age_label not in age_groups:
            age_groups[age_label] = {'weeks': weeks, 'vaccines': []}
        age_groups[age_label]['vaccines'].append({
            'name': vacc['vaccine'],
            'description': vacc['description']
        })
    
    sorted_groups = sorted(age_groups.items(), key=lambda x: x[1]['weeks'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Vaccines", len(schedule))
    with col2:
        st.metric("Age Stages", len(sorted_groups))
    
    st.markdown("---")
    st.subheader("When to Vaccinate Your Child")
    
    for age_label, data in sorted_groups:
        vaccines = data['vaccines']
        weeks = data['weeks']
        
        if weeks == 0:
            stage_icon = "👶"
            stage_color = "#e91e63"
        elif weeks <= 14:
            stage_icon = "🍼"
            stage_color = "#9c27b0"
        elif weeks <= 52:
            stage_icon = "🧒"
            stage_color = "#2196f3"
        elif weeks <= 260:
            stage_icon = "👦"
            stage_color = "#4caf50"
        else:
            stage_icon = "🧑"
            stage_color = "#ff9800"
        
        vaccine_count = len(vaccines)
        vaccine_text = "vaccine" if vaccine_count == 1 else "vaccines"
        
        with st.expander(f"{stage_icon} **{age_label}** — {vaccine_count} {vaccine_text}", expanded=False):
            for vacc in vaccines:
                st.markdown(f"""
                <div style="background-color: {stage_color}; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; color: white;">
                    <div style="font-weight: bold; font-size: 16px; margin-bottom: 4px;">
                        💉 {vacc['name']}
                    </div>
                    <div style="font-size: 14px; opacity: 0.95;">
                        {vacc['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("Quick Reference Table")
    
    table_rows = ""
    for age_label, data in sorted_groups:
        vaccine_names = ", ".join([v['name'] for v in data['vaccines']])
        table_rows += f"<tr><td style='padding: 10px; border: 1px solid #ddd; font-weight: bold;'>{age_label}</td><td style='padding: 10px; border: 1px solid #ddd;'>{vaccine_names}</td></tr>"
    
    st.markdown(f"""
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
        <thead>
            <tr style="background-color: #1e88e5; color: white;">
                <th style="padding: 12px; text-align: left; border: 1px solid #1565c0;">Age</th>
                <th style="padding: 12px; text-align: left; border: 1px solid #1565c0;">Vaccines</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #117a8b; padding: 15px; border-radius: 8px; color: white;">
        <strong>Important:</strong> This timeline shows the standard recommended vaccination schedule. 
        Always consult your pediatrician for advice specific to your child's health needs.
    </div>
    """, unsafe_allow_html=True)
