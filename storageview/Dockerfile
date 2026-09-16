FROM python:3.14-slim
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install flask
COPY app.py .
COPY templates/ templates/
EXPOSE 5000
CMD ["python", "app.py"]