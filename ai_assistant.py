
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def chat_with_assistant(user_input: str) -> str:
    

    if not user_input or not user_input.strip():
        return "Please enter a question."

    # Cloud-safe fallback
    if not OPENAI_AVAILABLE:
        return (
            "⚠️ AI assistant is disabled in the deployed version.\n\n"
            "Reason: OpenAI dependency is not available on free hosting.\n\n"
            "You can still view vaccination schedules, disease information, "
            "and health timelines."
        )

    # Local OpenAI usage
    try:
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a pediatric healthcare assistant. "
                        "Provide safe, non-diagnostic advice. "
                        "Always recommend consulting a doctor for serious symptoms."
                    )
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.4
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI error occurred: {str(e)}"


def get_quick_responses():
    """
    Predefined quick-help buttons (cloud & local safe)
    """
    return {
        "Next vaccine due": "When is my child's next vaccination due?",
        "Common cold care": "What should I do if my child has a common cold?",
        "Fever guidance": "What should I do if my child has a fever?",
        "Doctor visit": "When should I take my child to a doctor?"
    }


def transcribe_audio(_audio_bytes):
    
    return "🎙️ Voice input is planned for a future version."
