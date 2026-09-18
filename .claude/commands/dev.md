---
description: 로컬 개발 환경 전체 기동 (PostgreSQL → 백엔드 → 프론트엔드)
---

이 프로젝트의 로컬 개발 환경을 순서대로 기동해줘. 각 단계가 성공한 것을 확인한 뒤 다음으로 넘어간다.

### 1. PostgreSQL (5432)
```
docker compose up -d
```
`docker compose ps`로 컨테이너가 올라온 것을 확인한다. Docker Desktop이 꺼져 있으면 여기서 멈추고 알린다.

### 2. 백엔드 (Spring Boot, 8080)
`backend/`에서 `gradlew.bat bootRun` — 백그라운드 실행.

기동 시 `DataInitializer`가 스키마를 새로 만들고 `primary_data/official_teams_and_rosters.json`에서 팀·선수를 적재한다. 적재 완료 로그가 찍힐 때까지 기다린다.

### 3. 프론트엔드 (Vite, 5173)
`frontend/`에서 `npm run dev` — 백그라운드 실행.
`node_modules`가 없으면 먼저 `npm install`.

### 마무리
http://localhost:5173 을 알려준다.
중간에 실패하면 그 단계에서 멈추고 실패한 로그를 보여준다. 다음 단계로 넘어가지 않는다.
