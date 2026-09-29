# HANDOFF — 2026-09-29

리그 6개 중 **4개 수집 완료**. 여기까지 전부 커밋·푸시됨 (`895d4ac`).

---

## 1. 완료한 일

### 리그 데이터 (이번 세션의 주 작업)

| 탭 | 대회 | 팀 | 구성 | 시드 구분 방법 |
|---|---|---|---|---|
| PWS | 2026 Phase 2 (한국) | 24 | pro 13 / am 11 | 시드 파일 직접 기록 |
| PCL | 2026 Autumn Stage S (중국) | 24 | pro 8 / am 16 | `seed_types_pcl.json` 수작업 |
| EMEA | 2026 Fall | 29 | pro 9 / am 20 | **자동** (`--seed-from-qualification`) |
| AMER | 2026 Series 2 | 29 | pro 7 / am 22 | **자동** (`--seed-from-qualification`) |

선수 합계 493명, 팀 로고 106개.

### 수집 도구 (`ingest/`)
- `mediawiki_client.py` — `liquipedia.net/pubg/api.php`. **API 키 불필요.** 연락처 포함 UA, gzip, 응답 캐싱, 호출 간 2초
- `build_league_seed_mediawiki.py` — 대회 문서 하나 → 시드 초안 + 로고 다운로드

**LPDB v3 키를 기다릴 필요가 없다는 것이 이번 세션의 핵심 발견이다.** 리퀴피디아에는 API 가 두 개이고, 기존 PWS 데이터도 키 없는 MediaWiki 경로로 들어온 것이었다.

### 탭 구조 변경
APAC 을 **PTS(태국)·PVS(베트남)** 로 분리. 탭은 `PWS / PCL / EMEA / AMER / PTS / PVS` 여섯 개.

### 대회 로고 정정
EMEA·APAC 로고가 **국기 이미지**였다(`scripts/65` 가 `Eu_hd.png` 144x96, `Asia-pacific_flag_hd.png` 36x24 를 하드코딩). EMEA 를 실제 로고(800x207)로 교체하고 PTS·PVS 를 새로 받았다. 참조가 사라진 `apac.png` 는 삭제.

---

## 2. 진행 중인 일

**없음.** 커밋·푸시 완료, 작업 트리 깨끗.

실행 중일 수 있는 것: Docker(`pubg-postgres`), 백엔드 8080, Vite 5173. 세션이 끝나면 백엔드·Vite 는 내려간다.

---

## 3. 다음 할 일

### 우선순위 1 — 남은 리그 2개
**여기서 재개하면 된다.** 절차는 EMEA·AMER 과 동일하다.

```bash
# PTS (태국) — 종료된 대회라 안전
python ingest/build_league_seed_mediawiki.py \
    --page "PUBG_Thailand_Series/2026/Phase_1" \
    --league PTS --region TH \
    --seed-from-qualification --include-subs --download-logos \
    --out intermediate_results/pts_seed_draft.json

python ingest/verify_seed.py intermediate_results/pts_seed_draft.json --compare-league PTS
# 사람이 원문 대조 → primary_data/pts_teams_verified.json 으로 확정
```

그다음 배선 2곳:
1. `DataInitializer.VERIFIED_SEEDS` 에 경로 한 줄
2. `PlayersTab.jsx` 의 해당 리그에 `bannerTitle` 과 `sourceUrl`

**PTS**: `PUBG_Thailand_Series/2026/Phase_1` (24팀, 2026-04-28 ~ 05-12 종료)
**PVS**: `PUBG_Vietnam_Series/2026/Phase_2` (16팀). **인포박스에 날짜가 비어 있어 시작 여부를 먼저 확인할 것.** 시작 전이면 참가팀이 확정되지 않았을 수 있다.

`--seed-from-qualification` 이 먹히는지는 돌려봐야 안다. 실패하면 `method` 가 없는 것이므로 PCL 처럼 구분표를 만들어야 한다.

### 우선순위 2 — EMEA·AMER 재수집
두 대회 모두 **2026-10-04 에 끝난다.** 진행 중에 수집했으므로 종료 후 다시 돌려야 최종 명단이 된다.

### 우선순위 3 — PUBG API 키 (사용자 조치)
`setx PUBG_API_KEY` 로 저장돼 있고 실제 호출도 **HTTP 200** 으로 확인했다. 다만 Claude Code 세션에서는 안 잡힌다 — **터미널 창을 완전히 닫고 새로 열어야** 한다(`/exit` 만으로는 부족). 지금 진행 중인 작업에는 이 키가 필요 없다.

옛 키가 커밋 `ba3a8d5` 히스토리에 잔존한다. Private 저장소라 급하지 않으나 재발급 권장.

### 우선순위 4 — 트로피
PWS 만 채워져 있고 PCL·EMEA·AMER 은 전부 빈 배열이다. 자동 수집하지 않는 항목이라 사람이 확인해서 채워야 한다(PWS 도 세 번 고쳤다 — 보고서 26·27).

### 우선순위 5 — 미룬 정비
`/api/tournaments/{id}` 가 404 대신 500, 로고 이미지 최적화(`vex.png` 1.6MB 등), `README.md` 재작성, LICENSE 없음, 테스트 0개.

---

## 4. 관련 파일

- `ingest/README.md` — 리그 추가 절차. **PCL 에서 실제로 걸린 함정들이 정리돼 있다**
- `ingest/build_league_seed_mediawiki.py` — 수집기
- `primary_data/*_teams_verified.json` — 리그별 확정 시드 (손으로 편집 가능, 생성 스크립트는 초안까지만)
- `CLAUDE.md` — 매 세션 자동 로드. 리그 추가 방법·함정 정리
- `frontend/src/components/players/PlayersTab.jsx` — `LEAGUES` 배열이 탭 정의
- `backend/.../config/DataInitializer.java` — `VERIFIED_SEEDS` 목록

---

## 5. 주의사항

### 데이터 성격
- **수집한 로스터는 "대회 시점" 기준이다.** 이적이 반영되지 않으며 그게 의도다. PCL 의 Weibo Gaming 은 대회 후 4명 전원이 바뀌었지만 시드에는 대회 때 명단이 들어 있다
- **자동 갱신 시스템은 없다.** 스케줄러 0건. 바꾸려면 스크립트를 다시 돌린다
- **선수 세팅은 PWS 만 값이 있고 그마저 가짜다** (96명 전원 800/32/동일 마우스 — `scripts/60` 이 일괄 주입). PCL·EMEA·AMER 은 아예 넣지 않아 화면에 `미등록` 이 뜬다. 이게 올바른 상태다
- **트로피는 PWS 만 채워져 있다**

### 리그별 차이 (다음 리그에서도 나올 수 있다)
- 위키 코드가 **약칭인 리그**(PCL: `jdg`)와 **팀 이름 그대로인 리그**(EMEA: `Natus Vincere`)가 있다. `code_to_tag()` 가 코드와 팀명이 같으면 tag 를 비운다
- 참가팀이 **Stage 소절로 나뉘는 대회**(PCL: S 8 / A 8 / B 24)가 있다. 목표 팀이 여러 소절에 흩어져 있으면 `--seed-map` 으로 골라내야 한다
- 동명 팀은 문서명이 `ZEAL (Chinese team)` 이 된다. 접미사를 뗀다
- 위키 원문은 **팀 이름이 아니라 내부 코드**를 준다. 정식명은 렌더된 HTML 에서만 얻는다. **개수가 다르면 멈추도록** 되어 있다

### 코드 함정
- **`ddl-auto: create`** — 재기동마다 DB 전멸 후 시드 재적재
- **기동 레이스** — `DataInitializer` 가 웹 서버 뒤에 실행된다. 준비 확인은 "HTTP 200" 이 아니라 **기대 팀 수**로 할 것
- **PostgreSQL null 파라미터** — JPQL 에 nullable 바인딩 금지
- **컬렉션 2개 동시 fetch join 금지** (`MultipleBagFetchException`)
- **`seedType IS NOT NULL`** — 팀 카드 조회 필수 조건
- **`pro`/`amateur` 외의 seedType 은 화면에서 사라진다** (`LeagueTeamGrid`)

### 협업
- 한국어로 소통한다
- **지시하지 않은 작업을 임의로 진행하지 말 것.** 세션 초반에 그 문제로 작업을 전부 되돌린 이력이 있다
- 비자명한 작업은 **계획을 먼저 보고하고 승인받는다**
- **모르거나 애매하면 물어본다.** 이번 리그 작업에서 7번 멈추고 질문했고 그중 하나는 내가 확인하지 않고 선택지를 만든 실수였다(리퀴피디아에 팀 약칭 데이터가 있다고 가정했으나 없었다)
- **조사 결과를 그대로 믿지 말 것.** 수치는 원본으로 확인한다

---

**이어받는 법**: `claude -c` (같은 폴더에서), 또는 `/clear` 후 `@HANDOFF.md`.
**바로 이어서 할 일**: 위 "우선순위 1 — 남은 리그 2개" 의 PTS 명령부터.
