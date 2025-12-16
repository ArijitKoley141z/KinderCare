import streamlit as st
import plotly.graph_objects as go
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
    
    render_visual_timeline(schedule, guideline)
    
    st.markdown("---")
    
    render_timeline_by_age(schedule)
    
    st.markdown("---")
    
    render_vaccine_list(schedule)
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #117a8b; padding: 15px; border-radius: 5px; border-left: 4px solid #0c5460; color: white;">
        <strong>Note:</strong> This timeline shows the standard recommended vaccination schedule. 
        Actual timing may vary based on your child's health condition and your pediatrician's advice.
    </div>
    """, unsafe_allow_html=True)

def render_visual_timeline(schedule, guideline):
    st.subheader("Visual Timeline")
    
    fig = go.Figure()
    
    age_groups = {}
    for vacc in schedule:
        age_label = vacc['age_label']
        weeks = vacc['age_weeks']
        if age_label not in age_groups:
            age_groups[age_label] = {'weeks': weeks, 'vaccines': []}
        age_groups[age_label]['vaccines'].append(vacc['vaccine'])
    
    colors = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0', '#e91e63', '#00bcd4', '#8bc34a', '#ff5722']
    
    sorted_groups = sorted(age_groups.items(), key=lambda x: x[1]['weeks'])
    
    for i, (age_label, data) in enumerate(sorted_groups):
        weeks = data['weeks']
        months = weeks / 4.33
        vaccines = data['vaccines']
        
        color = colors[i % len(colors)]
        
        hover_text = f"<b>{age_label}</b><br>" + "<br>".join([f"• {v}" for v in vaccines])
        
        fig.add_trace(go.Scatter(
            x=[months],
            y=[0],
            mode='markers',
            marker=dict(size=25 + len(vaccines) * 3, color=color, symbol='circle'),
            name=age_label,
            showlegend=False,
            hovertemplate=hover_text + "<extra></extra>"
        ))
        
        fig.add_annotation(
            x=months,
            y=0.15 if i % 2 == 0 else -0.15,
            text=f"<b>{age_label}</b><br>({len(vaccines)} vaccines)",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor=color,
            font=dict(size=10),
            align='center'
        )
    
    fig.add_shape(
        type="line",
        x0=0, y0=0, x1=max([g[1]['weeks']/4.33 for g in sorted_groups]) + 5, y1=0,
        line=dict(color="#ddd", width=3)
    )
    
    fig.update_layout(
        height=350,
        margin=dict(t=80, b=80, l=40, r=40),
        xaxis_title="Age (Months)",
        yaxis=dict(visible=False, range=[-0.5, 0.5]),
        hovermode='closest',
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch')

def render_timeline_by_age(schedule):
    st.subheader("Vaccination Schedule by Age")
    
    age_groups = {}
    for vacc in schedule:
        age_label = vacc['age_label']
        weeks = vacc['age_weeks']
        if age_label not in age_groups:
            age_groups[age_label] = {'weeks': weeks, 'vaccines': []}
        age_groups[age_label]['vaccines'].append(vacc)
    
    sorted_groups = sorted(age_groups.items(), key=lambda x: x[1]['weeks'])
    
    colors = ['#4caf50', '#2196f3', '#ff9800', '#9c27b0', '#e91e63', '#00bcd4', '#8bc34a', '#ff5722']
    
    for i, (age_label, data) in enumerate(sorted_groups):
        vaccines = data['vaccines']
        color = colors[i % len(colors)]
        
        st.markdown(f"""
        <div style="display: flex; align-items: stretch; margin-bottom: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; margin-right: 15px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background-color: {color}; 
                            display: flex; align-items: center; justify-content: center; color: white; 
                            font-weight: bold; font-size: 12px;">
                    {len(vaccines)}
                </div>
                <div style="width: 3px; flex-grow: 1; background-color: {color}; min-height: 20px; opacity: 0.5;"></div>
            </div>
            <div style="flex-grow: 1; background-color: #f8f9fa; padding: 15px; border-radius: 8px; 
                        border-left: 4px solid {color}; margin-bottom: 15px;">
                <h4 style="margin: 0 0 10px 0; color: {color};">{age_label}</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """, unsafe_allow_html=True)
        
        vaccine_badges = ""
        for vacc in vaccines:
            vaccine_badges += f"""
                <span style="background-color: {color}; color: white; padding: 5px 12px; 
                             border-radius: 15px; font-size: 13px; display: inline-block; margin: 2px;">
                    {vacc['vaccine']}
                </span>
            """
        
        st.markdown(f"""
                    {vaccine_badges}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_vaccine_list(schedule):
    st.subheader("Complete Vaccine List")
    
    with st.expander("View All Vaccines with Details", expanded=False):
        for vacc in schedule:
            weeks = vacc['age_weeks']
            if weeks == 0:
                age_text = "At Birth"
            elif weeks < 52:
                age_text = f"{weeks} weeks"
            else:
                years = weeks // 52
                remaining_weeks = weeks % 52
                if remaining_weeks > 0:
                    age_text = f"{years} year(s) {remaining_weeks} weeks"
                else:
                    age_text = f"{years} year(s)"
            
            st.markdown(f"""
            **{vacc['vaccine']}** ({vacc['code']})
            - **Recommended Age:** {vacc['age_label']} (~{age_text})
            - **Description:** {vacc['description']}
            
            ---
            """)
