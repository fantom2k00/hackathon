from chat_gpt_api import generateArticle
from google_scholar_api import searchGoogleScholar
from google_trends_api import getTrendingTopics
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def hello_world():
    return render_template(
        "index.html",
        )

@socketio.on('connect')
def test_connect():
    topics = getTrendingTopics("Technology")
    topic_id = random.randint(0, len(topics))
    titles, links = searchGoogleScholar(topics[topic_id])
    article_id = random.randint(0, len(titles))
    article = generateArticle(links[article_id])
    emit('trend response', {'data': topics[topic_id]})
    emit('scholar response', {'data': titles[article_id]})
    emit('gpt response', {'data': article})
    emit('link response', {'data': links[article_id]})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)
