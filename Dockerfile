FROM python:3.10

RUN pip install "poetry==1.1.14"

RUN mkdir /application
WORKDIR /application

COPY app/pyproject.toml /application
COPY app/poetry.lock /application

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi

RUN pip install passlib PyJWT python-multipart

COPY app /application

RUN chmod +x /application/script.sh
CMD [ "sh", "-c", "/application/script.sh" ]
