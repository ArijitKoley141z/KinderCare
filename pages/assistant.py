import streamlit as st
import database as db
from ai_assistant import (
    chat_with_assistant,
    transcribe_audio,
    get_quick_responses
)


st.set_page_config(page_title="AI Assistant", layout="wide")



def process_user_message(user_input, child):
    if not user_input or not user_input.strip():
        return

    response = chat_with_assistant(user_input)

    st.session_state.conversation_history.append(
        {"role": "user", "content": user_input}
    )
    st.session_state.conversation_history.append(
        {"role": "assistant", "content": response}
    )



def render():
    # ---------- Styling ----------
    st.markdown("""
    <style>
        h2, h3 { color: #1a1a1a !important; }
        p { color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<h1 style="color:#667eea;margin-top:0;">🤖 KinderCare Health Assistant</h1>',
        unsafe_allow_html=True
    )

    st.info(
        "This assistant provides general health guidance only and does not "
        "replace professional medical consultation."
    )

   
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    
    user_id = st.session_state.get("user_id")
    children = db.get_all_children(user_id=user_id) if user_id else []

    if not children:
        st.warning("Please add a child profile to use the AI assistant.")
        st.stop()

   
    if "selected_child_id" not in st.session_state or st.session_state.selected_child_id is None:
        st.session_state.selected_child_id = children[0]["id"]

    child_options = {c["name"]: c["id"] for c in children}

    selected_name = st.selectbox(
        "Select Child",
        options=list(child_options.keys()),
        index=list(child_options.values()).index(
            st.session_state.selected_child_id
        ) if st.session_state.selected_child_id in child_options.values() else 0,
        key="assistant_select_child"
    )

    st.session_state.selected_child_id = child_options[selected_name]

    
    child_id = st.session_state.get("selected_child_id")
    if child_id is None:
        st.info("Please select a child to continue.")
        st.stop()

    child = db.get_child(child_id)
    vaccinations = db.get_vaccinations(child_id)
    health_events = db.get_health_events(child_id)

    
    st.markdown("---")
    st.markdown("<h2>💡 Quick Questions</h2>", unsafe_allow_html=True)

    quick_responses = get_quick_responses()
    cols = st.columns(3)

    for idx, (label, query) in enumerate(quick_responses.items()):
        with cols[idx % 3]:
            if st.button(label, key=f"assistant_quick_{idx}", use_container_width=True):
                process_user_message(query, child)
                st.rerun()

    
    st.markdown("---")
    st.markdown("<h2>💬 Chat</h2>", unsafe_allow_html=True)

    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="background:#667eea;color:white;padding:12px 15px;
                        border-radius:15px;margin:10px 0;margin-left:20%;
                        text-align:right;">
                <strong>You:</strong> {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:#e8e8e8;color:#333;padding:12px 15px;
                        border-radius:15px;margin:10px 0;margin-right:20%;">
                <strong>Assistant:</strong><br>{msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    # ---------- Input ----------
    st.markdown("---")
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input(
            "Type your message",
            placeholder="e.g., When is my child's next vaccine due?",
            label_visibility="collapsed",
            key="assistant_user_input"
        )

    with col2:
        send = st.button("Send", type="primary", use_container_width=True)

    if send and user_input:
        process_user_message(user_input, child)
        st.rerun()



render()
