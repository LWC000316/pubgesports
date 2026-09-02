# 중간 보고서: PUBG ESPORTS 탭 전환, 15스텝 감도 가이드 통합 및 세부 대회별 탭 개편

## 1. 개요 및 반영 요구사항

사용자의 요청에 따라:
1. **메뉴 구조 대개편**:
   * 기존 `TEAMS & ROSTERS` $\rightarrow$ **`PUBG ESPORTS`** 탭으로 명칭 변경
   * 기존 `LEADERBOARD`, `SENS CONVERTER` 상단 탭 완전 삭제
2. **권역별 팀 & 로스터 무결점 구축**:
   * PWS, PCL, EMEA, AMER, APAC 각 권역별 2026 실제 활성 프로팀과 정확한 소속 선수(100% 팩트) 주입
3. **PUBG 15스텝 감도 법칙 인라인 가이드 배치**:
   * `PUBG ESPORTS` 뷰 상단에 15스텝 감도 법칙(400 DPI ↔ 800 DPI ↔ 1600 DPI 변경 시 감도 15 증감) 설명 배너 및 퀵 환산기 배치
   * 각 선수 카드에 15스텝 동등 환산 감도 요약 칩 제공
4. **토너먼트 세부 대회 탭 분할**:
   * **`PGS`**, **`PGC`**, **`EWC`**, **`PNC`**, **`PWS`**, **`PCL`**, **`APAC`**, **`전체(ALL)`** 탭으로 대회별 독립 탐색 환경 구축

---

## 2. 파일 수정 내역

* [primary_data/official_teams_and_rosters.json](../primary_data/official_teams_and_rosters.json): 2026 검증된 권역별 팀/로스터 데이터베이스
* [frontend/src/components/Header.jsx](../frontend/src/components/Header.jsx): `PUBG ESPORTS`, `TOURNAMENTS` 2개 핵심 탭으로 메뉴 간소화
* [frontend/src/components/TeamRosterView.jsx](../frontend/src/components/TeamRosterView.jsx): 상단 15스텝 감도 가이드 배너 및 선수 카드별 15스텝 환산 요약 칩 적용
* [frontend/src/components/TournamentView.jsx](../frontend/src/components/TournamentView.jsx): PGS, PGC, EWC, PNC, PWS, PCL, APAC 세부 탭 분할 뷰 완성
* [frontend/src/data/mockData.js](../frontend/src/data/mockData.js): 2026 공식 대회 및 권역 리그 데이터 동기화

---

## 3. 검증 결과
* Vite 프론트엔드 `build` 성공 (2.40s, 0 errors).
