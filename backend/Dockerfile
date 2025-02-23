FROM python:3.11.11-slim

WORKDIR /src
ENV PYTHONPATH=/src \
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt update && apt install -y curl
RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY poetry.lock pyproject.toml ./
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install

COPY . /src/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]