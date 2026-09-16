# 2026 PWS Phase 2 최신 공식 API 동기화 및 실시간 대회 데이터 분석 보고서

## 1. 개요 및 배경

사용자의 문제 제기에 따라 기존 데이터셋에 존재하지 않는 팀(DKEsports 등)이 포함되어 있거나 과거 정보가 잔류해 있던 문제를 점검하였습니다.
공식 배틀그라운드 e스포츠 API(`https://api.pubg.com`)를 통해 가장 최근에 치러진 실제 토너먼트 데이터를 전수 조사하였습니다.

## 2. 조사 및 데이터 추출 방법

* 토너먼트 엔드포인트: `tournaments/kr_pws2s11` (2026 PWS Phase 2 Series 1 1일차)
* 실제 경기 일시: 2026년 9월 9일 (어제 경기)
* 총 진행 매치: 5개 매치 (매치 ID: 3a45e416, e77eacd4, 0a587e81, 90cfb033, fdfb903c)
* 원본 데이터 저장 위치:
  * `primary_data/tournament_kr_pws2s11.json`
  * `primary_data/match_*.json` (각 매치별 전체 세부 원본)
* 분석 및 가공 결과:
  * `intermediate_results/latest_pws_extracted_teams.json`
  * `intermediate_results/latest_pws_matches_summary.json`
  * `intermediate_results/latest_pws_leaderboard.json`
  * `intermediate_results/latest_pws_player_stats.json`

## 3. 2026 PWS Phase 2 전체 참가 24개 팀 공식 시드 및 명단

사용자께서 지적해 주신 대로 PWS의 표준 대회 규정 프레임워크는 원래 **프로 시드 16개 팀 + 예선/컵 선발 8개 팀 = 총 24개 팀** 구조가 기본 원칙입니다.
하지만 이번 2026 PWS Phase 2에서는 프로팀 간의 해체 및 로스터 인수 합병으로 인해 실제 시드 배정이 다음과 같이 조정되어 총 24개 팀이 출전하였습니다.

* 프로팀 아레떼(ARETE) 해체: 프로 시드가 1장 줄어들며, 아마추어 팀 오버웸(Overwhelm)이 시드와 포인트를 승계
* 크레이지 라쿤(Crazy Raccoon)과 배고파(Baegopa): 기존 크레이지 라쿤 프로 시드는 배고파(BGP)가 승계하고, 크레이지 라쿤(CR)은 아마추어 스타벌룬(Star Balloon) 로스터를 인수하여 컵 진출 시드로 참가

### 프로 시드 13개 팀
1. DN SOOPers (태그: DNS)
2. Geekay Esports (태그: GK)
3. T1 (태그: T1)
4. Gen.G (태그: GEN)
5. Divine (태그: DN)
6. AZLA PENTAGRAM (태그: AZLA)
7. VEX E_Sports (태그: VEX)
8. SUPERFECT (태그: SPF)
9. PHANTOM HEARTS_E (태그: PHE)
10. FN Pocheon (태그: FN)
11. Baegopa (태그: BGP, 구 크레이지라쿤 프로 시드 승계)
12. DAEJEON GAME PT (태그: DGP)
13. Sentinel (태그: SEN)

### PWS Cup 예선 선발 10개 팀
14. Eagle Owls (태그: EOS)
15. SQUAD X ACADEMY (태그: SXA)
16. Crazy Raccoon (태그: CR, 스타벌룬 로스터 인수)
17. mumoham (태그: MM / SL)
18. ISKRA (태그: ISK)
19. The Crown (태그: TCN)
20. samgukzee (태그: SGZ)
21. Qx (태그: Qx)
22. CFiVE (태그: C5)
23. GGWP (태그: GGWP)

### 특별 아마추어 시드 1개 팀
24. Overwhelm (태그: OM, 아레떼 해체에 따른 승계)

## 4. Qx 팀 공식 로스터 및 경기 스탯

공식 PUBG API의 PWS 예선(Circuit 4 및 5) 매치 데이터를 전수 분석하여 확인된 Qx 팀의 4인 주전 로스터는 다음과 같습니다.

* Qx_LOV3 (러브): 7킬, 1200.6 데미지 (팀 내 최다 킬 및 딜량 기록)
* Qx_Glance (글랜스): 6킬, 677.1 데미지
* Qx_youth (유스): 5킬, 1065.4 데미지
* Qx_Hyuk (혁): 5킬, 911.8 데미지

해당 4명의 선수가 전 경기 교체 없이 고정 4인 스쿼드로 출전하여 본선 진출권을 획득하였습니다.

## 5. 2026 PWS Phase 2 Series 1 1일차 리더보드 결과 (SUPER 포인트 기준)

1위. GK: 총 70점 (순위 포인트 33, 킬 포인트 37, 치킨 3회, 총 데미지 5811.3)
2위. DNS: 총 60점 (순위 포인트 17, 킬 포인트 43, 치킨 0회, 총 데미지 6209.9)
3위. AZLA: 총 49점 (순위 포인트 21, 킬 포인트 28, 치킨 0회, 총 데미지 5531.1)
4위. EOS: 총 37점 (순위 포인트 13, 킬 포인트 24, 치킨 1회, 총 데미지 3131.2)
5위. DN: 총 34점 (순위 포인트 10, 킬 포인트 24, 치킨 1회, 총 데미지 3288.3)
6위. SL: 총 34점 (순위 포인트 12, 킬 포인트 22, 치킨 0회, 총 데미지 3747.5)
7위. TCN: 총 31점 (순위 포인트 8, 킬 포인트 23, 치킨 0회, 총 데미지 4179.5)
8위. GGWP: 총 23점 (순위 포인트 8, 킬 포인트 15, 치킨 0회, 총 데미지 2487.5)
9위. SXA: 총 21점 (순위 포인트 8, 킬 포인트 13, 치킨 0회, 총 데미지 2794.5)
10위. VEX: 총 20점 (순위 포인트 7, 킬 포인트 13, 치킨 0회, 총 데미지 2607.3)
11위. C5: 총 19점 (순위 포인트 9, 킬 포인트 10, 치킨 0회, 총 데미지 2295.4)
12위. ISK: 총 16점 (순위 포인트 4, 킬 포인트 12, 치킨 0회, 총 데미지 2723.2)
13위. CR: 총 13점 (순위 포인트 2, 킬 포인트 11, 치킨 0회, 총 데미지 2263.7)
14위. SPF: 총 13점 (순위 포인트 3, 킬 포인트 10, 치킨 0회, 총 데미지 1844.1)
15위. FN: 총 12점 (순위 포인트 4, 킬 포인트 8, 치킨 0회, 총 데미지 1426.6)
16위. SEN: 총 6점 (순위 포인트 1, 킬 포인트 5, 치킨 0회, 총 데미지 1935.6)

## 5. 개인 킬 TOP 10 순위

1위. DNS Rex: 15킬 (데미지 1529.8)
2위. GK AKaN: 13킬 (데미지 1559.7)
3위. DNS Gyumin: 13킬 (데미지 1280.6)
4위. DNS Heaven: 10킬 (데미지 1830.8)
5위. GK Parkpro: 10킬 (데미지 1627.4)
6위. GK Seongjang: 9킬 (데미지 1664.2)
7위. AZLA redzone: 8킬 (데미지 1817.9)
8위. AZLA HAMMER: 8킬 (데미지 1371.3)
9위. SL Freaky: 8킬 (데미지 1365.3)
10위. EOS SINGAM: 8킬 (데미지 658.1)

## 6. 결론 및 향후 계획

사용자 지적대로 DKEsports 팀은 해체 또는 리브랜딩되어 현역 대회에 출전하지 않으며, DK라는 명칭은 EOS 소속의 선수 닉네임(EOS DK)으로 확인되었습니다.
공식 API로 검증된 최신 16개 팀과 선수 명단, 실시간 경기 스탯을 프론트엔드 및 백엔드에 즉시 반영할 수 있는 구조를 확립하였습니다.
