# Match Schedule (프론트엔드 전용)

간단한 정적 웹페이지로 `match.csv` 파일을 읽어 예쁘게 출력하고 브라우저의 인쇄(PDF 저장)를 사용해 PDF로 저장할 수 있습니다.

실행 (Docker Compose 권장)

1. Docker & Docker Compose 설치 후 프로젝트 루트에서 실행:

```bash
docker compose up
```

2. 브라우저에서 열기: http://localhost:8000

3. 페이지에서 `PDF로 저장` 버튼을 누르거나 브라우저 메뉴에서 `인쇄` -> `PDF로 저장` 선택

로컬에서 (간단)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m http.server 8000
# 브라우저에서 http://localhost:8000 열기
```

파일

- index.html — 메인 페이지
- styles.css — 스타일
- script.js — CSV 파싱 및 렌더링
- match.csv — 일정 데이터 (기존에 있음)
- docker-compose.yml — 정적 서버 실행 설정
 - emblems/ — 구단 엠블럼 이미지 폴더 (선택). 이미지 파일명은 각각 `encodeURIComponent(구단명).png` 형태로 넣으시면 됩니다. 예: `FC안양.png` → `emblems/FC%EC%95%88%EC%96%91.png`

참고: 로컬 파일을 직접 브라우저로 열면(Ctrl+O) 브라우저 보안 정책으로 `fetch('match.csv')`가 차단될 수 있으니 반드시 서버로 서빙하세요.
