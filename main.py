import datetime
import os.path
import pickle
import threading

import pyttsx3
import speech_recognition as sr
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak_reminder(reminder_message):
    engine.say(reminder_message)
    engine.runAndWait()

def set_reminder(reminder_date, reminder_time, reminder_message):
    try:
        reminder_date = datetime.datetime.strptime(reminder_date, "%Y-%m-%d")
        reminder_time = datetime.datetime.strptime(reminder_time, '%H:%M')
        reminder_datetime = reminder_date.replace(hour=reminder_time.hour, minute=reminder_time.minute)
        time_diff = reminder_datetime - datetime.datetime.now()
        if time_diff.total_seconds() < 0:
            reminder_datetime += datetime.timedelta(days=1)
            time_diff = reminder_datetime - datetime.datetime.now()
        threading.Timer(time_diff.total_seconds(), lambda: speak_reminder(reminder_message)).start()
    except ValueError:
        print("Invalid date or time format")

def create_event(service, reminder_date, reminder_time, reminder_message):
    event = {
        'summary': reminder_message,
        'description': reminder_message,
        'start': {'dateTime': f'{reminder_date}T{reminder_time}:00'},
        'end': {'dateTime': f'{reminder_date}T{reminder_time}:01'},
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def main():
    engine.say('I am your Alexa')
    engine.say('what i can do for you?')
    engine.runAndWait()
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                print(command)
    except:
        pass

    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'set reminder' in command:
                engine.say('Please speak the reminder date in YYYY-MM-DD format')
                engine.runAndWait()
                with sr.Microphone() as source:
                    reminder_date_voice = listener.listen(source)
                    reminder_date = listener.recognize_google(reminder_date_voice)
                    print(reminder_date)

                engine.say('Please speak the reminder time in HH:MM format')
                engine.runAndWait()
                with sr.Microphone() as source:
                    reminder_time_voice = listener.listen(source)
                    reminder_time = listener.recognize_google(reminder_time_voice)
                    print(reminder_time())

                engine.say('Please speak the reminder message')
                engine.runAndWait()
                with sr.Microphone() as source:
                    reminder_message_voice = listener.listen(source)
                    reminder_message = listener.recognize_google(reminder_message_voice)
                    print(reminder_message())

                set_reminder(reminder_date, reminder_time, reminder_message)

                creds = None
                # The file token.pickle stores the user's access and refresh tokens, and is
                # created automatically when the authorization flow completes for the first
                # time.
                if os.path.exists('token.pickle'):
                    with open('token.pickle', 'rb') as token:
                        creds = pickle.load(token)
                # If there are no (valid) credentials available, let the user log in.
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', SCOPES)
                        creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open('token.pickle', 'wb') as token:
                        pickle.dump(creds, token)
                try:
                    service = build('calendar', 'v3', credentials=creds)

                    create_event(service, reminder_date, reminder_time, reminder_message)
                except:
                    pass
            else:
                print('i didnt understand that')
    except sr.UnknownValueError:
        print('i didnt understand that')
        pass

if __name__ == '__main__':
    main()