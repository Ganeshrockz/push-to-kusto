FROM python:3-slim
WORKDIR /app
COPY . .
ENV INPUT_NAME="Ganesh"
CMD ["python3", "app.py"]