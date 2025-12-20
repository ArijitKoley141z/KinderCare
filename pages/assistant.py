import streamlit as st
import os
import tempfile
from datetime import date
import database as db
from ai_assistant import chat_with_assistant, transcribe_audio, get_quick_responses

def process_user_message(user_input, child, vaccinations, health_events):
    if not child:
        st.warning("Please select a child first")
        return
    
    response = chat_with_assistant(user_input, child, vaccinations, health_events)
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.session_state.conversation_history.append({"role": "assistant", "content": response})

def render():
    st.markdown("""
    <style>
        h2, h3 {
            color: #1a1a1a !important;
        }
        p {
            color: #000 !important;
        }
        button, [data-testid="baseButton-primary"], [data-testid="baseButton-secondary"] {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: #667eea; margin-top: 0;">🤖 Health Assistant</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
        <h3 style="color: white; margin-top: 0;">AI Health Assistant</h3>
        <p style="color: white; margin: 0;">Ask questions about your child's vaccination schedule, health concerns, or get general guidance. I understand natural language - just ask as you would ask a friend!</p>
    </div>
    """, unsafe_allow_html=True)
    
    children = db.get_all_children()
    
    if not children:
        st.warning("Please add a child profile to use the assistant effectively.")
        child = None
        vaccinations = []
        health_events = []
    else:
        if 'selected_child_id' not in st.session_state or st.session_state.selected_child_id is None:
            st.session_state.selected_child_id = children[0]['id']
        
        child_options = {c['name']: c['id'] for c in children}
        selected_name = st.selectbox(
            "Select Child",
            options=list(child_options.keys()),
            index=list(child_options.values()).index(st.session_state.selected_child_id) 
                  if st.session_state.selected_child_id in child_options.values() else 0,
            key="assistant_child_select"
        )
        st.session_state.selected_child_id = child_options[selected_name]
        
        child = db.get_child(st.session_state.selected_child_id)
        vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
        health_events = db.get_health_events(st.session_state.selected_child_id)
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    st.markdown("---")
    
    st.markdown('<h2 style="color: #1a1a1a; margin-top: 0; margin-bottom: 1rem; font-weight: 700;">💡 Quick Questions</h2>', unsafe_allow_html=True)
    quick_responses = get_quick_responses()
    
    cols = st.columns(3)
    for idx, qr in enumerate(quick_responses):
        with cols[idx % 3]:
            if st.button(qr['label'], key=f"quick_{idx}", width='stretch'):
                process_user_message(qr['query'], child, vaccinations, health_events)
                st.rerun()
    
    st.markdown("---")
    
    st.markdown('<h2 style="color: #1a1a1a; margin-top: 0; margin-bottom: 1rem; font-weight: 700;">💬 Chat</h2>', unsafe_allow_html=True)
    
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.conversation_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style="background-color: #667eea; padding: 12px 15px; border-radius: 15px; 
                            margin: 10px 0; margin-left: 20%; text-align: right; color: white;">
                    <strong>You:</strong> {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #e8e8e8; padding: 12px 15px; border-radius: 15px; 
                            margin: 10px 0; margin-right: 20%; color: #333;">
                    <strong>Assistant:</strong><br>{msg['content']}
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Type your message",
            placeholder="e.g., When is my child's next vaccine due?",
            key="user_message_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", width='stretch')
    
    if send_button and user_input:
        process_user_message(user_input, child, vaccinations, health_events)
        st.rerun()
