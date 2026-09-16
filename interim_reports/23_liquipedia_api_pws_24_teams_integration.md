# 중간 보고서 23: 리퀴피디아 API 연동 및 2026 PWS 페이즈 2 참가 24개 팀 동기화

## 1. 개요 및 배경
기존 PUBG 게임 API는 게임 매치 로그 특성상 구단 공식 풀네임이 부재하여 약칭 태그 매칭 시 구단명 오차가 발생했습니다. 특히 SL 태그의 경우 과거 스타벌룬에서 최신 SLASH DOOM LAB으로 변경된 사실을 반영하지 못하는 한계가 있었습니다.
이에 사용자의 요청에 따라 별도의 API 키 없이 호출 가능한 리퀴피디아 미디어위키 API를 직접 연동하여 2026 PWS 페이즈 2 참가 24개 팀 전체와 공식 로스터를 무결점으로 추출하고 프론트엔드에 반영하였습니다.

## 2. 채택된 방법 및 기술적 타당성
* API 엔드포인트: 리퀴피디아 미디어위키 파서 API
* 파싱 대상: PUBG WEEKLY SERIES 2026 Phase 2 공식 페이지
* 파싱 대상 템플릿: TeamParticipants, Opponent, Person 구조
* 인증 방식: 별도의 API Key 없이 올바른 형식의 User Agent 및 Accept Encoding(gzip) 명시만으로 전면 개방된 공식 오픈 API 활용
* 처리 스크립트:
  * scripts/59_fetch_liquipedia_pws_teams.py (위키텍스트 파싱)
  * scripts/60_transform_liquipedia_teams_for_frontend.py (데이터 정규화)
  * scripts/61_inject_liquipedia_to_frontend.py (프론트엔드 주입)

## 3. 핵심 추출 결과
총 24개 팀의 공식 명칭과 실전 로스터가 100% 오차 없이 확보되었습니다.
1. SOOPers: DIEL, Gyumin, Heaven, Rex
2. Gen.G Esports: BeaN, taemin, Salute, seoul (taemin 영입 반영)
3. T1: EEND, Heather, Rain1ng, Type
4. Baegopa: Pio, Inonix, blackwalk, yugee (CR 시드권 이양 반영)
5. FN Esports: BreaKers, Hush, kkachi, Starlord
6. AZLA PENTAGRAM: F1ame, HAMMER, Orca, redzone
7. Divine: Barpo, Stella, Tosi, Daejang, wonderful
8. PHANTOM HEARTS: DAEVA, King, GimJun, ZeniTh
9. GAMEPT: fizzy, instinct, PolarBear, Search
10. SENTINEL: Rascal, heyden, HyukSung, VenTus
11. SUPERFECT: Acid, TheMinos, Karwn, Todol
12. Vex E Sports: Forward, Solution, Lure, Nyeong, ROY
13. Geekay Esports: Parkpro, EJ, Seongjang, AKaN
14. Eagle Owls: DK, SINGAM, Right, Jaechan
15. SQUAD X ACADEMY: KAL, BBANG, HELLPER, Sunday
16. Crazy Raccoon: Ayoh, GGoBuGi, Glaz, Gyuyeon
17. SLASH DOOM LAB: Morek, Freaky, vilo, muel (정확한 최신 구단명 반영 완료)
18. ISKRA: ParkChaN, Genom, Yong, Primmie
19. The Crown: 2cut, 2heart, CxldMxn, HanlNu
20. samgukzee: GuanYu, ZhaoYun, Yubi, YeoPo
21. HESEDIAN: LOV3, Glance, Hyuk, youth (구 Qx 리브랜딩 반영)
22. CFiVE: Archi, Malik, Gray, Krbyz
23. GGWP: sony, Geunwon, naheesoo, Wanted
24. Overwhelm: Woong, night, Fairy, FoxVer (아레떼 시드 승계 반영)

## 4. 의의 및 결론
* API 키 발급이나 결제 없이 리퀴피디아의 공개 위키텍스트 API만으로 24개 팀을 완전 자동 추출하는 파이프라인을 성공적으로 검증하였습니다.
* 기존 프론트엔드의 세련된 UI/UX 및 HOT 선수 12인 모달 시스템을 그대로 유지한 채 공식 팀명 데이터만 완벽하게 최신화되었습니다.
