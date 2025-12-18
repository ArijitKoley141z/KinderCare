import streamlit as st
from vaccination_guidelines import INDIA_UIP_SCHEDULE, WHO_SCHEDULE, CDC_SCHEDULE

def render():
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">Vaccination Timeline</h1>', unsafe_allow_html=True)
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
        vaccine_count = len(vaccines)
        vaccine_text = "vaccine" if vaccine_count == 1 else "vaccines"
        
        with st.expander(f"**{age_label}** — {vaccine_count} {vaccine_text}", expanded=False):
            for vacc in vaccines:
                st.markdown(f"""
                <div style="background-color: #667eea; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px; color: white;">
                    <div style="font-weight: bold; font-size: 16px; margin-bottom: 4px;">
                        💉 {vacc['name']}
                    </div>
                    <div style="font-size: 14px; opacity: 0.95;">
                        {vacc['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <h3>Important</h3>
        <p>This timeline shows the standard recommended vaccination schedule. Always consult your pediatrician for advice specific to your child's health needs.</p>
    </div>
    """, unsafe_allow_html=True)
