# 중간 보고서: 권역별 최신 대회 출전 전수 팀(73개 팀) 구축 및 로드 완료

## 1. 개요 및 변경 배경
* **사용자 요구사항**:
  * "그냥 제일 최근 대회에 참가한 권역별 팀 pws pcl emea amer apac 모든 팀을 다 넣어줘 예를 들어 pws2026 상반기에 참가한 팀이 24팀이라면 그 팀을 모두 넣는거야"
* **실행 내역**:
  * 최신 메이저 16팀 슬롯 제한을 해제하고, 각 권역별(PWS 한국, PCL 중국, EMEA 유럽, APAC 아시아태평양, AMER 아메리카) 최신 대회에 참가한 **모든 공식 프로팀 및 출전 팀(총 73개 팀)**을 전수 추출 및 전면 적재 완료.

---

## 2. 권역별 수집 및 적재 팀 현황 (총 73개 팀)

### 🇰🇷 1. PWS (대한민국 - 31개 팀)
* Gen.G Esports, DN SOOPers, T1, Crazy Raccoon, FN Pocheon, AZLA PENTAGRAM, Eagle Owls, SGA Esports, GGWP Esports, NS Esports (농심 레드포스), AAA Esports, C5 Esports, PNKO Esports, KBR Esports, XF Esports, MHG Esports, DK Esports, BKL Esports, KX Esports, XGZ Esports, Hi Esports, YCZ Esports, TAG Esports, MAY Esports 외 7개 참가팀

### 🇨🇳 2. PCL (중국 - 24개 팀)
* 17Gaming, Petrichor Road, Four Angry Men, Weibo Gaming, Tianba Esports, NewHappy, Chance Top Gaming, DDT Esports, SMS Esports, JH Esports, MKL Esports, LNP Esports, OG Esports, PTG Esports, XYG Esports, Xtr Esports, BBT Esports, 722 Esports, 007 Esports, 77 Esports, Wac Esports, JRG Esports, GH Esports, TYLOO

### 🇪🇺 3. EMEA (유럽/중동 - 9개 팀)
* Twisted Minds, Team Liquid, Geekay Esports, Natus Vincere, FaZe Clan, HOWL Esports, Entropiq, Acend Club, BBL Esports

### 🌏 4. APAC (아시아태평양 - 7개 팀)
* CERBERUS Esports, Geek Fam, Made in Thailand, The Expendables, Daytrade Gaming, Attack All Around, All Gamers

### 🇺🇸 5. AMER (아메리카 - 2개 팀)
* Soniqs, TSM

---

## 3. 검증 결과
* 백엔드 Spring Boot `/api/teams` 카운트: **73개 팀 정상 서빙 확인 (Status 200 OK)**
* 프론트엔드 React Vite 빌드: **성공 (3.04s, 0 errors)**
