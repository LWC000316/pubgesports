# HANDOFF — 2026-09-29

리그 6개 **전부 수집 완료**(146팀 685명). 트로피 제거와 시드 라벨 정정까지 끝났다.

---

## 1. 현재 상태

팀 목록은 **구획 없이 한 줄기**로 나온다. 프로로 볼 수 있는 구단이 앞, 아마추어가 뒤.
구획 제목도 구분선도 없다.

| 탭 | 대회 | 팀 | 상단 / 하단 | 상단이 근거하는 것 |
|---|---|---|---|---|
| PWS | 2026 Phase 2 (한국) | 24 | 13 / 11 | 위키의 `text=Pro Seed` |
| PCL | 2026 Autumn Stage S (중국) | 24 | 8 / 16 | Stage S 직행 시드 |
| EMEA | 2026 Fall | 29 | 9 / 20 | Global·Regional Partner, PGS Attending |
| AMER | 2026 Series 2 | 29 | 7 / 22 | 동일 |
| PVS | 2026 Phase 2 (베트남) | 16 | 3 / 13 | 직전 Phase 1 파이널 1~3위 |
| PTS | 2026 Phase 1 (태국) | 24 | 20 / 4 | **없음** — 순서에 실질적 의미 없음 |

### 이번에 고친 것

**1. `seedType` 의 의미를 바로잡았다.** `pro`/`amateur` 는 프로 여부가 아니라
**본선 진입 경로**(직행 / 예선 통과)다. `--seed-from-qualification` 이 `invite→pro`,
`qual→amateur` 로 기계적으로 매핑했는데 **그 규칙은 PWS 에서만 참**이었다. 결과적으로
PTS 는 근거 없이 20팀이 프로가 되고, PVS 는 **컵 1위 팀이 아마추어로** 들어가 있었다.
그룹에 이름을 붙이려는 시도를 두 번 했고 두 번 다 위키가 뒷받침하지 않는 주장을
만들어냈다. 결국 **구획을 없애고 순서로만 구분**하기로 했다.

**2. 트로피를 제품에서 제거했다.** `TeamCard.jsx` 가 애초에 렌더하지 않아 이미 죽은
데이터였다. 엔티티·DTO·적재 루프·시드 필드·ingest 로직을 모두 지웠다.
`scripts/66·68·69` 와 보고서 25·26·29 는 **감사 기록으로 남겼다.**

**3. PVS 태그 오류 2건.** `Trần Long KingSky → TRAN LONG KINGSKY` (발음부호 때문에
"코드==팀명" 검사가 통과해버림), `The Daredevil Team → TDT ESPORTS` (약칭이 아니라
다른 표기명). 둘 다 비웠고 `code_to_tag()` 의 비교를 발음부호 제거 후 하도록 고쳤다.

---

## 2. 진행 중인 일

**없음.** 작업 트리 깨끗.

실행 중일 수 있는 것: Docker(`pubg-postgres`), 백엔드 8080, Vite 5173.

---

## 3. 다음 할 일

### 우선순위 1 — 진행 중 대회 재수집
- **EMEA·AMER**: 2026-10-04 종료 예정. 둘 다 대회 중에 수집한 것이라 종료 후 다시 돌려야 한다

**PVS 는 재수집 대상이 아니다.** Week 3·4 가 `finished=` 로 비어 있지만 미진행이 아니라
2주차까지만 치르고 끝난 대회다(사용자 확인). 참가 16팀 확정.
절차는 `ingest/README.md` 와 동일하되, **`--seed-from-qualification` 결과를 그대로
믿지 말고 그 리그의 `text=` 값을 직접 확인**할 것.

### 우선순위 2 — 선수 감도·장비 (디스코드 수집 대기)
`ddl-auto: create` 아래에서는 런타임에 쓴 데이터가 재기동 때 사라진다.
**API 가 아니라 시드 파일로 들어와야 한다.**
현재 PWS 96명의 `800/32/동일 마우스`는 `scripts/60` 이 일괄 주입한 **가짜값**이다.
실측이 들어오면 함께 정리한다.

### 우선순위 3 — PUBG API 키 (사용자 조치)
`setx PUBG_API_KEY` 로 저장돼 있고 호출도 **HTTP 200** 확인. 다만 Claude Code
세션에서는 안 잡힌다 — **터미널 창을 완전히 닫고 새로 열어야** 한다(`/exit` 만으로는 부족).
현재 작업에는 이 키가 필요 없다.

옛 키가 커밋 `ba3a8d5` 히스토리에 잔존한다. Private 저장소라 급하지 않으나 재발급 권장.

### 우선순위 4 — 미룬 정비
`/api/tournaments/{id}` 가 404 대신 500, 로고 이미지 최적화(`vex.png` 1.6MB 등),
`README.md` 재작성, LICENSE 없음, 테스트 0개.

---

## 4. 관련 파일

- `ingest/README.md` — 리그 추가 절차와 **리그별 시드 근거 표**
- `ingest/build_league_seed_mediawiki.py` — 수집기 (키 불필요)
- `primary_data/*_teams_verified.json` — 리그별 확정 시드 (손으로 편집 가능)
- `CLAUDE.md` — 매 세션 자동 로드
- `frontend/src/components/players/PlayersTab.jsx` — `LEAGUES` 배열이 탭 정의
- `frontend/src/components/players/LeagueTeamGrid.jsx` — `SEED_ORDER` 가 목록 순서
- `backend/.../config/DataInitializer.java` — `VERIFIED_SEEDS` 목록

---

## 5. 주의사항

### 데이터 성격
- **수집한 로스터는 "대회 시점" 기준이다.** 이적이 반영되지 않으며 그게 의도다
- **자동 갱신 시스템은 없다.** 스케줄러 0건. 바꾸려면 스크립트를 다시 돌린다
- **선수 세팅은 PWS 만 값이 있고 그마저 가짜다.** 나머지는 `미등록` 이 뜬다. 이게 올바른 상태다

### 리그별 차이 (다음 리그에서도 나올 수 있다)
- 위키 코드가 **약칭인 리그**(PCL: `jdg`)와 **팀 이름 그대로인 리그**(EMEA: `Natus Vincere`)가 있다
- 위키 코드는 **ASCII 로만 적히는 일이 잦다**(PVS: `Tran Long KingSky` vs `Trần Long KingSky`)
- 참가팀이 **Stage 소절로 나뉘는 대회**(PCL)가 있다. `--seed-map` 으로 골라내야 한다
- 동명 팀은 문서명이 `ZEAL (Chinese team)` 이 된다. 접미사를 뗀다
- 위키 원문은 **팀 이름이 아니라 내부 코드**를 준다. 정식명은 렌더된 HTML 에서만 얻는다
- 선수 필터는 `type=staff` 뿐 아니라 **`role=` 이 붙은 항목 전부**를 제외한다

### 코드 함정
- **`ddl-auto: create`** — 재기동마다 DB 전멸 후 시드 재적재
- **엔티티를 지워도 테이블은 안 지워진다.** Hibernate 가 모르는 테이블은 드롭 대상이 아니다.
  트로피 제거 때 `team_trophies` 가 고아로 남아 수동 `DROP TABLE` 했다
- **기동 레이스** — `DataInitializer` 가 웹 서버 뒤에 실행된다. 준비 확인은 **기대 팀 수**로
- **PostgreSQL null 파라미터** — JPQL 에 nullable 바인딩 금지
- **컬렉션 2개 동시 fetch join 금지** (`MultipleBagFetchException`)
- **`seedType IS NOT NULL`** — 팀 카드 조회 필수 조건
- **`seedType` 이 null 이면 팀이 사라진다** (`seedType IS NOT NULL` 필터). `pro`/`amateur`
  외의 값은 목록 맨 뒤로 밀린다 (`SEED_ORDER` 기본값 9)

### 협업
- 한국어로 소통한다
- **지시하지 않은 작업을 임의로 진행하지 말 것**
- 비자명한 작업은 **계획을 먼저 보고하고 승인받는다**
- **모르거나 애매하면 물어본다**
- **조사 결과를 그대로 믿지 말 것.** 수치는 원본으로 확인한다.
  이번 seedType 오류는 **사용자가 화면을 보고 먼저 감지**했다 — 자동 매핑 결과를
  검증 없이 여섯 리그에 그대로 적용한 것이 원인이다

---

**이어받는 법**: `claude -c` (같은 폴더에서), 또는 `/clear` 후 `@HANDOFF.md`.
