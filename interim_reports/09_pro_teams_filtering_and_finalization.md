# 중간 보고서: 대한민국 PWS 공식 시드 8대 정규 프로팀 최종 정제 및 적재 완료

## 1. 개요 및 변경 사항
* **사용자 요청**:
  * "그럼 정규프로팀을 제외한 나머지 팀을 다 삭제해줘"
* **실행 내역**:
  * 아마추어/챌린저스 및 해체 구단을 모두 제외하고, 크래프톤 공식 시드를 부여받은 **대한민국 PWS 8대 정규 프로팀 및 100% 팩트 로스터**만 선별 정제.
  * 백엔드 Spring Boot DB 및 프론트엔드 React에 8개 정규 프로팀 전면 적재 완료 (`/api/teams` count: 8).

---

## 2. 최종 확정된 PWS 8대 공식 정규 프로팀 및 로스터
1. **Gen.G Esports (GEN)**: seoul (조기열), Salute (우제현), BeaN (오원빈), diyy (대니얼 노)
2. **DN SOOPers (DNS)**: Gyumin (심규민), Heaven (김태성), DIEL (김진현), REX (김해찬)
3. **T1 (T1)**: Rain1ng (김종명), EEND (노태영), Heather (차지훈), Type (이재원)
4. **Crazy Raccoon (CR)**: Inonix (나희주), Pio (차승훈), Glaz (윤성빈), Gyuyeon (최규연)
5. **FN Pocheon (FN)**: Starlord (이종호), kkachi (배호진), BreaKers, Hush
6. **AZLA PENTAGRAM (AZLA)**: F1ame, HAMMER, Orca, redzone
7. **Eagle Owls (EOS)**: DK, HongGilDong, Jaechan, Right
8. **SGA Esports (SGA 인천)**: Hane, Xantast, Innate, inforyou

---

## 3. 검증 결과
* 백엔드 `/api/teams` 응답: 8개 정규 프로팀 정상 서빙 (Status 200 OK).
* 프론트엔드 Vite build: 성공 (2.74s, 0 errors).
