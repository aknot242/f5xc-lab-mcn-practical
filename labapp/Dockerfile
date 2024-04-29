FROM python:3.10.14-slim
LABEL org.opencontainers.image.description MCN Practical Lab App

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY app .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0"]
