import streamlit as st

def render():
    st.markdown("""
    <style>
        /* Improve text input styling */
        [data-testid="stTextInput"] input {
            font-size: 1rem !important;
            padding: 10px 12px !important;
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
            outline: none !important;
        }
        /* Improve checkbox styling */
        [data-testid="stCheckbox"] {
            color: #333 !important;
        }
        /* Style buttons */
        [data-testid="baseButton-primary"] {
            font-weight: 600 !important;
            font-size: 1.05em !important;
            border-radius: 8px !important;
        }
        [data-testid="baseButton-secondary"] {
            font-weight: 600 !important;
            font-size: 1.05em !important;
            border-radius: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #667eea; font-size: 2rem; margin: 0; font-weight: 800;">Create Account</h1>
            <p style="color: #999; margin-top: 0.5rem; font-size: 1.05rem;">Join KinderCare to track your child's health</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.12); border-top: 4px solid #667eea;">', unsafe_allow_html=True)
        
        name = st.text_input("👤 Full Name", placeholder="Your Full Name", key="signup_name")
        email = st.text_input("📧 Email Address", placeholder="your@email.com", key="signup_email")
        password = st.text_input("🔐 Password", type="password", placeholder="Create a strong password", key="signup_password")
        confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Re-enter your password", key="signup_confirm")
        
        col_terms, col_space = st.columns([5, 1])
        with col_terms:
            agree_terms = st.checkbox("I agree to the Terms & Conditions", key="terms_agree", value=False)
        
        if st.button("✍️ Create Account", key="signup_btn", use_container_width=True, type="primary"):
            if not name or not email or not password or not confirm_password:
                st.error("❌ Please fill all fields")
            elif password != confirm_password:
                st.error("❌ Passwords don't match")
            elif not agree_terms:
                st.error("❌ Please agree to Terms & Conditions")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long")
            else:
                st.success("✅ Account created successfully!")
                st.session_state.current_page = "Home"
                st.rerun()
        
        st.markdown("---")
        
        col_text, col_btn = st.columns([2, 1])
        with col_text:
            st.markdown('<p style="color: #888; margin: 0;">Already have an account?</p>', unsafe_allow_html=True)
        with col_btn:
            if st.button("Login", key="switch_to_login", use_container_width=True, type="secondary"):
                st.session_state.current_page = "Login"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
