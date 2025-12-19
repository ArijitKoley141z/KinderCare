import streamlit as st

def render():
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1rem;">
        <h1 style="font-size: 2.5rem; font-weight: 800; color: #667eea; margin-bottom: 1rem;">
            KinderCare
        </h1>
        <h2 style="font-size: 1.5rem; font-weight: 600; color: #333; margin-bottom: 1.5rem;">
            Your Child's Health & Vaccination Companion
        </h2>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem; line-height: 1.6;">
            Track vaccinations, manage health records, and get instant answers from our AI assistant
        </p>
        <p style="font-size: 1rem; color: #666; line-height: 1.8;">
            This application helps you keep track of your child's vaccinations and health. Use the navigation buttons at the top to explore different features. Our AI Health Assistant is always ready to answer your questions about child health and vaccinations.
        </p>
    </div>
    """, unsafe_allow_html=True)
