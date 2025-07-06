FROM python:3.10-slim
WORKDIR /app
COPY mqtt_publisher.py .
RUN pip install paho-mqtt
CMD ["python", "mqtt_publisher.py"]
