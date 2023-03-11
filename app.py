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
  "type": "service_account",
  "project_id": "explosivepopcorn-2428d",
  "private_key_id": "81ae841298e03d46edf709a72838c4f407cb609d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCnUrrW8de6ls8d\nD5VHNSEbx1NqbjjLthJA0CPf33K0Mmm0lDfYgyYnIXl+SDBQnN2a613tqKq/T4Vv\ni4+Uz647n0opT+RisJJFLRmYvUEXR2U2pJiBJRNUf7V2aXH1GjFWtAp1LfdMB2UN\nsn4VCYyv9bV4b9REGFiyqtnUvVa5bD73AannDVDEcIwfqRYmcVFdbJMWn9GC4fXn\nxheNXENK9BmnoHzDNb6rgofFiqg87/KkzfHGkriYDCQEf/rJBE2DDS/aJX9S40a0\ncB0rgv5q3+3M7Qg6yZm3zkIEfMNFE+krgN2za4mWCiZc9uuPWVQdObg9MxOJAtZN\nr5ircskXAgMBAAECggEAAbCuPnmW6kWXtf1wTpXUzckHqK2QWU5vhMQVeK9zIyrX\nMoHExqUcf4yxA3uLMWVEP8pc2oe3odMVz/ii7KfkZKnJP/2UmwKZl6VK+uX+gFOy\nTAkBmVxcg5/+n0GVaxpmoS+UY3ahZt00Qh0pdODx0N00hhDrHfz4+GUNaj63X4wa\nKywyKUDPKweNfFYvw6eqaVA02d/mskyNTovhrpjBg3EUy2kwsKXlhilNJAMPPrlE\ntky/QNgH2TkoV/3svppSlzQt2d8z1Udo/7aiJq7HLHFlat/LuBeLrCiOxFeK1Jkn\nbytDiMt7mAnQkjio2yuF/Raw30sWFChODP4M3ZASoQKBgQDkSOIXN3Y1ZbFzAuih\nglkahTTJD3xIvILVD1sGITRgjpyrAa1zARcmqqnrZ5xzn4cLj2nQTh+rCNhs04P7\nQXFyEs/+HBot08wJFmbQhr/rNqeDej7jWU+ySMyXoqmEPAif1AOvmJjyJblnFZ0J\n2rIOy+Ze6VznfEZW+zhbxezNnwKBgQC7oyeQlCVAjmtewymZ035HeytZ2f1qiMoD\nB+kL0tm6cRclwcxUEY3mGIC2J7bOm6oWbcT69T73azxj/dXQ67RtBfvR0b7dTFaN\nni2zxajVodMm7nDQnz83Na9TaXCRvHtrPz5C9tos5I5idIGuueuoE/aN7P0V6cjK\nnXKnAQDhiQKBgCphmY/j3Q9GxO3sQVISyAYTatxVAqbiUIvLoQN/UKEIeO+KjTAH\nqMul7YvlnXcdy82Kn4NrrZdsOfniPuN7n9skwPaVMwsFAiFBxm66RZEegXT4UgqV\nPyWDPHB+Y2hIWPWLP+/urZ5vAH+x1IjK0DnNAwTl4DidqtVlKG5pTXBTAoGBAKYr\nhGNmv2LffbjrT1E6WnAFZUvqYKHTSEvM2pctAMM7WguHCGQ/M5JdisdGfn+UndnF\nFphFTqEg59eJuayOwTd4AB4+CTDEZTZ/qeu2FaIz8OJecaxgC0Til0VgcF+wMwC0\nfnghUvBE7M/Ga/6ICmnMXCIuiae5ZagCLcI2gkg5AoGBAJaUfKbUT2OZfmCZGaxL\nWy65AsjVTs7cy2Ur/9hte85CNReQQbETesdsYLKqrgrlaezwgeb1OmkW6ayfmvdW\nrVm3BlT3p5CUcHhof6IqPO+Ld+aafLjcqyc/ycTiFEDsHwWSZTUhx7vegjb3KK57\nfsUMhxsSBedTb/o490x7APM1\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3qqhe@explosivepopcorn-2428d.iam.gserviceaccount.com",
  "client_id": "104692780969323790880",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3qqhe%40explosivepopcorn-2428d.iam.gserviceaccount.com"
}

cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://explosivepopcorn-2428d-default-rtdb.europe-west1.firebasedatabase.app/'})
firestore_client = firestore.client()

@app.route("/read_data")
def get_from_db():
    ref = firestore_client.collection("articles").document("QF1e4Ypo0DOOtmFdkoZg")
    print(ref.get().to_dict())
    return "<p>ref<p>"

@app.route("/")
def hello_world():
    return render_template("index.html")

@socketio.on('connect')
def test_connect():
    print("CONNECTING /////////////////////////")
    topics = getTrendingTopics("Technology")
    topic_id = random.randint(0, len(topics)-1)
    print(topics)
    emit('trend response', topics[topic_id])

@socketio.on('scholar')
def test_scholar(topic):
    print("SCHOLAR /////////////////////////")
    authors, titles, links = searchGoogleScholar(topic)
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
