import os
import json
from datetime import date, datetime
from typing import Optional, List, Dict
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def get_openai_client():
    if not OPENAI_API_KEY:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)

def format_child_context(child: Dict, vaccinations: List[Dict], health_events: List[Dict]) -> str:
    if not child:
        return "No child profile is currently selected."
    
    dob = child.get('date_of_birth', 'Unknown')
    if isinstance(dob, str):
        try:
            dob_date = date.fromisoformat(dob)
            from vaccination_guidelines import get_age_string
            age = get_age_string(dob_date)
        except:
            age = "Unknown"
    else:
        from vaccination_guidelines import get_age_string
        age = get_age_string(dob)
    
    context = f"""
Child Information:
- Name: {child.get('name', 'Unknown')}
- Date of Birth: {dob}
- Age: {age}
- Vaccination Guideline: {child.get('country_guideline', 'WHO')}
- Gender: {child.get('gender', 'Not specified')}
- Blood Group: {child.get('blood_group', 'Not specified')}
- Known Allergies: {child.get('allergies', 'None recorded')}

Vaccination Status:
"""
    
    today = date.today()
    overdue = []
    upcoming = []
    completed = []
    
    for vacc in vaccinations:
        due_date = vacc.get('due_date')
        if isinstance(due_date, str):
            due_date = date.fromisoformat(due_date)
        
        if vacc.get('status') == 'completed':
            completed.append(vacc)
        elif due_date < today:
            overdue.append(vacc)
        else:
            upcoming.append(vacc)
    
    context += f"- Completed Vaccines: {len(completed)}\n"
    context += f"- Overdue Vaccines: {len(overdue)}\n"
    context += f"- Upcoming Vaccines: {len([v for v in upcoming if (date.fromisoformat(v['due_date']) if isinstance(v['due_date'], str) else v['due_date']) <= today + __import__('datetime').timedelta(days=30)])}\n"
    
    if overdue:
        context += "\nOverdue Vaccines:\n"
        for v in overdue[:5]:
            context += f"  - {v['vaccine_name']} (was due: {v['due_date']})\n"
    
    if upcoming:
        context += "\nUpcoming Vaccines (next 30 days):\n"
        for v in upcoming[:5]:
            due = v['due_date']
            if isinstance(due, str):
                due = date.fromisoformat(due)
            if due <= today + __import__('datetime').timedelta(days=30):
                context += f"  - {v['vaccine_name']} (due: {v['due_date']})\n"
    
    if health_events:
        context += "\nRecent Health Events:\n"
        for event in health_events[:5]:
            context += f"  - [{event['event_type']}] {event['title']} on {event['event_date']}\n"
            if event.get('symptoms'):
                context += f"    Symptoms: {event['symptoms']}\n"
    
    return context

def get_system_prompt(child_context: str) -> str:
    return f"""You are a helpful Smart Child Vaccination & Health Assistant. You help parents track and manage their child's vaccination schedule and provide general health guidance.

IMPORTANT GUIDELINES:
1. You have access to the following child health data:
{child_context}

2. For vaccination questions:
   - Reference the actual vaccination schedule data provided
   - Identify overdue, upcoming, and completed vaccines
   - Explain vaccine importance when asked

3. For health-related questions:
   - Provide general, non-diagnostic guidance
   - Always recommend consulting a healthcare professional for specific medical advice
   - Be supportive and informative

4. ALWAYS include this disclaimer for health advice:
   "⚠️ This information is for educational purposes only and is not a substitute for professional medical advice. Please consult your child's pediatrician for personalized medical guidance."

5. Be warm, supportive, and parent-friendly in your responses.
6. Keep responses concise but informative.
7. If asked about symptoms, provide general guidance but emphasize consulting a doctor.

Current date: {date.today().strftime('%B %d, %Y')}
"""

def chat_with_assistant(
    user_message: str,
    child: Optional[Dict],
    vaccinations: List[Dict],
    health_events: List[Dict],
    conversation_history: List[Dict]
) -> str:
    client = get_openai_client()
    
    if not client:
        return "⚠️ AI Assistant is not available. Please configure your OpenAI API key in the Settings page to enable the AI assistant."
    
    child_context = format_child_context(child, vaccinations, health_events)
    system_prompt = get_system_prompt(child_context)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    for msg in conversation_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    messages.append({"role": "user", "content": user_message})
    
    try:
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            max_completion_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ I encountered an error: {str(e)}. Please check your API key configuration or try again later."

def transcribe_audio(audio_file_path: str) -> str:
    client = get_openai_client()
    
    if not client:
        return "Audio transcription requires an OpenAI API key. Please configure it in Settings."
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return response.text
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def get_quick_responses() -> List[Dict[str, str]]:
    return [
        {"label": "Next vaccine due?", "query": "When is my child's next vaccine due?"},
        {"label": "Missed vaccines?", "query": "Which vaccines has my child missed?"},
        {"label": "Vaccine schedule", "query": "Can you show me my child's complete vaccination schedule?"},
        {"label": "Child has fever", "query": "My child has a fever, what should I do?"},
        {"label": "Vaccine side effects", "query": "What are common side effects after vaccination?"},
        {"label": "Feeding advice", "query": "Can you give me some general feeding tips for my child's age?"},
    ]
