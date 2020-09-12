import os
import pyrebase
import json


firebase_config = {
  "apiKey": os.getenv('FIREBASE_API_KEY'),
  "authDomain": f'{os.getenv("FIREBASE_PROJECT_ID")}.firebaseapp.com',
  "databaseURL": f'https://{os.getenv("FIREBASE_PROJECT_ID")}.firebaseio.com',
  "storageBucket": f'{os.getenv("FIREBASE_PROJECT_ID")}.appspot.com'
}

firebase = pyrebase.initialize_app(firebase_config)

db = firebase.database()

def push_to_audio_chunks(value):
    db.child("audio-chunks").child(time.time()).push(value)

def push_to_results(value):
    db.child("results").child(time.time()).push(value)


def stream_handler(event):
    messages = event['data']
    for key in messages:
        message = messages[key]
        text, timestamp = message['text'], message['timestamp']
        print(f'{text} : {timestamp}')
        # call NLP to update results

def start_event_stream():
    my_stream = db.child("audio-chunks").stream(stream_handler)
    return my_stream