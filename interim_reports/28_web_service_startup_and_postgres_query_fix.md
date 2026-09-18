# 웹 서비스 구동 및 PostgreSQL 쿼리 바인딩 개선

## 개요
로컬 개발 환경에서 전체 시스템을 정상 구동하고 사용자 브라우저에 웹사이트를 띄우기 위한 절차를 수행함.
구동 과정에서 발생한 데이터베이스 쿼리 파라미터 타입 추론 오류를 분석하고 명시적 분기 방식으로 개선함.

## 수행 작업 및 조치 내용

1. 데이터베이스 컨테이너 구동
• Docker Desktop 프로세스 가동 확인 및 백그라운드 구동
• PostgreSQL 16 기반 pubg_postgres 컨테이너 5432 포트 정상 활성화

2. 백엔드 기동 및 PostgreSQL 호환성 패치
• 백엔드 Spring Boot 3.2.3 서버 구동 중 /api/players 조회 시 500 에러 감지
• 원인: 기존 PlayerRepository 쿼리에서 null 파라미터가 바인딩될 때 PostgreSQL 드라이버가 bytea 타입으로 추론하여 lower(bytea) 함수 부재 오류 발생
• 조치:
  • PlayerRepository: 검색 조건별 명시적 전용 쿼리 메서드(findAllWithTeam, findByTeamIdWithTeam, searchByQueryWithTeam, searchByTeamIdAndQueryWithTeam) 분리
  • PlayerService: teamId와 query 파라미터의 존재 여부에 따라 조건별 메서드를 명시적으로 분기 호출하도록 개선
• 결과: 296명의 선수 목록 데이터 정상 반환 및 200 OK 응답 확인

3. 프론트엔드 구동 및 연동 검증
• React 18 및 Vite 5 개발 서버를 5173 포트로 구동
• Vite 프록시(/api -> localhost:8080)를 통한 데이터 연동 정상 확인 (296명 데이터 수신)
• 사용자 기본 웹 브라우저를 통해 http://localhost:5173 사이트 자동 오픈 완료

## 검증 결과
• 백엔드 API 상태: HTTP 200 OK
• 프론트엔드 서버 상태: HTTP 200 OK
• 선수 데이터 수신: 총 296명 정상 로드
