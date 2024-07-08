FROM python:3.11.9

WORKDIR /app

RUN pip install -U pip poetry==1.6.1 lockfile==0.12.2 --no-cache-dir &&  \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . .

ENV PYTHONPATH=.:src

ENTRYPOINT uvicorn src.app:app --host 0.0.0.0 --port 8080 --reload
