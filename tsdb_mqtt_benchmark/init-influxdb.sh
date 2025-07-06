#!/bin/bash

ORG=demo-org
BUCKET=demo-bucket
TOKEN=demo-token
INFLUX_HOST=http://influxdb:8086

# InfluxDB가 완전히 뜰 때까지 대기 (최대 60초)
for i in {1..30}; do
  influx ping --host $INFLUX_HOST && break
  echo "[init-influxdb] InfluxDB가 아직 준비되지 않음, 대기 중... ($i)"
  sleep 2
done

# org가 없으면 생성
for i in {1..10}; do
  influx org list --host $INFLUX_HOST --token $TOKEN | grep -q $ORG && break
  echo "[init-influxdb] org가 없으므로 생성 시도... ($i)"
  influx org create --host $INFLUX_HOST --token $TOKEN --name $ORG && break
  sleep 2
done

# 버킷 존재 여부 확인 및 생성
for i in {1..10}; do
  influx bucket list --host $INFLUX_HOST --org $ORG --token $TOKEN | grep -q $BUCKET && break
  echo "[init-influxdb] 버킷이 없으므로 생성 시도... ($i)"
  influx bucket create --host $INFLUX_HOST --org $ORG --token $TOKEN --name $BUCKET && break
  sleep 2
done

echo "[init-influxdb] 초기화 완료!"