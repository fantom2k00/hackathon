import random
import firebase_admin
import time

from chat_gpt_api import generateArticle
from google_scholar_api import searchGoogleScholar
from google_trends_api import getTrendingTopics
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

config = {
  "user configs"
}

cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://explosivepopcorn-2428d-default-rtdb.europe-west1.firebasedatabase.app/'})
firestore_client = firestore.client()

ref = firestore_client.collection("categories")

@app.route("/")
def hello_world():
    return render_template("index.html")

@socketio.on('connect')
def test_connect(_):
    print("CONNECTING /////////////////////////")
    trend = ''
    for r in ref.get():
        if r.to_dict()['selected']:
            trend = str(r.to_dict()['title'])

    if not trend:
        trend = 'Technology'
            
    print(trend)

    topics = getTrendingTopics(trend)
    topic_id = random.randint(0, len(topics)-1)
    print(topics)
    emit('trend response', topics[topic_id])

@socketio.on('scholar')
def test_scholar(topic):
    print("SCHOLAR /////////////////////////")
    authors, titles, links = searchGoogleScholar(list(topic))
    article_id = random.randint(0, len(titles)-1)
    print(authors[article_id])
    print(titles[article_id])
    print(links[article_id])    
    emit('scholar response', {'topic': topic, 'author': authors[article_id], 'title': titles[article_id], 'link': links[article_id]})
  
@socketio.on('gpt')
def test_gpt(data): 
    print("GPT /////////////////////////") 
    article = generateArticle(data["link"])
    data["article"] = article
    print(data)
    emit('gpt response', data)
    
@socketio.on('firebase')
def test_firebase(data):
    print("FIREBASE /////////////////////////")
    doc_ref = firestore_client.collection('articles').document()
    doc_ref.set({
        'dateArticle': '2020',
        'author': data["author"],
        'date': time.time(), 
        'summary': data["article"],
        'source': data["link"],
        'title': data["title"],
        'topic': data["topic"]
    })
    emit('firebase response')
    
@socketio.on('disconnect')
def test_disconnect():
    print("DICONNECT /////////////////////////")
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
