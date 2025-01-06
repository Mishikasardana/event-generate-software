import speech_recognition as sr
import pyttsx3
import datetime
import threading
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import cv2
from deepface import DeepFace
import pyaudio
import wave

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
r = sr.Recognizer()
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

def speak_reminder(reminder_message):
    engine.say(reminder_message)
    engine.runAndWait()

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
                    print(reminder_time)

                engine.say('Please speak the reminder message')
                engine.runAndWait()
                with sr.Microphone() as source:
                    reminder_message_voice = listener.listen(source)
                    reminder_message = listener.recognize_google(reminder_message_voice)
                    print(reminder_message)
                    if reminder_message == "Mishika":
                        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

                        counter = 0

                        face_match = False
                        reference_img = cv2.imread('reference.jpg')

                        def check_face(frame):
                            global face_match
                            try:
                                if DeepFace.verify(frame, reference_img.copy())['verified']:
                                    face_match = True
                                else:
                                    face_match = False
                            except ValueError:
                                face_match = False

                        while True:
                            ret, frame = cap.read()

                            if ret:
                                if counter % 30 == 0:
                                    try:
                                        threading.Thread(target=check_face, args=(frame.copy(),)).start()
                                    except ValueError:
                                        pass
                                counter += 1

                                if face_match:
                                    cv2.putText(frame, "Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                                else:
                                    cv2.putText(frame, "Not Match", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),
                                                3)
                                cv2.imshow('Video', frame)
                            key = cv2.waitKey(1)
                            if key == ord('q'):
                                break
                        cv2.destroyAllWindows()

                set_reminder(reminder_date, reminder_time, reminder_message)
                creds = None
                if os.path.exists("token.json"):
                    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
                # If there are no (valid) credentials available, let the user log in.
                if not creds or not creds.valid:
                    if creds and creds.expired and creds.refresh_token:
                        creds.refresh(Request())
                    else:
                        flow = InstalledAppFlow.from_client_secrets_file(
                            "credentials.json", SCOPES
                        )
                        creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open("token.json", "w") as token:
                        token.write(creds.to_json())

                try:
                    service = build("calendar", "v3", credentials=creds)

                    # Call the Calendar API
                    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
                except HttpError as error:
                    print(f"An error occurred: {error}")
            else:
                print('i didnt understand that')
    except sr.UnknownValueError:
        print('i didnt understand that')
        pass



def record_text():
    while(1):
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occured")
    return
def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return
while (1):
        text = record_text()
        output_text(text)
        print(text)
        if text == "set reminder":
            main()

audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
frames = []
try:
    while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass





if __name__ == '__main__':


    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    audio.terminate()
    sound_file = wave.open('voiceRecognition.wav', 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    r = sr.Recognizer()
    sound_file.close()
