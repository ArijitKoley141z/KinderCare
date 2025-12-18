import streamlit as st

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <h1 style="text-align: center; color: #667eea; margin: 0 0 2rem 0; font-size: 2rem;">
                Welcome Back
            </h1>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_remember, col_forgot = st.columns([1, 1])
        with col_remember:
            st.checkbox("Remember me", key="remember_login")
        with col_forgot:
            st.markdown('<a href="#" style="text-align: right; color: #667eea; text-decoration: none;">Forgot Password?</a>', unsafe_allow_html=True)
        
        if st.button("Login", key="login_btn", use_container_width=True, type="primary"):
            if email and password:
                st.success("Login successful! (Demo mode)")
                st.session_state.current_page = "Dashboard"
                st.rerun()
            else:
                st.error("Please enter both email and password")
        
        st.markdown("---")
        st.markdown('<div style="text-align: center; color: #666;">Don\'t have an account? <a href="#" style="color: #667eea; text-decoration: none; font-weight: 600;">Sign Up</a></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
