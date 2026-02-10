import streamlit as st
import database as db
from ai_assistant import chat_with_assistant, transcribe_audio, get_quick_responses


def process_user_message(user_input, child, vaccinations, health_events):
    if not user_input or not user_input.strip():
        return

    if not child:
        st.warning("Please select a child first.")
        return

    response = chat_with_assistant(user_input)

    st.session_state.conversation_history.append(
        {"role": "user", "content": user_input}
    )
    st.session_state.conversation_history.append(
        {"role": "assistant", "content": response}
    )


def render():
    # ---------- Page styling ----------
    st.markdown("""
    <style>
        h2, h3 { color: #1a1a1a !important; }
        p { color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<h1 style="color:#667eea;margin-top:0;">🤖 Health Assistant</h1>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
        <h3 style="color:white;margin-top:0;">AI Health Assistant</h3>
        <p style="margin:0;">
            Ask questions about your child's vaccination schedule or health concerns.
            This assistant provides general guidance only.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Load children ----------
    user_id = st.session_state.get("user_id")
    children = db.get_all_children(user_id=user_id) if user_id else []

    child = None
    vaccinations = []
    health_events = []

    if children:
        if "selected_child_id" not in st.session_state:
            st.session_state.selected_child_id = children[0]["id"]

        child_options = {c["name"]: c["id"] for c in children}

        selected_name = st.selectbox(
            "Select Child",
            options=list(child_options.keys()),
            index=list(child_options.values()).index(
                st.session_state.selected_child_id
            ) if st.session_state.selected_child_id in child_options.values() else 0,
            key="assistant_child_select"
        )

        st.session_state.selected_child_id = child_options[selected_name]

        child = db.get_child(st.session_state.selected_child_id)
        vaccinations = db.get_vaccinations(st.session_state.selected_child_id)
        health_events = db.get_health_events(st.session_state.selected_child_id)
    else:
        st.warning("Please add a child profile to use the assistant.")

    # ---------- Conversation state ----------
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # ---------- Quick questions ----------
    st.markdown("---")
    st.markdown(
        '<h2 style="margin-bottom:1rem;">💡 Quick Questions</h2>',
        unsafe_allow_html=True
    )

    quick_responses = get_quick_responses()
    cols = st.columns(3)

    for idx, (label, query) in enumerate(quick_responses.items()):
        with cols[idx % 3]:
            if st.button(label, key=f"quick_{idx}", use_container_width=True):
                process_user_message(query, child, vaccinations, health_events)
                st.rerun()

    # ---------- Chat history ----------
    st.markdown("---")
    st.markdown(
        '<h2 style="margin-bottom:1rem;">💬 Chat</h2>',
        unsafe_allow_html=True
    )

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
        process_user_message(user_input, child, vaccinations, health_events)
        st.rerun()



render()
