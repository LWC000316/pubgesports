# 중간 보고서: 권역별 팀 및 로스터 시스템 개편 및 PUBG 15스텝 감도 계산기 구축

## 1. 개요 및 배경

기존 시스템은 전체 선수를 단순 카드 박스로 나열하는 평면적 구조였으며, 배틀그라운드 유저들의 직관적 탐색을 지원하지 못했습니다. 또한 배틀그라운드 실전에서 사용되지 않는 eDPI 지표가 포함되어 있었습니다. 이에 따라 권역별(PWS, PCL, EMEA, AMER, APAC) 리그 팀 기반 탐색 아키텍처로 전면 개편하고, 배그 프로 실전 15스텝 감도 법칙(400/800/1600 DPI 간 15 증감 법칙)을 전산화한 감도 변환기와 데이터 관리자(Admin) 기능을 구축하였습니다.

## 2. 수행된 작업 및 시스템 변경 내역

### 1) 백엔드 데이터 모델 및 REST API 확장
* [Team.java](../backend/src/main/java/com/pubg/esports/domain/Team.java): `league`(PWS/PCL/EMEA/AMER/APAC), `description`, `foundedYear`, `coach`, `achievements` 필드 추가
* [Player.java](../backend/src/main/java/com/pubg/esports/domain/Player.java) 및 [PlayerSetting.java](../backend/src/main/java/com/pubg/esports/domain/PlayerSetting.java): 세팅 및 프로필 업데이트 메서드 구현
* [AdminController.java](../backend/src/main/java/com/pubg/esports/controller/AdminController.java) 및 [AdminService.java](../backend/src/main/java/com/pubg/esports/service/AdminService.java): 신규 팀/선수/세팅/기어 등록 및 수정/삭제 CRUD REST API 엔드포인트 신설
* [DataInitializer.java](../backend/src/main/java/com/pubg/esports/config/DataInitializer.java): 권역별 14개 명문팀 및 20명 이상의 프로 선수 로스터 시드 데이터 주입

### 2) 프론트엔드 UI/UX 대개편
* [TeamRosterView.jsx](../frontend/src/components/TeamRosterView.jsx):
  * 권역 리그 셀렉터 (PWS 🇰🇷 / PCL 🇨🇳 / EMEA 🇪🇺 / AMER 🇺🇸 / APAC 🌏 / ALL)
  * 팀 박스 그리드 $\rightarrow$ 팀 상세 배너(전적, 코치, 창단연도) $\rightarrow$ 소속 로스터 카드 $\rightarrow$ 선수 클릭 시 상세 세팅 모달 3단계 탐색 구조
* [PlayerDetailModal.jsx](../frontend/src/components/PlayerDetailModal.jsx):
  * eDPI 게이지 및 계산 표시 완전 삭제
  * 400 / 800 / 1600 DPI 15스텝 환산 세팅 안내 추가
* [SensCalculator.jsx](../frontend/src/components/SensCalculator.jsx):
  * 배틀그라운드 전용 15스텝 감도 계산기 (400 DPI 감도 35 $\rightarrow$ 800 DPI 감도 20 $\rightarrow$ 1600 DPI 감도 5 환산)
  * 주요 프로 선수(Seoul, Salute, Inonix, TGLTN) 프리셋 원클릭 로드 기능
  * 발로란트/오버워치/에이펙스/CS2 $\rightarrow$ PUBG 감도 변환기 탑재
* [AdminModal.jsx](../frontend/src/components/AdminModal.jsx):
  * 웹 화면에서 신규 팀 및 선수 정보, 감도, 장비를 직접 등록할 수 있는 관리자 모달 구현
* [Header.jsx](../frontend/src/components/Header.jsx) 및 [App.jsx](../frontend/src/App.jsx):
  * 신규 탭 메뉴(`TEAMS & ROSTERS`, `TOURNAMENTS`, `LEADERBOARD`, `SENS CONVERTER`) 및 `ADMIN MANAGE` 버튼 연동

## 3. 검증 결과

* 프론트엔드 Vite 프로덕션 빌드 정상 완료 (`npm run build` 성공)
* 백엔드 Gradle 컴파일 정상 수행

## 4. 향후 확장 계획

* 외부 크롤러 소스 확정 시 실시간 리그 경기 결과 및 팀/선수 데이터 정밀 파싱 연동
* 관리자 기능을 통한 대회 매치별 세부 스코어보드 입력 지원
