# 중간 보고서 25: 로컬 공식 로고 호스팅 및 대회 우승 트로피 뱃지 시스템 구축

## 1. 개요
기존에 외부 리퀴피디아 이미지 URL을 직접 참조할 때 브라우저의 핫링크 방지(Referer 차단)로 인해 로고 이미지가 화면에 출력되지 않는 현상이 발생했습니다.
이에 대회 로고 및 팀 로고 고화질 에셋을 로컬 정적 디렉터리(frontend/public/logos)로 직접 다운로드하여 100% 로컬 호스팅 체계로 전환하였고, 각 팀별 공식 대회 우승 트로피 뱃지 및 시드 구분을 완벽하게 개편하였습니다.

## 2. 세부 구현 및 개선 내역

### 1) 대회 및 팀 로고 로컬 정적 호스팅 구축
* 대회 로고 (PWS, PCL, EMEA, AMER, APAC)를 frontend/public/logos/tournaments에 보관
* 주요 참가팀 로고 (DN SOOPers, Gen.G, T1, Baegopa, FN, AZLA, Divine, PHANTOM HEARTS, GAMEPT, SENTINEL, SUPERFECT, Geekay, Eagle Owls, Crazy Raccoon, SLASH DOOM LAB, GGWP, Overwhelm 등)를 frontend/public/logos/teams에 다운로드하여 로컬 서빙
* 로고가 없는 신생 팀은 고유 태그(TAG) 엠블럼으로 자연스럽게 fallback 렌더링

### 2) 우승 대회 및 트로피(Trophy) 뱃지 시스템
* 기존의 단순한 태그 및 시드 텍스트를 제거하고, 각 구단이 공식 대회에서 획득한 우승 타이틀(Championships)을 트로피 뱃지로 구성
  * Gen.G Esports: PGC 🏆x2, PWS 🏆x3
  * DN SOOPers: PGC 🏆x1, PWS 🏆x4
  * T1: PWS 🏆x1, PKL 🏆x1
  * AZLA PENTAGRAM: PWS 🏆x1, BSC 🏆x2
  * Baegopa: PWS 🏆x1
  * Geekay Esports: PWS 🏆x1
  * Crazy Raccoon: PWS 🏆x1
  * DAEJEON GAME PT: BSC 🏆x1
  * FN Esports: BSC 🏆x1
  * 우승 기록이 없는 신생/예선 통과 팀: CHALLENGER 뱃지 표시

### 3) 시드 헤더 명칭 및 아이콘 정밀화
* 프로 시드 섹션: Crown(황금 왕관) 아이콘과 함께 Pro Seeds (13) 공식 표기
* 퀄리파이어 시드 섹션: Target(타겟/조준선) 아이콘과 함께 Qualifier Seeds (11) 공식 표기

## 3. 검증 결과
* 로컬 이미지 엔드포인트(/logos/tournaments/pws.png, /logos/teams/geng.png 등)에 대한 HTTP GET 요청 시 정상 200 OK 반환 확인
* npm run build 통과 및 브라우저 정상 렌더링 검증 완료
