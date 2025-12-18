import streamlit as st

def render():
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 0; margin: 0 -2rem 2rem -2rem; padding-left: 2rem; padding-right: 2rem; background-color: #f8f9ff;">
        <div style="font-size: 1.5rem; font-weight: 700; color: #1e88e5;">
            💉 Smart Child
        </div>
        <div style="display: flex; gap: 2rem; align-items: center; font-size: 0.95rem;">
            <a href="#" style="text-decoration: none; color: #333; font-weight: 500;">Home</a>
            <a href="#" style="text-decoration: none; color: #666;">Features</a>
            <a href="#" style="text-decoration: none; color: #666;">About Us</a>
            <button style="background-color: #1e88e5; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 20px; cursor: pointer; font-weight: 600;">Log In</button>
            <button style="background-color: #43a047; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 20px; cursor: pointer; font-weight: 600;">Sign Up</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin: 0 0 1.5rem 0; color: #1a1a1a;">
                Smart Child Vaccination & Health Assistant
            </h1>
            
            <p style="font-size: 1.1rem; color: #555; line-height: 1.6; margin: 0 0 2rem 0; max-width: 450px;">
                Complete health and vaccination management for your child. Track vaccines, monitor health milestones, and get instant answers to your parenting questions from our AI Health Assistant.
            </p>
            
            <div style="display: flex; gap: 1rem;">
                <button style="background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%); color: white; border: none; padding: 0.8rem 1.8rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 1rem; box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);">
                    Get Started
                </button>
                <button style="background-color: transparent; color: #1e88e5; border: 2px solid #1e88e5; padding: 0.8rem 1.8rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 1rem;">
                    Learn More
                </button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; min-height: 400px;">
            <div style="background: linear-gradient(135deg, rgba(30, 136, 229, 0.1) 0%, rgba(67, 160, 71, 0.1) 100%); border-radius: 20px; padding: 2rem; text-align: center; position: relative; overflow: hidden;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">
                    👨‍👩‍👧‍👦
                </div>
                <div style="font-size: 3rem; margin-bottom: 1rem;">
                    💉 ❤️ 📅
                </div>
                <div style="font-size: 3rem;">
                    🤖 📊 🏥
                </div>
                <div style="position: absolute; top: -50px; right: -50px; width: 150px; height: 150px; background: rgba(30, 136, 229, 0.05); border-radius: 50%; "></div>
                <div style="position: absolute; bottom: -30px; left: -30px; width: 100px; height: 100px; background: rgba(67, 160, 71, 0.05); border-radius: 50%; "></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("")
    
    st.markdown("""
    <h2 style="text-align: center; font-size: 2rem; font-weight: 700; margin: 2rem 0 3rem 0; color: #1a1a1a;">
        Key Features
    </h2>
    """, unsafe_allow_html=True)
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Health Dashboard</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.95;">Track your child's health and growth in one place</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 20px rgba(245, 87, 108, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">💉</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Vaccination Schedule</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.95;">Never miss a vaccine with personalized reminders</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 20px rgba(79, 172, 254, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🤖</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">AI Assistant</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.95;">Get instant answers to your health questions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    
    with feat_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 20px rgba(250, 112, 154, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📅</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Health Timeline</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.95;">Record and track health events and milestones</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 20px rgba(48, 207, 208, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏥</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Health Resources</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.95;">Learn about diseases and home remedies</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; min-height: 200px; display: flex; flex-direction: column; justify-content: center; box-shadow: 0 8px 20px rgba(168, 237, 234, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">📈</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Vaccination Timeline</h3>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.95;">Visualize your child's vaccination progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; border-radius: 16px; text-align: center; color: white; margin: 2rem 0;">
        <h2 style="margin: 0 0 1rem 0; font-size: 2rem; font-weight: 700;">Ready to Get Started?</h2>
        <p style="margin: 0 0 1.5rem 0; font-size: 1.1rem; opacity: 0.95;">Start tracking your child's health and vaccinations today</p>
        <button style="background-color: white; color: #667eea; border: none; padding: 0.8rem 2rem; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 1rem; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);">
            Begin Now
        </button>
    </div>
    """, unsafe_allow_html=True)
