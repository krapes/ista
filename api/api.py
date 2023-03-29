import time
from flask import Flask, request
from google.cloud import storage
from lingotk import languagemodel as lm
import os
import logging

app = Flask(__name__)
#CLOUD_STORAGE_BUCKET = os.environ["CLOUD_STORAGE_BUCKET"]
CLOUD_STORAGE_BUCKET = "subjectguru"

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
    uploaded_file = request.files.get("file")
    filenames = request.files.getlist("file")
    if not uploaded_file:
        return "No file uploaded.", 400
    # Create a Cloud Storage client.
    gcs = storage.Client()
    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)
    blob.upload_from_string(
        uploaded_file.read(), content_type=uploaded_file.content_type
    )
    logging.info(f"Upload of {filenames} Complete")
    return {"message": "Upload Complete"}


if __name__ == '__main__':
    app.run(port=5001)
