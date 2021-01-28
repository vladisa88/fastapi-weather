FROM python:3.9

RUN pip install pipenv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

COPY ./app/Pipfile* /app/

RUN pipenv install --system --deploy --dev

COPY ./app /app
