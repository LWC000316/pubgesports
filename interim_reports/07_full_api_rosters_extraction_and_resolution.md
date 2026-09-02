# 중간 보고서: 공식 API 기반 전 세계 71개 프로팀 및 로스터 전수 자동 추출 완료

## 1. 개요 및 문제 해결
* **기존 문제**:
  * 특정 팀(17Gaming 등)의 로스터가 수동 정제 과정에서 누락되거나 일부만 들어가는 현상 발생.
* **원인 분석**:
  * 공식 API에 `GET /teams` 엔드포인트가 없어서 매치 텔레메트리(`GET /matches/{id}`)를 순회 파싱해야 하는데, 이전 표본 추출(3개 매치)로 인해 전체 팀 전수 수집이 되지 않았음.
* **해결 조치**:
  * [scripts/20_full_extract_all_teams_from_api.py](../scripts/20_full_extract_all_teams_from_api.py)를 구축하여 PGS, PWS, PCL, EWC, PNC 등 주요 권역/세계 대회의 매치를 전수 순회.
  * 크래프톤 공식 API에 출전한 **총 71개 공식 프로팀 및 284명 이상의 실출전 선수 닉네임**을 100% 코드로 자동 추출.
  * 백엔드 Spring Boot 및 프론트엔드 React에 71개 전체 팀을 전면 적재 완료 (`/api/teams` count: 71).

---

## 2. 주요 추출 팀 및 공식 로스터 팩트
* **17Gaming (17)**: Lilghost, WenBo, tiantian, xwudd
* **Gen.G Esports (GEN)**: seoul, Salute, BeaN, diyy
* **DN SOOPers (DNS)**: Gyumin, Heaven, DIEL, REX
* **T1 (T1)**: Rain1ng, EEND, Heather, Type
* **Twisted Minds (TWIS)**: BatulinS, Lu, Perfect1ks, xmpl
* **Petrichor Road (PeRo)**: Cui71, MMing, i26v6, 04NB
* **Four Angry Men (4AM)**: HSmm, Shen, SpaceMan, WINDah
* **Team Liquid (TL)**: CowBoi, PurdyKurty, aLOW, luke12
* **Geek Fam (GK)**: AKaN, EJ01, Parkpro, Seongjang
* **Natus Vincere (NAVI)**: Feyerist, Hakatory, boost1k-, spyrro
* **PNC 국가대표팀들**: 대한민국(KOR), 중국(CHN), 미국(USA), 베트남(VIE) 등 총 71개 팀
