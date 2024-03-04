FROM python:3.11-alpine3.16 as requirements-stage

WORKDIR /tmp

RUN pip install poetry
COPY ./poetry.lock* ./pyproject.toml /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-alpine3.16 as build-stage

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

CMD ["uvicorn", "src.main:app","--host", "0.0.0.0", "--port", "8000", "--reload"]