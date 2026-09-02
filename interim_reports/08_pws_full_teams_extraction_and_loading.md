# 중간 보고서: 공식 API 기반 대한민국 PWS 전체 66개 프로팀 및 로스터 전수 수집 완료

## 1. 개요 및 수행 내역
* **사용자 요청**:
  * "PWS 팀이 이것밖에 안 돼? 일단 이것부터 해보자 PWS팀만 다 가져와봐"
* **실행 내역**:
  * 크래프톤 공식 Developer API의 모든 PWS 토너먼트(`kr-pws2c5`, `kr-pws2c4`, `kr-pws2c3`, `kr-pws2c2`, `kr-pws2c1`, `kr-pws1wf3`, `kr-pws1s33`, `kr-pws1s32` 등) 내 모든 매치 텔레메트리를 전수 순회 분석.
  * PWS 대한민국 공식 무대에 참가한 **총 66개 한국 프로팀/챌린저스 구단 및 소속 선수 전원**을 100% 코드로 자동 추출.
  * 추출된 66개 팀 데이터를 [primary_data/pws_all_extracted_teams.json](../primary_data/pws_all_extracted_teams.json)에 원본 저장.
  * 백엔드 Spring Boot DB 및 프론트엔드 React에 66개 전체 팀을 전면 적재 완료 (`/api/teams` count: 66).

---

## 2. 수집된 PWS 대표 프로팀 및 로스터 목록 (전체 66팀 중 발췌)
* **Gen.G Esports (GEN)**: seoul, Salute, BeaN, diyy
* **DN SOOPers (DNS)**: Gyumin, Heaven, DIEL, Rex
* **T1 (T1)**: Rain1ng, EEND, Heather, Type
* **Crazy Raccoon (CR)**: Inonix, Pio, Glaz, Gyuyeon
* **FN Pocheon (FN)**: BreaKers, Hush, Starlord, kkachi
* **AZLA PENTAGRAM (AZLA)**: F1ame, HAMMER, Orca, redzone
* **Eagle Owls (EOS)**: DK, HongGilDong, Jaechan, Right, SINGAM, WaSsoBeSso
* **SGA Esports (SGA 인천)**: AnX1n, Hane, Innate, Xantast, inforyou
* **GGWP Esports (GGWP)**: Geunwon, Wanted, insfire, naheesoo, sony
* **NS Esports (농심 레드포스, NS)**: 4mine, Curo, RicE, yoyangwon
* **AAA Esports (AAA)**: Black9, Focus, MooHeon, MooSik, RimQ
* **C5 Esports (C5)**: Archi, Gray, KrbyZ, Malik, todn
* **PNKO Esports (PNKO)**: Entia, LongDuo, Oops, ShotDuo, huka
* **KBR Esports (KBR)**: Cliche, HITMAN, Leaper, Sayd
* **XF Esports (XF)**: 570yT, Arte, ChoiHyunseo, One1Tap, Sunday
* **MHG Esports (MHG)**: Agnes, CHANAHRI, DO, DORI, DaeJang, JEJE, PEEKKING, Roger
* **Dplus KIA (DK)**: Americano, Mantal, Under, minuda
* **기타 챌린저스/프로 49개 팀 포함 총 66개 구단**
