FROM python:3.10.14-slim
LABEL org.opencontainers.image.description MCN Practical Lab App

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY app .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
