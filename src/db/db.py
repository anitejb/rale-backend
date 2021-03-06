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


def update_result(new_topic, new_question, new_wolfram_question):
    if not db.child("results").child('current_session').shallow().get().val():
        entry = None
    else:
        entries = db.child("results").child('current_session').get()
        for e in entries.each():
            entry = e.val()
            key = e.key()

    if entry:
        topics = entry.get('topics', [])
        questions = entry.get('questions', [])
        wolfram_questions = entry.get('wolfram', [])
        updated_result = {
            'topics': topics + new_topic,
            'questions': questions + new_question,
            'wolfram': wolfram_questions + new_wolfram_question
        }
        db.child("results").child('current_session').child(key).update(updated_result)
    else:
        db.child("results").child('current_session').push({
            'topics': new_topic,
            'questions': new_question,
            'wolfram': new_wolfram_question
        })

# update_result([{'topic': 'green gas emission'}], [{"question": 'Is the earth round?', "question_type": 'YN'}])
