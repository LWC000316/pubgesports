# 중간 보고서 24: PWS UI/UX 공식화 리팩토링 및 시드별 분리 완료

## 1. 개요
사용자 요청에 따라 PWS 화면의 모든 비공식적 안내 문구와 부가적인 한국어 텍스트를 제거하고, 글로벌 공식 e스포츠 대회 규격의 프로페셔널한 UI/UX로 전면 개편하였습니다.

## 2. 주요 개선 내역

### 1) 텍스트 정제 및 공식화
* (공식 PUBG e스포츠 API 실시간 검증 로스터 반영) 등 불필요한 부가 설명 문구 전면 제거
* 각 팀별 설명(description) 텍스트 제거
* 팀명 옆 한국어 표기(koreanName) 제거, 국제 공식 영문 구단명만 단독 노출
* 순위 표기(#1위, #2위 등) 제거 (대회 개막 전/중 팀 프로필 본연의 역할에 집중)

### 2) 대회 및 팀 로고 시스템 구축
* 상단 대회 탭 칩(PWS, PCL, EMEA, AMER, APAC)에 리퀴피디아 고화질 공식 다크모드 대회 로고 이미지 삽입
* 각 팀 카드 좌측 상단 사진란에 리퀴피디아 공식 고해상도 구단 로고 이미지(DN SOOPers, Gen.G, T1, Baegopa, FN, AZLA, Crazy Raccoon 등) 탑재
* 이미지 로드 지연 또는 부재 시 팀 고유 태그(TAG) 엠블럼으로 자연스럽게 fallback 처리

### 3) 프로 시드와 아마추어 및 예선 시드 분리
* 2026 PWS Phase 2 공식 규정에 따라 24개 팀을 두 개의 명확한 섹션으로 분리
  * Pro Seeds (프로 시드 13개 팀): DN SOOPers, Gen.G Esports, T1, Baegopa, FN Esports, AZLA PENTAGRAM, Divine, PHANTOM HEARTS, DAEJEON GAME PT, SENTINEL, SUPERFECT, Vex E Sports, Geekay Esports
  * Amateur & Qualifier Seeds (아마추어 및 컵대회 예선 진출 11개 팀): Eagle Owls, SQUAD X ACADEMY, Crazy Raccoon, SLASH DOOM LAB, ISKRA, The Crown, samgukzee, HESEDIAN, CFiVE, GGWP, Overwhelm

## 3. 검증 결과
* npm run build 결과 1476개 모듈이 에러 없이 완벽히 빌드됨
* 실시간 개발 서버(/)에서 변경된 공식 UI/UX가 정상 서비스 중임