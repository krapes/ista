import time
from flask import Flask, request
# from api.LanguageModel import ask_question, setup
import sys, os
from pathlib import Path

from lingotk import languagemodel as lm

app = Flask(__name__)
active_model = None


@app.route('/')
def home():
    return {'message': 'SUCCESS'}


@app.route('/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/query', methods=['POST'])
def query():
    global active_model
    question = request.json.get('query', '')
    if question == '':
        return {'query': None, 'response': 'Please ask a question'}
    if active_model is None:
        active_model = lm.LanguageModel()
    return active_model.ask_question(question)


if __name__ == '__main__':
    app.run(port=5001)
