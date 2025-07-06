FROM python:3.10-slim
WORKDIR /app
COPY mqtt_tdengine_consumer.py .
RUN pip install paho-mqtt taospy
RUN apt-get update && apt-get install -y wget && \
    wget https://www.taosdata.com/assets-download/3.2.4.0/TDengine-client-3.2.4.0-Linux-x64.tar.gz && \
    tar -zxvf TDengine-client-3.2.4.0-Linux-x64.tar.gz && \
    cd TDengine-client-3.2.4.0 && ./install_client.sh && \
    ldconfig
CMD ["python", "mqtt_tdengine_consumer.py"]
