#!/bin/bash

source .env
docker build -f Dockerfile.client -t gcr.io/$PROJECT_ID/react-flask-app-client .
docker push gcr.io/$PROJECT_ID/react-flask-app-client
docker build -f Dockerfile.api -t gcr.io/$PROJECT_ID/react-flask-app-api \
         --build-arg OPENAI_API_KEY=$OPENAI_API_KEY .
docker push gcr.io/$PROJECT_ID/react-flask-app-api
gcloud builds submit  --config scripts/cloudbuild.yaml
