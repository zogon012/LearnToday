# Signal Kill Test

Docker와 Poetry를 사용한 시그널 처리 및 graceful shutdown 테스트 애플리케이션

## 프로젝트 구조

```
signal_kill_test/
├── main.py              
├── pyproject.toml       
├── Dockerfile           
├── docker-compose.yml   
└── README.md           
```

## 주요 기능

- 시그널 처리: SIGTERM, SIGINT 시그널을 캐치하여 우아한 종료 수행
- Graceful Shutdown: 리소스 정리, 연결 해제, 상태 저장 등 시뮬레이션
- 로깅: 자세한 로그로 시그널 처리 과정 추적

## 사용법

### 애플리케이션 실행

```bash
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build
```

### 시그널 테스트

#### SIGTERM 시그널 전송
```bash
docker stop signal-kill-test

# 또는 직접 SIGTERM 전송
docker kill --signal=TERM signal-kill-test
```

#### SIGINT 시그널 전송
```bash
docker kill --signal=INT signal-kill-test
```

#### SIGKILL 시그널 전송
```bash
docker kill --signal=KILL signal-kill-test
```

### 로그 확인

```bash
# 실시간 로그 확인
docker-compose logs -f

# 또는
docker logs -f signal-kill-test
```

## 예상 출력

정상적인 graceful shutdown 시:

```
2025-12-14 10:30:00,000 - INFO - Application starting...
2025-12-14 10:30:00,001 - INFO - Send SIGTERM (docker stop) or SIGINT (Ctrl+C) to test graceful shutdown
2025-12-14 10:30:00,002 - INFO - Signal handlers registered for SIGTERM and SIGINT
2025-12-14 10:30:00,003 - INFO - Working... (iteration 1)
2025-12-14 10:30:01,004 - INFO - Working... (iteration 2)
...
2025-12-14 10:30:05,010 - WARNING - Received SIGTERM - Initiating graceful shutdown...
2025-12-14 10:30:05,011 - INFO - Starting graceful shutdown process...
2025-12-14 10:30:05,012 - INFO - Saving application state...
2025-12-14 10:30:06,013 - INFO - Closing connections...
2025-12-14 10:30:06,514 - INFO - Cleaning up resources...
2025-12-14 10:30:07,015 - INFO - Graceful shutdown completed (triggered by SIGTERM)
2025-12-14 10:30:07,016 - INFO - Application terminated
```

## 정리

```bash
# 컨테이너 정리
docker-compose down

# 이미지까지 삭제
docker-compose down --rmi all
```

## 주의사항

- SIGKILL (signal 9)은 프로세스를 즉시 강제 종료하므로 graceful shutdown이 불가능합니다
- Docker의 기본 stop 타임아웃은 10초입니다. 그 이후에는 자동으로 SIGKILL이 전송됩니다
- 프로덕션 환경에서는 적절한 타임아웃 설정이 중요합니다