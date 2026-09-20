# HANDOFF — 2026-09-20

Claude Code 설정 → PE탭 PWS 백엔드 연동 → 전체 구조 감사 → 정비까지 완료한 시점.
**모든 작업이 아직 커밋되지 않았습니다.**

---

## 1. 완료한 일

### A. Claude Code 설정 (커밋 `cdbf817`)
`.claude/settings.json`(권한 허용 18/차단 6), 커스텀 커맨드 `/dev`·`/report`(프로젝트), `/handoff`·`/spec`(전역, `~/.claude/commands/`), `CLAUDE.md` 생성.

### B. PE탭 PWS 백엔드 연동 (커밋 `1dcb905`)
프론트가 정적 상수를 쓰던 것을 API 호출로 전환. `Team`에 `tag`·`seedType`·`TeamTrophy` 추가, `TeamCardDto`와 `GET /api/teams/cards?league=PWS` 신설, `DataInitializer`가 검증 PWS 시드를 먼저 적재하고 레거시는 팀명 중복 시 스킵.

### C. 보안 — 노출 구조 제거 (미커밋)
**API 키가 21곳에 있었습니다.** `application.yml` 하나가 아니라 **파이썬 스크립트 20개에 같은 키가 복붙**돼 있었음.

- 21곳 전부 `os.environ["PUBG_API_KEY"]` / `${PUBG_API_KEY}` 참조로 변경
- `docker-compose.yml` DB 비밀번호도 환경변수화(로컬 기본값 유지)
- `.gitignore`에 `.env`, `.env.*`, `*.pem`, `*.key`, `secrets/` 추가 (이전에는 `.env` 항목이 아예 없었음)
- 타사(wwcd.lol) Supabase 키·엔드포인트 제거 — 번들 15개 + `supabase_client_snippet.txt` 삭제, `scripts/40`·`41`의 하드코딩 키 제거
- **추적 파일 전수 스캔 결과 자격증명 0건**

### D. 죽은 코드 삭제 (미커밋, 총 34건)
크롤러 일체(`CrawlerService`/`CrawlerController`/`CrawlerStatusDto` + `@EnableScheduling` + Jsoup 의존성), 관리자 API(`AdminController`/`AdminService` + DTO 2), `mockData.js`, `TeamRosterView.jsx`(255줄), `PlayerHighlight`+`HighlightDto`+`PlayerHighlightRepository`, `PlayerSettingRepository`, `PlayerGearRepository`, `PROJECT_OVERVIEW.md`, `scripts/70`, `secondary_data/`, 서드파티 번들 16개, `sl.png`.

`intermediate_results/` 6.4MB → 216KB.

### E. 데이터 무결성 (미커밋)
- **`PlayerDetailModal`** — FOV·해상도·마우스패드·키보드·헤드셋·모니터를 하드코딩 기본값으로 채워 **모든 PWS 선수가 검증된 값인 양 표시**하던 버그 제거. 이제 실제 값만 표시하고 없으면 `미등록`
- **`PubgOfficialApiService`** — API 실패 시 하드코딩 대회 목록("EWC 2026 / $2,000,000" 등)을 `source: KRAFTON_OFFICIAL_API` 라벨로 반환하던 폴백 61줄 제거
- **`HitEndingTab`** — 실존 선수(Xmpl·seoul·Salute·TGLTN)에 대한 출처 없는 경기 서술 제거, "준비 중" + 계획 안내로 대체
- **`TournamentsTab`** — 선택한 대회와 무관하게 항상 PGS4 순위표를 보여주던 버그 수정

### F. 리그 복제 준비 — 리팩터 (미커밋) ★이번 작업의 핵심
`PlayersTab.jsx` **600줄 → 108줄**. 신규 9파일.

```
api/client.js, api/teams.js          모든 백엔드 호출 경로
hooks/useApi.js                      { data, loading, error, reload }
components/common/{Loading,Error}Panel.jsx
components/players/PlayersTab.jsx    칩 + 검색 + 분기만
components/players/LeagueTeamGrid.jsx  ← league prop 하나로 동작 (복제 단위)
components/players/TeamCard.jsx
components/players/HotPlayerGrid.jsx
```

**리그 추가가 `PlayersTab.jsx`의 `LEAGUES` 배열에 한 줄 넣는 일이 됐습니다.** PCL·EMEA·AMER·APAC을 실제로 API에 연결해 빈 상태를 표시하도록 했고, 브라우저로 동작을 확인했습니다.

### G. 검증 (브라우저 실측)
PWS 24팀(pro13/am11) 리팩터 전과 동일 · PCL 탭 빈 상태 표시 · 선수 모달 `미등록` · 대회 탭 PWS 선택 시 순위표 없음 · 히트엔딩 준비 중 · HOT 탭 회귀 없음 · 콘솔 에러 0건 · `compileJava` 및 `npm run build` 통과(번들 189.5KB).

---

## 2. 진행 중인 일

**없음.** 코드 작업은 완결됐고 검증도 끝났습니다.

---

## 3. 다음 할 일

### 우선순위 1 — 커밋 (사용자 답변 대기)
두 가지를 두 번 물었으나 아직 답을 못 받았습니다.
1. `interim_reports/29_trophy_and_challenger_removal_and_api_verification.md` — 사용자가 직접 작성한 파일. 커밋에 포함할지
2. 커밋을 **보안 정리 / 죽은 코드 삭제 / 무결성 + 리팩터** 로 나눌지, 하나로 할지

로컬이 `origin/main`보다 2커밋 앞선 상태(B·A). 푸시는 별도 확인 필요.

### 우선순위 2 — API 키 재발급 (사용자만 가능)
코드는 환경변수화했지만 **옛 키가 커밋 `ba3a8d5` 히스토리에 살아 있습니다.** 저장소는 Private이라 급하지 않으나, 협업자 추가나 public 전환 시 그대로 노출됩니다. 크래프톤 개발자 포털에서 재발급 필요. 파일만 고치는 것으로는 무효화되지 않습니다.

### 우선순위 3 — `/api/tournaments/official` 500 수정
**원래부터 깨져 있던 엔드포인트입니다** (제 변경 때문이 아님). `PubgTournamentController`의 `@CrossOrigin(origins = "*")`와 `WebConfig`의 `allowCredentials(true)`가 충돌해 Spring이 거부. `@CrossOrigin` 한 줄 제거로 해결(`WebConfig`가 이미 `/api/**` CORS 처리). 이 때문에 E항목의 가짜 폴백 제거는 **코드·컴파일만 확인했고 실제 응답으로 검증하지 못했습니다.**

### 우선순위 4 — 기능 착수 (각각의 선행 조건 있음)
| 기능 | 선행 조건 |
|---|---|
| 다른 리그(PCL 등) | 검증된 시드 데이터. 코드는 준비됨 |
| 선수 상세 실데이터 | 디스코드 수집 → **API가 아니라 시드 파일로** 유입 |
| HOT 탭 | `ddl-auto: create` → Flyway 전환 (조회수 영속성) |
| 대회 탭 | `scripts/49~51`의 순위·스탯 집계를 Java로 이식 (약 80% 완성돼 있음) |
| 히트엔딩 | 반복 실행 텔레메트리 파이프라인 |

### 우선순위 5 — 미룬 정비
컨트롤러 경로 충돌(`/api/tournaments` 중복 매핑), 로고 이미지 압축(`vex.png` 1.6MB 등 3.1MB), `README.md` 재작성(모순 17건), LICENSE 없음, 테스트 0개.

---

## 4. 관련 파일

- `CLAUDE.md` — 매 세션 자동 로드. 리그 추가 방법, 시드 적재 순서, 기동 레이스, 알려진 고장이 정리돼 있음
- `primary_data/pws2_teams_verified.json` — 검증된 24팀. 직접 편집한다 (생성 스크립트 없음)
- `frontend/src/components/players/LeagueTeamGrid.jsx` — 리그 복제 단위
- `frontend/src/api/` + `hooks/useApi.js` — 모든 백엔드 호출 경로
- `interim_reports/` 29건 — 데이터 결정 근거

**참고**: 삭제한 구 `PlayersTab.jsx`(600줄)의 최종 내용은 git blob `ab69879e45c5dea1bf33468fdbb4711b01d95de0` 에 보존돼 있습니다. 복원이 필요하면 `git cat-file -p ab69879 > 파일명`.

---

## 5. 주의사항

### 데이터 품질
**검증된 실데이터는 팀 단위뿐입니다** — 팀명·태그·로고·트로피·시드(리퀴피디아 대조, 보고서 26·27). **선수 개인 데이터는 전부 플레이스홀더**입니다: 로스터 96명 전원 `800 DPI / 32 감도 / 동일 마우스`, `realName`이 닉네임과 동일. 선수 세팅을 근거로 뭔가 주장하지 말 것.

**리퀴피디아는 실시간 호출하지 않습니다.** 백엔드에 관련 코드 0줄이며 앞으로도 넣지 않습니다.

### 코드 수정 시 함정
- **`ddl-auto: create`** — 재기동마다 스키마·데이터 전멸 후 시드에서 재적재. 런타임에 쓴 데이터는 남지 않는다
- **기동 레이스** — `DataInitializer`는 웹 서버 기동 *후* 실행. 기동 직후 몇 초간 `/api/teams/cards`가 `[]`를 반환한다. 준비 확인은 "HTTP 200"이 아니라 **"24팀이 오는가"** 로 할 것
- **PostgreSQL null 파라미터** — JPQL에 nullable 파라미터 바인딩 금지. 조건별 전용 메서드로 분기
- **컬렉션 2개 동시 fetch join 금지** — `Team.players` + `Team.trophies` → `MultipleBagFetchException`. trophies는 `@BatchSize`
- **`seedType IS NOT NULL`** — 팀 카드 조회에서 필수. 없으면 24팀 대신 49팀
- **`index.css`에 `spin` 키프레임 없음** — `fadeIn`, `pulseGlow`만 있다
- **기본값을 지어내지 말 것** — 값이 없으면 `미등록`. 이 세션에서 프론트·백엔드 양쪽의 창작 폴백을 제거했다

### 협업 관련
- 한국어로 소통한다
- **지시하지 않은 작업을 임의로 진행하지 말 것.** 세션 초반에 그 문제로 작업을 전부 되돌린 이력이 있다. 요청을 수행할 수 없으면 대체 작업을 만들지 말고 알리고 멈출 것
- 비자명한 작업은 **계획을 먼저 보고하고 승인받는다**(EnterPlanMode → ExitPlanMode)
- **조사 에이전트 보고를 그대로 믿지 말 것.** 이 세션에서 "트로피 13팀"(실제 7팀), "1090줄이 번들에 실린다"(실제로는 tree-shaking돼 0.68KB 차이) 두 건이 틀렸다. 수치는 원본으로 확인한다
- 감사 결과를 보고할 때는 **"미완성 / 정비 필요 / 삭제 대상"을 구분**할 것. 나열식 보고가 "구조부터 잘못됐다"로 읽혀 불필요한 불안을 준 적이 있다

---

**이어받는 법**: `claude -c` (같은 폴더에서), 또는 `/clear` 후 `@HANDOFF.md`.
