FROM python:3.10.12

ENV PYTHONUNBUFFERED=1

RUN curl -sSL https://install.python-poetry.org 

WORKDIR /src

RUN pip install -U pip poetry lockfile --no-cache-dir && \
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install 

COPY . .

EXPOSE 8000
