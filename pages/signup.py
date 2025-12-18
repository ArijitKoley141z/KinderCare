import streamlit as st

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <h1 style="text-align: center; color: #667eea; margin: 0 0 2rem 0; font-size: 2rem;">
                Create Account
            </h1>
        """, unsafe_allow_html=True)
        
        name = st.text_input("Full Name", placeholder="Your Name")
        email = st.text_input("Email Address", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        st.checkbox("I agree to the Terms & Conditions", key="terms_agree")
        
        if st.button("Sign Up", key="signup_btn", use_container_width=True, type="primary"):
            if not name or not email or not password or not confirm_password:
                st.error("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords don't match")
            else:
                st.success("Account created successfully! (Demo mode)")
                st.session_state.current_page = "Dashboard"
                st.rerun()
        
        st.markdown("---")
        st.markdown('<div style="text-align: center; color: #666;">Already have an account? <a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">Login</a></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
