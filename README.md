## GET STARTED

1. Using docker:\
    First build docker image: `docker build -t <your_image_name> -f <your_dockerfile> .`\
    Second run docker container: `docker run --name <your_new_container_name> -p 8000:8000 <your_image_name>`\
2. Using virtual environment:\
    Create venv: `python -m venv venv`\
    Launch your venv (using Windows): `venv/Scripts/activate` or using Mac/Linux `source venv/bin/activate`\
    Install dependencies: `pip install -r requirements.txt`
    Start your app (development mode) in `src` folder: `uvicorn main:app --reload`