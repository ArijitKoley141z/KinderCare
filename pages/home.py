import streamlit as st

def render():
    st.markdown("""
    <div class="hero">
        <h1>KinderCare</h1>
        <h2>Your Child's Health & Vaccination Companion</h2>
        <p>Track vaccinations, manage health records, and get instant answers from our AI assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-grid">
        <div class="card">
            <div class="card-gradient" style="--gradient-start: #667eea; --gradient-end: #764ba2;">
                <div class="card-icon">📊</div>
                <h3>Dashboard</h3>
                <p>View your child's health overview</p>
            </div>
        </div>
        <div class="card">
            <div class="card-gradient" style="--gradient-start: #f093fb; --gradient-end: #f5576c;">
                <div class="card-icon">💉</div>
                <h3>Vaccinations</h3>
                <p>Track vaccine schedules and timelines</p>
            </div>
        </div>
        <div class="card">
            <div class="card-gradient" style="--gradient-start: #4facfe; --gradient-end: #00f2fe;">
                <div class="card-icon">🤖</div>
                <h3>AI Assistant</h3>
                <p>Ask health and vaccine questions</p>
            </div>
        </div>
        <div class="card">
            <div class="card-gradient" style="--gradient-start: #fa709a; --gradient-end: #fee140;">
                <div class="card-icon">📅</div>
                <h3>Health Timeline</h3>
                <p>Record health events and milestones</p>
            </div>
        </div>
        <div class="card">
            <div class="card-gradient" style="--gradient-start: #30cfd0; --gradient-end: #330867;">
                <div class="card-icon">🏥</div>
                <h3>Diseases & Remedies</h3>
                <p>Learn about common childhood illnesses</p>
            </div>
        </div>
        <div class="card">
            <div class="card-gradient" style="--gradient-start: #a8edea; --gradient-end: #fed6e3;">
                <div class="card-icon">📈</div>
                <h3>Timeline</h3>
                <p>Visualize your child's vaccination progress</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>Welcome to KinderCare</h3>
        <p>This application helps you keep track of your child's vaccinations and health. Use the navigation bar at the top to explore different features. Our AI Health Assistant is always ready to answer your questions about child health and vaccinations.</p>
    </div>
    """, unsafe_allow_html=True)
