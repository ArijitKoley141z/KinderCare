import streamlit as st

def render():
    st.markdown("""
    <div style="padding: 2rem 0;">
        <p style="font-size: 1rem; color: #666; line-height: 1.8;">
            This application helps you keep track of your child's vaccinations and health. Use the navigation buttons at the top to explore different features. Our AI Health Assistant is always ready to answer your questions about child health and vaccinations.
        </p>
    </div>
    """, unsafe_allow_html=True)
