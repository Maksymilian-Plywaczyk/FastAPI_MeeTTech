FROM python:3.12.2-alpine3.19

WORKDIR /code

RUN  pip install --no-cache-dir poetry

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry config virtualenvs.create false

RUN poetry install --no-dev --no-interaction

COPY ./src /code/src

CMD ["uvicorn", "src.main:app","--host", "0.0.0.0", "--port", "8000", "--reload"]
