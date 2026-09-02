# 중간 보고서: 공식 PUBG Developer API 백엔드 파이프라인 구축 및 주요 권역/세계 대회 전면 개편

## 1. 개요 및 배경

사용자의 요청에 따라:
1. 크래프톤 공식 **PUBG Developer API (`developer.pubg.com`)**와 통신하는 백엔드 연동 클라이언트 및 REST API 구축
2. 토너먼트 범위를 **주요 권역 대회(PWS 한국, PCL 중국)** 및 **주요 세계 대회(PGS, PGC, PNC, EWC)**로 한정하여 필터링 및 리더보드 연동
3. 2026 최신 활성 팀(Gen.G Esports, DN SOOPers, T1 등)과 연계된 프론트엔드 UI/UX 대개편 완료

---

## 2. 작업 상세 내역

### 1) 백엔드 공식 API 연동 모듈
* [backend/src/main/resources/application.yml](../backend/src/main/resources/application.yml): `pubg.api` 설정 및 허용 토너먼트(`PWS`, `PCL`, `PGS`, `PGC`, `PNC`, `EWC`) 등록
* [backend/src/main/java/com/pubg/esports/service/PubgOfficialApiService.java](../backend/src/main/java/com/pubg/esports/service/PubgOfficialApiService.java): 공식 API 통신 및 PWS/PCL/PGS/PGC/PNC/EWC 선별 필터링 서비스 구현
* [backend/src/main/java/com/pubg/esports/controller/PubgTournamentController.java](../backend/src/main/java/com/pubg/esports/controller/PubgTournamentController.java): `/api/tournaments/official` REST 컨트롤러 제공
* Gradle `compileJava` 성공 검증 완료 (0 errors).

### 2) 프론트엔드 UI/UX 대개편
* [frontend/src/data/mockData.js](../frontend/src/data/mockData.js): 2026 공인 세계 대회(PGS 9, EWC 2026, PNC 2026, PGC 2026) 및 권역 리그(PWS 2026, PCL 2026) 데이터셋 확충
* [frontend/src/components/TournamentView.jsx](../frontend/src/components/TournamentView.jsx):
  * 상단 카테고리 탭: **"🌍 세계 대회 (PGS, PGC, PNC, EWC)"** vs **"🏛️ 주요 권역 대회 (PWS 한국, PCL 중국)"**
  * 선택된 대회 상세 카드 및 공식 우승팀(2026 PGS 9 젠지 우승 등) 챔피언 배너 노출
  * 공식 토너먼트 종합 리더보드 순위표 실시간 렌더링
* Vite 프론트엔드 `build` 성공 검증 완료 (2.52s).
