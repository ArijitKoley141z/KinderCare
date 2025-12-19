import streamlit as st

def render():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #667eea; font-size: 2rem; margin: 0;">Welcome Back</h1>
            <p style="color: #999; margin-top: 0.5rem;">Sign in to your KinderCare account</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        
        email = st.text_input("📧 Email Address", placeholder="your@email.com", key="login_email")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter your password", key="login_password")
        
        col_remember, col_forgot = st.columns([1, 1])
        with col_remember:
            st.checkbox("Remember me", key="remember_login", value=False)
        with col_forgot:
            st.markdown('<p style="text-align: right; color: #667eea; cursor: pointer; margin: 0;">🔗 Forgot Password?</p>', unsafe_allow_html=True)
        
        if st.button("🔓 Login", key="login_btn", use_container_width=True, type="primary"):
            if email and password:
                st.success("✅ Login successful!")
                st.session_state.current_page = "Home"
                st.rerun()
            else:
                st.error("❌ Please enter both email and password")
        
        st.markdown("---")
        
        col_text, col_btn = st.columns([2, 1])
        with col_text:
            st.markdown('<p style="color: #888; margin: 0;">Don\'t have an account?</p>', unsafe_allow_html=True)
        with col_btn:
            if st.button("Sign Up", key="switch_to_signup", use_container_width=True, type="secondary"):
                st.session_state.current_page = "Sign Up"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
