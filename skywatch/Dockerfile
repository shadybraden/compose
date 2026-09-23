ARG PYTHON_VERSION=3.14.7
ARG ALPINE_VERSION=3.23
FROM python:${PYTHON_VERSION}-alpine${ALPINE_VERSION}

ENV TZ="America/New_York"

WORKDIR /app

COPY skywatch/. /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "skywatch.py"]
