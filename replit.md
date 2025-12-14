# Smart Child Vaccination & Health Assistant

## Overview

A comprehensive full-stack Streamlit web application designed for parents to track and manage their child's vaccination and health timeline. The application is user-friendly, medically responsible, and scalable.

## Project Structure

```
├── app.py                      # Main Streamlit application entry point
├── database.py                 # SQLite database module with schema and operations
├── vaccination_guidelines.py   # Vaccination schedules (India UIP, WHO, CDC)
├── ai_assistant.py             # OpenAI integration for chat and voice
├── notifications.py            # Email reminder functionality
├── pages/
│   ├── __init__.py
│   ├── dashboard.py           # Dashboard with overview and charts
│   ├── vaccination_schedule.py # Vaccine tracking and completion
│   ├── health_timeline.py     # Health events timeline
│   ├── assistant.py           # AI chat and voice assistant
│   └── settings.py            # Child profiles and notification settings
├── .streamlit/
│   └── config.toml            # Streamlit server configuration
└── vaccination_health.db      # SQLite database (auto-created)
```

## Technology Stack

- **Frontend & Backend**: Streamlit (Python)
- **Database**: SQLite
- **AI/NLP**: OpenAI GPT-5 & Whisper for chat and voice
- **Charts**: Plotly for interactive visualizations
- **Notifications**: SMTP for email reminders

## Features

### 1. Personalized Vaccination Scheduler
- Auto-generates schedules based on India UIP, WHO, or CDC guidelines
- Tracks upcoming, overdue, completed, and pending vaccines
- Mark vaccines as completed with details (date, doctor, batch number)

### 2. Health Timeline & History
- Visual timeline of vaccinations, illnesses, symptoms, and doctor visits
- Filterable by category
- Chronological event tracking

### 3. Smart Reminders & Alerts
- In-app notifications for overdue and upcoming vaccines
- Email reminder support (7 days, 1 day, and on due date)
- Opt-in notification preferences per child

### 4. Voice & Chat-Based AI Assistant
- Natural language queries about vaccination schedule
- Voice input using OpenAI Whisper transcription
- Health guidance with medical disclaimers

### 5. Dashboard
- Vaccination progress overview
- Status charts using Plotly
- Quick action navigation

## Running the Application

```bash
streamlit run app.py --server.port 5000
```

## Environment Variables

### Required
- `OPENAI_API_KEY`: For AI assistant functionality

### Optional (for email notifications)
- `SMTP_SERVER`: SMTP server address
- `SMTP_PORT`: SMTP port (default: 587)
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password

## Database Schema

### Tables
1. **children**: Child profiles with DOB, guideline selection, allergies
2. **vaccinations**: Vaccine records with due dates and completion status
3. **health_events**: Illnesses, symptoms, and doctor visits
4. **reminder_settings**: Notification preferences per child
5. **sent_reminders**: Tracking of sent notifications

## Vaccination Guidelines Supported

1. **India (UIP)**: Universal Immunization Programme
2. **WHO**: World Health Organization recommendations
3. **CDC (USA)**: Centers for Disease Control and Prevention

## Medical Disclaimer

This application provides general vaccination tracking and health information. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult your child's pediatrician for personalized medical guidance.

## Future Enhancements

- PostgreSQL migration for production
- Twilio SMS integration
- Multi-child profile management
- PDF report generation
- Vaccine certificate with QR codes
- Multi-language support
