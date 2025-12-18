import streamlit as st

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #667eea; margin-bottom: 2rem; font-size: 1.8rem;">Create Account</h2>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name", placeholder="Your Name", key="signup_name")
        email = st.text_input("Email Address", placeholder="your@email.com", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="signup_confirm")
        
        st.checkbox("I agree to the Terms & Conditions", key="terms_agree", value=False)
        
        if st.button("Sign Up", key="signup_btn", use_container_width=True, type="primary"):
            if not name or not email or not password or not confirm_password:
                st.error("❌ Please fill all fields")
            elif password != confirm_password:
                st.error("❌ Passwords don't match")
            elif not st.session_state.get('terms_agree', False):
                st.error("❌ Please agree to Terms & Conditions")
            else:
                st.success("✅ Account created successfully! (Demo mode)")
                st.session_state.current_page = "Dashboard"
                st.rerun()
        
        st.divider()
        st.markdown('<p style="text-align: center; color: #888;">Already have an account? <strong style="color: #667eea;">Login</strong></p>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
