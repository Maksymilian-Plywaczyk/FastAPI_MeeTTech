## GET STARTED
This repository represent demo app for MeeTTech presentation. The main idea is to present how fast you can build your first API with FastAPI including error handling, data validation, authentication, testing, dependency injection and auto generation of documentation (OpenAPI). 
1. Using docker imgae:\
    First build docker image: `docker build -t <your_image_name> -f <your_dockerfile> .`\
    Second run docker container: `docker run --name <your_new_container_name> -p 8000:8000 <your_image_name>`\
2. Using docker compose:\
    Build your services: `docker compose build`
    Run your services: `docker compose up` alternatively you can add flag `-d` like: `docker compose up -d` to run services in the background 
4. Using poetry:\
    Configurate poetry on your machine: https://python-poetry.org/docs/  \
    Install dependencies: `poetry install`\
    Launch your venv (using poetry): `poetry shell`\
    Start your app (development mode) in `src` folder: `uvicorn main:app --reload`
