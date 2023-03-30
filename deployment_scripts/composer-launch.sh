#!/bin/bash

source .env
docker build -f Dockerfile.client -t gcr.io/$PROJECT_ID/react-flask-app-client .
docker build -f Dockerfile.api  -t gcr.io/$PROJECT_ID/react-flask-app-api \
         --build-arg OPENAI_API_KEY=$OPENAI_API_KEY .
       #  --build-arg PROJECT_ID=$PROJECT_ID \

docker-compose up