import streamlit as st

def render():
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem;">
        <h1 style="font-size: 3.5rem; font-weight: 800; margin: 0; line-height: 1.1;">
            <span style="color: #1e88e5;">Smart Child</span>
        </h1>
        <h2 style="font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0; line-height: 1.2;">
            <span style="color: #43a047;">Vaccination</span> &
            <span style="color: #ff7043;">Health Assistant</span>
        </h2>
        <p style="font-size: 1.2rem; color: #666; margin: 1.5rem 0; max-width: 600px; margin-left: auto; margin-right: auto;">
            Your trusted companion for child health and vaccination management
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">Dashboard</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">View your child's health overview</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💉</div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">Vaccinations</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Track vaccine schedules and timelines</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">AI Assistant</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Ask health and vaccine questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📅</div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">Health Timeline</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Record health events and milestones</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🏥</div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">Diseases & Remedies</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Learn about common childhood illnesses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 180px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚙️</div>
            <h3 style="margin: 0; font-size: 1.3rem; font-weight: 700;">Settings</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Manage your profile and preferences</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background-color: #f0f7ff; padding: 2rem; border-radius: 12px; border-left: 5px solid #1e88e5; text-align: center;">
        <h3 style="margin: 0 0 0.5rem 0; color: #1e88e5;">Welcome!</h3>
        <p style="margin: 0; color: #333; line-height: 1.6;">
            This application helps you keep track of your child's vaccinations and health. Use the navigation buttons at the top to explore different features. Our AI Health Assistant is always ready to answer your questions about child health and vaccinations.
        </p>
    </div>
    """, unsafe_allow_html=True)
