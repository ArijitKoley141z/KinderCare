import streamlit as st

def render():
    st.markdown("""
    <div class="form-container">
        <h2 style="text-align: center; color: #667eea; margin-bottom: 2rem;">Welcome Back</h2>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Email Address", placeholder="your@email.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
    
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Remember me", key="remember_login")
    with col2:
        st.markdown('<a href="#" style="text-align: right; color: #667eea; text-decoration: none;">Forgot Password?</a>', unsafe_allow_html=True)
    
    if st.button("Login", key="login_btn", use_container_width=True, type="primary"):
        if email and password:
            st.success("Login successful! (Demo mode)")
            st.session_state.current_page = "Dashboard"
            st.rerun()
        else:
            st.error("Please enter both email and password")
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #666;">Don\'t have an account? <a href="#" onclick="document.querySelector(\'[data-testid=stButton]:has(>button:contains(\"Sign Up\")))\').click()" style="color: #667eea; text-decoration: none; font-weight: 600;">Sign Up</a></div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
