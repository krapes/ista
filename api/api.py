import time
from flask import Flask, request
from . import LanguageModel


app = Flask(__name__)

@app.route('/')
def home():
    return {'message': 'SUCCESS'}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/query', methods=['POST'])
def query():
    question = request.json.get('query')
    return LanguageModel.trial_question(question)

if __name__ == '__main__':
      app.run(port=5001)