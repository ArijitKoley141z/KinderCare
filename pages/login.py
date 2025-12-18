import streamlit as st

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #667eea; margin-bottom: 2rem; font-size: 1.8rem;">Welcome Back</h2>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="your@email.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        col_remember, col_forgot = st.columns([1, 1])
        with col_remember:
            st.checkbox("Remember me", key="remember_login", value=False)
        with col_forgot:
            st.caption("🔗 Forgot Password?")
        
        if st.button("Login", key="login_btn", use_container_width=True, type="primary"):
            if email and password:
                st.success("✅ Login successful! (Demo mode)")
                st.session_state.current_page = "Dashboard"
                st.rerun()
            else:
                st.error("❌ Please enter both email and password")
        
        st.divider()
        st.markdown('<p style="text-align: center; color: #888;">Don\'t have an account? <strong style="color: #667eea;">Sign Up</strong></p>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
