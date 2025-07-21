# event-generate-software

A smart assistant system to automatically record, track, and remind teachers and students of meetings, assigned tasks, and schedules.

##  Overview

In a typical academic setup, teachers frequently interact with multiple students — assigning tasks, scheduling follow-ups, and organizing discussions. However, it's easy to lose track of:
- Who was assigned what task
- When the next meeting is
- What discussions were held previously

event-generate-software addresses this issue by providing an intelligent, voice-enabled assistant that:
- Recognizes the student's face and voice
- Records meeting details and tasks automatically
- Stores event logs with timestamps
- Notifies both teacher and student about upcoming meetings or deadlines

##  Key Features

- Voice Recognition: Identify commands and instructions from the teacher using speech recognition.
- Facial Recognition: Detect and verify participants (student) using facial data.
- Task/Event Generation: Automatically create and log events based on conversations.
- Assistant Module: A smart agent that understands intent and helps in logging meeting info.
- Storage Integration: Uses `token.json` and Google Calendar API to create real-time calendar events.
- Reminders: Notifies users about upcoming tasks or meetings.

##  Tech Stack

- Python for scripting and logic
- SpeechRecognition, PyAudio – voice processing
- OpenCV, face_recognition – facial detection
- Google Calendar API – event creation and reminders
- Node.js (tensorflow.js) – real-time interaction or ML inference (optional)

## Project Structure

event-generate-software/
│
├── 1.py # Utility or testing script
├── assistant.py # Main assistant logic for voice/intent processing
├── facerecognition.py # Handles face recognition using OpenCV
├── main.py # Entry point, integrates all modules
├── quickstart.py # Google Calendar API setup and authentication
├── tensorflow.js # Optional TensorFlow.js script for browser-based logic
├── token.json # OAuth token for Google Calendar API
├── voiceRecognition.py # Handles speech-to-text and keyword spotting
├── README.md # Project documentation


##  How It Works

1. Authentication: Authenticate with Google Calendar using `token.json`.
2. Initiate Meeting: Teacher starts the session using `main.py`.
3. Voice and Face Recognition: System identifies participants.
4. Intent Parsing: Extracts tasks and meeting times from voice input.
5. Event Creation: Automatically logs the task and meeting in Google Calendar.
6. Reminders: Sends alerts
   

 ## Future Enhancements
Web dashboard for viewing and editing events

Integration with WhatsApp or email notifications

Summarization of past conversations using LLMs

Student-side assistant interface


