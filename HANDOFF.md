# HANDOFF — 2026-10-03

대회 탭이 **화면·집계 모두 동작**한다. 남은 것은 **데이터를 다 받는 일**이고,
그 작업을 GitHub Actions 로 넘기는 준비까지 끝냈다.

```
본선 334단계 중  원본 125 수집 · 집계 118 · 단계 이름 74
미푸시 커밋 14개 — 아직 로컬에만 있다
```

> 이전 인수인계(2026-09-30, PE·HOT 완료 시점)는 git 이력에 있다. 이 문서는 그
> 다음 작업인 **대회 탭**을 다룬다.

---

## 1. 완료한 일

### 대회 탭 화면 (커밋 `822e9b9`, `7d238e4`, `6706abd`, `f6cfcc8`)

- **5단계 탐색**: 분류(글로벌·지역·스크림) → 시리즈 → 연도 → 대회(회차) → 단계
  → 리더보드 / 플레이어 스탯 / 매치로그. 브라우저에서 직접 확인함.
- 리더보드 열을 사용자 지정대로 바꿈: **경기 · 치킨 · 순위 · 킬 · 평균 · 합계**
- 플레이어 스탯 11개 열 전부 양방향 정렬, 기본은 OVERALL 내림차순
- 매치로그: 공식 맵 이미지 위에 이동 경로·자기장·킬 지점, 재생·팀 필터
- **팀마다 경기 수가 다른 단계에 경고를 띄움** (61단계 중 15개가 해당)
- 데이터 없는 시리즈(EWC·PGC)와 스크림은 **이유를 적어** 보여줌

### 데이터 정확성 (커밋 `86f46fb`, `96fefb0`, `80d4b87`)

- **옛날 팀 이름 오염 차단.** 2019 NAVI → "S8UL", 2021 Gen.G → "Baegopa" 로
  찍히던 것을 막았다. 시드와 같은 시기가 아니면 팀 태그가 인게임 접두사와
  정확히 같을 때만 이름을 쓴다. 2026년 대회는 회귀 없음(16/16 유지).
- **배점표를 리퀴피디아에서 확인.** 7개 연도·3개 시리즈 **28경기가 전부 같은 표**
  (킬 1점 · 1위 10 · 2위 6 · 3위 5 · 4위 4 · 5위 3 · 6위 2 · 7~8위 1).
  2019년부터 적용. **2018년은 확인하지 않아 점수 열이 빈 채로 나간다.**
- **중단된 재경기를 걸러냄.** 한 경기가 뿌리는 순위 점수 32점 고정이라는
  불변식으로 잡는다. PVS 1건, PNC 3건 발견.
- **단계 이름을 시리즈별로 가름.** 같은 코드가 다른 뜻이다 — `ws` 가 PGS 는
  Winners Stage, PGC 는 Weekly Survival.

### 단계 이름 (커밋 `d9e6723`, `96fefb0`, `7e384c6`, `29d9a69`)

전부 리퀴피디아 Format 절과 **경기 수·날짜 지문이 맞아떨어진 것만** 넣었다.

| 시리즈 | 코드 → 이름 | 지문 |
|---|---|---|
| PGS | gsg·ws·ss·fsg → Group·Winners·Survival·Final Stage | 9·5·5경기 |
| PGC | ws→Weekly Survival, gs→Grand Survival, wf·bm·rd | 하위 문서 9개 일대일 |
| PWS | s\<주차\>\<일차\>→Weekly Stage, wf→Weekly Finals | 5·10경기 + 달력 |
| EMEA | fc·fp·ff·sp·sf → Fall/Spring Cup·Playoff·Finals | 5·15경기 |
| AMER | c·p·f → Cup·Playoff·Finals | 5·15경기 |

### 수집 도구 (커밋 `95d267d` 외)

- `ingest/fetch_tournament_list.ps1` — 공식 API 전체 목록 (호출 1회)
- `ingest/stage_ids.txt` — 1,194개 중 본선 334단계 (최신순)
- `ingest/fetch_all.ps1` — 일괄 수집, 이어받기. `-MaxMinutes`·`-SkipBuilt` 추가
- `ingest/build_all.py` — 일괄 집계 (네트워크 없음)
- `ingest/build_match_logs_all.py` — 매치로그 대상 선정·추출. `--list` 로 비용 확인
- `ingest/stage_label.py` — id 에서 시리즈·회차·단계 해독
- `ingest/verify_scoring.py` — 리퀴피디아에서 배점표 확인
- `.github/workflows/collect-tournaments.yml` — **작성·YAML 검증 완료, 미실행**

### 시도했으나 취소함

- **없음.** 되돌린 결정은 없다. 다만 잘못 넣었다가 **같은 세션에서 고친 것**이
  둘 있다 (아래 5번 참고): 평평한 단계 이름 표, 미검증 배점표.

---

## 2. 진행 중인 일

### 원본 수집 — 125 / 334

로컬에서 `ingest/fetch_all.ps1` 이 돌고 있었다. **세션이 끝나면 함께 죽는다.**
받은 것은 그대로 남고 다시 돌리면 이어받는다.

```
받은 원본   intermediate_results/tournaments/  125단계 · 약 300MB (gitignore 대상)
집계 결과   primary_data/tournaments/          118단계 · 4MB (커밋 대상)
```

원본 125 vs 집계 118 의 차이 7개는 아직 집계 안 돌린 것 + EWC 익명화 거부 1건.

### 서버 전환 — 준비 끝, 사용자 조작 대기

`.github/workflows/collect-tournaments.yml` 를 만들었고 YAML 파싱·스크립트 인자
바인딩·`-SkipBuilt` 동작을 확인했다. **아직 푸시도 실행도 하지 않았다.**

설계: **원본을 서버에 보관하지 않는다.** 받아서 집계하고 결과(12MB)만 커밋하며,
**커밋된 `primary_data/tournaments/*.json` 이 곧 진행 표시**다. 다음 실행은 거기
없는 단계만 받는다. 캐시도 아티팩트도 필요 없다.

### 미완성 코드

없다. 모든 변경은 빌드·테스트를 통과했고 커밋됐다.

---

## 3. 다음 할 일

### (1) 푸시 — 커밋 14개가 로컬에만 있다

```bash
git push
```

`822e9b9` 부터 `95d267d` 까지. 집계 결과 118단계와 워크플로 파일이 올라간다.

### (2) GitHub Actions 로 나머지 수집 — **사용자만 할 수 있는 단계 포함**

1. **(사용자)** 저장소 Settings → Secrets and variables → Actions →
   New repository secret → `PUBG_API_KEY` 등록.
   키 값은 <https://developer.pubg.com> My Apps 에서 확인.
   **키 값을 대화에 붙여넣지 말 것.** 지금까지도 환경변수로만 썼다.
2. **(사용자)** Actions 탭 → "대회 기록 수집" → Run workflow.
   입력값 기본 그대로 (`max_minutes` 320, `delay_seconds` 6).
   `delay_seconds` 를 6 미만으로 줄이면 API 제한에 걸린다.
3. 끝나면 요약에 `수집 진행: N / 334` 가 뜬다. 남았으면 한 번 더 실행.

**미확인**: 저장소가 공개인지 비공개인지. 비공개면 Actions 무료 한도가 월
2,000분(한 번에 최대 320분)이라 6번이면 소진된다. 남은 분량은 두 번이면 끝난다.

로컬에서 계속 받아도 된다 — 다만 서버와 같은 단계를 양쪽에서 받으면 낭비다.
로컬로 더 받았다면 `python ingest/build_all.py` 후 커밋해야 서버가 건너뛴다.

### (3) 수집 완료 후 마무리

```bash
git pull                                  # 서버가 커밋한 집계 결과
python ingest/build_all.py                # 로컬 원본 중 미집계분
cd backend && ./gradlew bootRun           # 재기동해야 화면에 반영됨
```

백엔드는 `@PostConstruct` 로 기동 시 한 번만 파일을 읽는다.

### (4) 매치로그 추출 — 글로벌 결승 27단계

```bash
python ingest/build_match_logs_all.py --list   # 대상과 비용 먼저 확인
python ingest/build_match_logs_all.py
```

약 380경기 · **12GB 내려받기** · 저장소 95MB 증가. API 호출은 추가로 들지 않는다
(경기 JSON 안의 텔레메트리 URL 을 쓴다). 원본 33MB 는 추출 후 자동 삭제된다.

### (5) 남은 단계 코드 이름 채우기 (선택)

44개 단계가 아직 코드로 표시된다.

```
EMEA s26 · EWC api6·fs·gs · PCL ab·af26·as26·f·t · PGC api·ls
PGS api·api2·xapi · PNC ai·cn26·ss · PTS f1·g1·w1·w2·ws
PVS c262·p1·p2 · PWS c1~c5·f·lc·r·ws1
```

방법: 리퀴피디아 해당 문서의 Format 절을 읽고 **경기 수가 맞는지 대조**한 뒤
`ingest/stage_label.py` 의 `STAGE_NAMES`/`STAGE_PATTERNS` 에 넣는다.
**맞지 않으면 넣지 않는다.**

### (6) PGS 회차 이름 — 미해결

리퀴피디아는 PGS 2026 을 **Circuit 1~4 × (Series 1/2/Final)** 로 부른다.
우리 id 의 pgs1~pgs9 는 날짜상 3개씩 묶이고 매 3번째가 `gf` 라
**pgs7 = Circuit 3 Series 1** 이며 이건 경기 수까지 맞아 확인됐다.
나머지 회차는 확인하지 않았다. 화면의 "PGS 7" 은 **크래프톤 내부 번호**지
대회 이름이 아니다. 수집이 끝나 경기 수가 다 모이면 같은 방식으로 검증 가능.

---

## 4. 관련 파일

### 새로 만든 것

| 경로 | 역할 |
|---|---|
| `.github/workflows/collect-tournaments.yml` | 서버에서 수집·집계·커밋 |
| `ingest/fetch_tournament_list.ps1` | 공식 API 전체 대회 목록 (호출 1회) |
| `ingest/fetch_all.ps1` | 334단계 일괄 수집, 이어받기 |
| `ingest/stage_ids.txt` | 본선 334단계 목록 (날짜·시리즈·id) |
| `ingest/build_all.py` | 일괄 집계 |
| `ingest/build_match_logs_all.py` | 매치로그 대상 선정·추출 |
| `ingest/stage_label.py` | id → 시리즈·회차·단계 해독 |
| `ingest/verify_scoring.py` | 리퀴피디아에서 배점표 확인 |

### 고친 것

| 경로 | 무엇을 |
|---|---|
| `ingest/build_tournament_seed.py` | 배점표·팀이름 게이트·중단경기 제외·경기수 불균등 |
| `ingest/build_match_log.py` | 텔레메트리 자동 삭제, `--relabel-only` |
| `ingest/mediawiki_client.py` | `action=parse` 30초 간격, 429 재시도 |
| `backend/.../dto/TournamentArchiveDto.java` | year·edition·stage·matchesPerTeam 등 |
| `frontend/src/components/TournamentsTab.jsx` | 5단계 탐색, 리더보드 열, 경고 |
| `frontend/src/components/tournaments/PlayerStatsTable.jsx` | 11열 양방향 정렬 |
| `frontend/src/components/tournaments/MatchLogMap.jsx` | 반응형, 캔버스 해상도 고정 |
| `CLAUDE.md` | "대회 tab data" 절 전체 |
| `.gitignore` | 텔레메트리·진행로그·탐침 원본 제외 |

### 읽기만 한 것

- `primary_data/_sources.json` — 시드가 어느 시점인지. `seed_years()` 가 읽는다
- `intermediate_results/liquipedia_cache/` — 배점표·단계이름 근거가 여기 있었다

---

## 5. 주의사항

### 내가 틀렸다가 같은 세션에서 고친 것 둘

**(가) 배점표를 검증 없이 "표준"이라 단언했다.** 커밋 `6706abd` 에서 내 지식으로
배점표를 넣고 공식 출처로 확인한 것처럼 설명했다. 다음 커밋에서 구조를 바꿔
**`verifiedBy` 가 채워진 표만 쓰게** 했고, 그 뒤 리퀴피디아에서 실제로 읽어 채웠다.
→ "맞았다"와 "검증했다"는 다르다.

**(나) 단계 이름을 평평한 표에 넣었다.** `ws`=Winners Stage 를 전 시리즈에
적용해서 PGC 2021 의 `as-pgcws`(실제로는 Weekly Survival)에 틀린 이름이 붙었다.
한 시간 뒤 PGC 하위 문서를 보다가 발견해 시리즈별로 갈랐다.

### 사용자가 잡아낸 내 실수

**공식 API 의 id 하나를 "대회"로 취급했다.** PGS 7 은 id 가 4개(조별·Winners·
Survival·결승)인데 그중 결승 하나만 가져다 "PGS 7" 이라 불렀다. 예선이 통째로
빠져 있었다. → **바깥 데이터로 구조를 짜기 전에 "레코드 하나가 무엇인가"를 먼저
확인할 것.**

### 돌고 있는 작업 옆에서 테스트하지 말 것

GitHub Actions 용 스크립트를 더미 키로 1분 돌렸는데 그때 진짜 수집이 같은 목록을
훑고 있었다. 401 실패 45건이 진행 로그에 섞이고 빈 디렉터리 42개가 생겼다.
데이터 손상은 없었지만(파일 1,564개 JSON 검증) 운이었다.

### 함정 모음

- **리퀴피디아 `action=parse` 는 30초 간격이 필요하다.** 2초로 때려 429 차단을
  하루 겪었다. 차단되면 `action=query` 조차 막힌다. 더 때리면 길어진다
- **배점표는 `p_kill` 이 붙은 템플릿만 본다.** 같은 문서에 상금 배분과 시즌
  포인트(`p1=450`, `p1=50`)가 있어 섞으면 안 된다
- **PowerShell `Tee-Object` 는 UTF-16LE 로 쓴다.** 진행 로그를 셸에서 읽으려면
  `iconv -f UTF-16LE -t UTF-8` 가 필요하다. `Set-Content -Encoding UTF8` 은 BOM
- **EWC 는 참가자가 전원 익명**(`EWC-Player-23`). 빌더가 거부한다. 정상이다
- **`17`·`007`·`722`·`4AM` 은 진짜 팀 태그다** (중국 팀). 파싱 오류가 아니다
- **`frontend/public/maps/Neon_Main.png` 는 확장자만 png 이고 내용은 JPEG.**
  브라우저가 내용을 보고 렌더하므로 이름을 "고치지" 말 것
- **서버로 옮겨도 수집이 빨라지지 않는다.** API 제한이 계정 단위다.
  목적은 "컴퓨터가 꺼져도 돈다" 하나뿐이다
- **백엔드는 기동 시 한 번만 집계 파일을 읽는다**(`@PostConstruct`).
  새 데이터를 화면에 보이려면 재기동해야 한다

### 미확인으로 남은 것

- 저장소 공개 여부 (Actions 무료 한도에 영향)
- 2018년 배점표 (PGI 시절). 그 해 대회는 점수 열이 빈 채로 나간다
- 44개 단계 코드의 뜻
- PGS 회차와 Circuit/Series 의 대응 (pgs7 하나만 확인됨)

---

`/clear` 후 `@HANDOFF.md` 로 이어받으면 된다.
