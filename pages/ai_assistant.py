import streamlit as st
from datetime import date
import os
import json

# Project imports
from database import get_child, get_vaccinations
from vaccination_guidelines import categorize_vaccinations, get_age_string

# AI assistant imports
from kindercare_ai.ai_assistant import get_ai_response
from kindercare_ai.voice_input import render_voice_input


def load_disease_data():
    """Load disease database for AI context."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(
        BASE_DIR,
        "data",
        "disease_information_database.json"
    )

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_child_context(child_id):
    """Prepare child-specific context for AI assistant."""
    child = get_child(child_id)
    vaccinations = get_vaccinations(child_id)
    categories = categorize_vaccinations(vaccinations)

    dob = child["date_of_birth"]
    if isinstance(dob, str):
        dob = date.fromisoformat(dob)

    return {
        "name": child["name"],
        "age": get_age_string(dob),
        "upcoming_vaccines": [
            v["vaccine_name"] for v in categories["upcoming"]
        ],
        "overdue_vaccines": [
            v["vaccine_name"] for v in categories["overdue"]
        ],
        "completed_vaccines_count": len(categories["completed"])
    }


def render():
    st.markdown(
        '<h1 style="color:#667eea;margin-top:0;">🤖 AI Health Assistant</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="color:#000;">Ask questions about vaccinations, child health, or common diseases.</p>',
        unsafe_allow_html=True
    )

    # Ensure a child is selected
    if "selected_child_id" not in st.session_state:
        st.info("Please select a child profile to use the AI assistant.")
        return

    child_id = st.session_state.selected_child_id

    # Build contexts
    child_context = build_child_context(child_id)
    disease_context = load_disease_data()

    # Initialize chat history
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    # Display chat history
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Voice input (optional)
    audio_bytes = render_voice_input()

    user_input = st.chat_input("Ask a question about your child’s health or vaccinations")

    # Prefer voice input if present
    if audio_bytes:
        user_input = "User asked via voice input"

    if user_input:
        # Show user message
        st.session_state.ai_messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.write(user_input)

        # Get AI response
        with st.spinner("AI is thinking..."):
            response = get_ai_response(
                user_input=user_input,
                child_context=child_context,
                disease_context=disease_context
            )

        # Show assistant response
        st.session_state.ai_messages.append(
            {"role": "assistant", "content": response}
        )
        with st.chat_message("assistant"):
            st.write(response)

    st.markdown("---")
    st.markdown(
        """
        <small style="color:#666;">
        ⚠️ This AI assistant provides general health information only and does not replace professional medical advice.
        </small>
        """,
        unsafe_allow_html=True
    )
render()
