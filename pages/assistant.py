import streamlit as st
from ai_assistant import chat_with_history, get_quick_responses

def render():
    st.markdown("## 🤖 KinderCare AI Assistant")
    st.markdown("Ask me anything about your child's health, vaccinations, or general wellness.")
    st.markdown("---")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Quick suggestion buttons
    st.markdown("**💡 Quick Questions — click to ask:**")
    quick = get_quick_responses()
    col1, col2 = st.columns(2)
    for i, question in enumerate(quick):
        col = col1 if i % 2 == 0 else col2
        if col.button(question, key=f"quick_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("KinderCare AI is thinking..."):
                reply = chat_with_history(st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("---")

    # Display conversation history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box at bottom
    user_input = st.chat_input("Ask KinderCare AI anything about your child's health...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chat_with_history(st.session_state.chat_history)
            st.markdown(reply)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    # Clear chat button
    if st.session_state.chat_history:
        st.markdown("---")
        if st.button("🗑️ Clear Conversation", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
    render()

# Call render if this is the main page
render()
