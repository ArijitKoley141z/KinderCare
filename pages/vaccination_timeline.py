import streamlit as st
from vaccination_guidelines import INDIA_UIP_SCHEDULE, WHO_SCHEDULE, CDC_SCHEDULE

def render():
    st.title("Vaccination Timeline")
    st.markdown("View the recommended vaccination schedule based on official guidelines.")
    
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
    
    total_vaccines = len(schedule)
    total_stages = len(sorted_groups)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Vaccines", total_vaccines)
    with col2:
        st.metric("Age Stages", total_stages)
    
    st.markdown("---")
    st.subheader("Vaccination Schedule")
    
    for i, (age_label, data) in enumerate(sorted_groups):
        vaccines = data['vaccines']
        
        if data['weeks'] == 0:
            color = "#e91e63"
            icon = "👶"
        elif data['weeks'] <= 14:
            color = "#9c27b0"
            icon = "🍼"
        elif data['weeks'] <= 52:
            color = "#2196f3"
            icon = "🧒"
        elif data['weeks'] <= 260:
            color = "#4caf50"
            icon = "👦"
        else:
            color = "#ff9800"
            icon = "🧑"
        
        vaccine_cards = ""
        for vacc in vaccines:
            vaccine_cards += f"""
                <div style="background-color: white; border: 2px solid {color}; border-radius: 8px; 
                            padding: 10px 15px; min-width: 200px; flex: 1;">
                    <div style="font-weight: bold; color: #333; margin-bottom: 5px;">
                        {vacc['name']}
                    </div>
                    <div style="font-size: 12px; color: #666;">
                        {vacc['description']}
                    </div>
                </div>
            """
        
        connector_line = f"<div style='width: 3px; height: 30px; background-color: {color}; opacity: 0.4;'></div>" if i < len(sorted_groups) - 1 else ""
        
        with st.container():
            st.markdown(f"""
            <div style="display: flex; margin-bottom: 20px;">
                <div style="display: flex; flex-direction: column; align-items: center; margin-right: 20px; min-width: 60px;">
                    <div style="width: 50px; height: 50px; border-radius: 50%; background-color: {color}; 
                                display: flex; align-items: center; justify-content: center; 
                                font-size: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                        {icon}
                    </div>
                    {connector_line}
                </div>
                <div style="flex-grow: 1; background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                            padding: 20px; border-radius: 12px; border-left: 5px solid {color}; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <h3 style="margin: 0 0 15px 0; color: {color}; font-size: 1.3rem;">
                        {age_label}
                    </h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                        {vaccine_cards}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #117a8b; padding: 15px; border-radius: 5px; border-left: 4px solid #0c5460; color: white;">
        <strong>Note:</strong> This timeline shows the standard recommended vaccination schedule. 
        Actual timing may vary based on your child's health condition and your pediatrician's advice.
    </div>
    """, unsafe_allow_html=True)
