import time
from datetime import datetime
from flask import Flask, request
from google.cloud import storage
from lingotk import languagemodel as lm
import os
import logging


app = Flask(__name__)
gcs = storage.Client()
#CLOUD_STORAGE_BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
CLOUD_STORAGE_BUCKET = "subjectguru"
PROJECT_ID = "animated-verve-240319"
os.environ['PROJECT_ID'] = PROJECT_ID

active_model = None


@app.route('/api')
def home():
    return {'message': 'SUCCESS'}


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/health')
def health():
    return '', 200

@app.route('/ready')
def ready():
    return '', 200

@app.route('/api/query', methods=['POST'])
def query():
    global active_model
    question = request.json.get('query', '')
    if question == '':
        return {'query': None, 'response': 'Please ask a question'}
    if active_model is None:
        active_model = lm.LanguageModel()
    return active_model.ask_question(question)

@app.route('/api/fileupload', methods=['POST'])
def fileupload():
    """Process the uploaded file and upload it to Google Cloud Storage."""
    timestamp = datetime.now().strftime("%m-%d-%Y:%H:%M:%S")
    logging.info(f"Storing files in folder: {timestamp}")

    uploaded_files = request.files.getlist('file')
    if not uploaded_files:
        return "No file uploaded.", 400

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    # Create a new blob and upload the file's content.
    for file in uploaded_files:
        blob = bucket.blob(f"{timestamp}-{file.filename}")
        blob.upload_from_string(
            file.read(), content_type=file.content_type
        )
        logging.info(f"Upload of {file} Complete")

    global active_model
    active_model = lm.LanguageModel(document_directory=timestamp)
    return {"message": "Upload Complete"}


if __name__ == '__main__':
    app.run(port=5001)
