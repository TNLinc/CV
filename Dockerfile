FROM amd64/python:3.9.8-bullseye

RUN pip install --upgrade pip setuptools
RUN pip install poetry==1.1.11

WORKDIR /cv
COPY ./pyproject.toml /cv/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . .

CMD ["bash", "./scripts/flask-entrypoint.sh"]
