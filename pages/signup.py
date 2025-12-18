import streamlit as st

def render():
    st.markdown("""
    <div class="form-container">
        <h2 style="text-align: center; color: #667eea; margin-bottom: 2rem;">Create Account</h2>
    """, unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="Your Name", key="signup_name")
    email = st.text_input("Email Address", placeholder="your@email.com", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="signup_confirm")
    
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
