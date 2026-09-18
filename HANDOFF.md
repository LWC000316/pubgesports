# HANDOFF — 2026-09-18

Claude Code 설정 적용 → 프로젝트 구조 파악 → PE탭 PWS 백엔드 연동까지 완료한 시점의 인수인계 문서.

---

## 1. 완료한 일

### A. CLAUDE.md 생성 (`/init`)
`C:\work\pubgesports\CLAUDE.md` 신규 생성 (git 미추적). 프로젝트 개요 / 기술 스택 / 명령어 / 아키텍처 / 코드 규칙 / 데이터 파이프라인 / 데이터 정확성 주의사항.

### B. Claude Code 설정 적용
`aisyncclub.vercel.app` 체크리스트 23팁 중 설치·신규 프로젝트 생성을 제외한 설정 항목 적용.

| 경로 | 내용 |
|---|---|
| `~/.claude/commands/handoff.md` | `/handoff` — 이 문서를 만드는 커맨드 |
| `~/.claude/commands/spec.md` | `/spec` — 구현 전 인터뷰 → plan-spec.md |
| `~/.claude/settings.json` | `alwaysThinkingEnabled`, `spinnerTipsEnabled` 추가 |
| `.claude/settings.json` | 권한 허용 18 / 차단 6 |
| `.claude/commands/dev.md` | `/dev` — docker → 백엔드 → 프론트 순차 기동 |
| `.claude/commands/report.md` | `/report` — interim_reports 다음 번호 보고서 |
| `.gitignore` | `.claude/settings.local.json` 1줄 추가 |

커맨드 4개 모두 세션에 정상 등록 확인 완료.

### C. 프로젝트 구조 분석
백엔드 Java 전체 + 프론트 주요 컴포넌트 정독. 결과는 5번 절 참조.

### D. PE탭 PWS 섹션 백엔드 연동 ← **이번 세션의 주요 작업**

프론트가 `esportsData.js` 정적 상수를 쓰던 것을 백엔드 API 호출로 전환. 계획 승인 후 구현.

**백엔드 (7건)**
- `domain/Team.java` — `tag`, `seedType` 필드 및 `trophies` 연관관계 추가. `trophies`는 `players`와 동시 fetch join 시 `MultipleBagFetchException`이 나므로 `@BatchSize(50)`로 배치 로딩.
- `domain/TeamTrophy.java` (신규) — `{team, name, count}` 구조화된 트로피
- `dto/TeamCardDto.java` (신규) — 프론트가 읽는 필드명(`logo`, `roster`, `dpi`, `sens`, `mouse`)에 맞춘 뷰 DTO
- `repository/TeamRepository.java` — `findByLeagueWithPlayers(league)`
- `service/PlayerService.java` — `getTeamCards(league)`
- `controller/PlayerController.java` — `GET /api/teams/cards?league=PWS`
- `config/DataInitializer.java` — 검증 PWS 시드를 먼저 적재하고, 레거시 73팀 파일은 팀명 중복 시 건너뜀

**데이터 (2건)**
- `scripts/70_export_pws_teams_to_seed_json.py` (신규) — `esportsData.js`의 `LATEST_PWS2_TEAMS`를 파싱해 시드 JSON 생성
- `primary_data/pws2_teams_verified.json` (신규) — 24팀 / 96명, 스크립트 출력물

**프론트 (1건)**
- `components/PlayersTab.jsx` — `useEffect` + `fetch`, 로딩/에러 상태, 재시도 버튼, 널 안전성 보강, 시드 카운트 하드코딩(13/11) 제거

**브라우저까지 실제 검증 완료**: API 24팀(pro 13 / amateur 11, 트로피 7팀, 로스터 96명) · 화면 렌더링 정적 버전과 동일 · 선수 모달 정상 · 백엔드 종료 시 에러 화면 + 재시도 버튼 동작 · HOT 탭 회귀 없음 · 콘솔 에러 0건.

**구현 중 고친 버그**: 최초 구현에서 24팀이 아닌 49팀이 반환됐다. 레거시 73팀 파일에도 `league="PWS"`인 팀이 25개 있어 함께 잡힌 것. 조회 조건에 `seedType IS NOT NULL`을 추가해 해결.

### E. 시도했으나 취소함
세션 초반, 영상 자막을 읽지 못한 상태에서 **지시 없이** `.claude/settings.json` / `.gitignore` / `CLAUDE.md`에 임의 설정을 넣었다가 사용자 지적으로 전부 되돌림. 이후 계획 승인을 받고 다시 적용한 것이 B항목이다.

---

## 2. 진행 중인 일

**없음.** D항목까지 완결되었고 검증도 끝났다. **단, 아직 커밋하지 않았다.**

실행 중인 프로세스 (다음 세션에서는 꺼져 있을 수 있음):
- Docker Desktop + `pubg-postgres` 컨테이너 (5432)
- 백엔드 `gradlew bootRun` (8080)
- 프론트 `npm run dev` (5173)

---

## 3. 다음 할 일

### 우선순위 1 — 커밋 여부 결정
아래가 전부 미커밋 상태다. 사용자에게 커밋할지 물어볼 것.
- 이번 작업 산출물 10건 (1-D 참조)
- 설정 파일 (`.claude/`, `CLAUDE.md`, `.gitignore`)
- `HANDOFF.md` (개인 메모 성격이라 `.gitignore`에 넣는 선택지도 있음)
- **주의**: `backend/.../PlayerRepository.java`, `interim_reports/24`, `28`은 이번 세션과 무관한 이전 변경분이다. 함께 커밋할지 별도로 확인할 것.

### 우선순위 2 — 중간보고서
`/report PE탭 PWS 백엔드 연동` 으로 29번 보고서 생성 가능. 사용자가 원할 때만 할 것.

### 우선순위 3 — 다음 연동 범위
PE탭 PWS만 동적화했다. 남은 선택지:
- HOT 탭 (`HOT_PLAYERS_12`, 현재 정적)
- PCL/EMEA/AMER/APAC 탭 — 현재 "Coming Soon" 플레이스홀더이고 **검증된 데이터 자체가 없음**. 데이터 확보가 선행돼야 함.
- 대회 탭 (`TOURNAMENTS_DATA`, `LEADERBOARD_PGS4`) — DB에 Tournament 데이터를 적재하는 코드가 아예 없어 작업량이 큼
- 히트엔딩 탭 — DB 모델 자체가 없음

### 우선순위 4 — 보안: 커밋된 API 키
`backend/src/main/resources/application.yml` 26번 줄에 PUBG 공식 API Bearer 토큰이 평문 하드코딩되어 있고 git에 추적 중이다(`.gitignore`는 `application_local.yml`만 제외). 세션 중 3회 보고했으나 조치 없음. 키 재발급 + 환경변수 이전 권장.

### 우선순위 5 — 미적용 Claude Code 설정
체크리스트에 없어 적용하지 않은 항목: hooks, 서브에이전트(`.claude/agents/`), MCP 서버, statusline, worktree 설정.

---

## 4. 관련 파일

**이번 작업의 핵심 경로**
- `frontend/src/components/PlayersTab.jsx` — PE탭 전체. PWS 분기만 동적, HOT 분기는 정적
- `frontend/src/data/esportsData.js` — 여전히 HOT 탭과 대회 탭이 사용 중. 삭제 불가
- `backend/.../dto/TeamCardDto.java` — 프론트 계약(contract). 프론트 필드를 바꾸려면 여기부터
- `backend/.../config/DataInitializer.java` — 시드 적재 순서가 중요 (검증 PWS 먼저 → 레거시 중복 스킵)
- `primary_data/pws2_teams_verified.json` — 검증된 24팀. 직접 고치지 말고 스크립트 70번을 다시 돌릴 것
- `scripts/70_export_pws_teams_to_seed_json.py` — 위 JSON 생성기

**설정**
- `~/.claude/settings.json`, `~/.claude/commands/` — 전역
- `.claude/settings.json`, `.claude/commands/` — 이 레포 전용
- `CLAUDE.md` — 모든 세션에 자동 로드

---

## 5. 주의사항

### 데이터 품질 — 반드시 알 것

**검증된 실데이터는 팀 단위뿐이다.** 팀명·태그·로고·트로피·시드 구분은 리퀴피디아 대조로 검증됐다(26·27번 보고서). 반면 **선수 개인 데이터는 전부 플레이스홀더**다 — 로스터 96명이 전원 `800 DPI / 32 감도 / Logitech G PRO X Superlight`, `realName`이 닉네임과 동일. 레거시 73팀 파일도 마찬가지(전원 800/30.0, 로고는 `via.placeholder.com`, 팀 설명은 템플릿 문자열). 선수 세팅을 근거로 뭔가 주장하지 말 것.

**리퀴피디아는 실시간 호출하지 않는다.** 사용자 결정 사항. 백엔드에 리퀴피디아 코드는 0줄이며 앞으로도 넣지 않는다. 수집은 `scripts/59~69`가 오프라인으로 담당.

### 아직 남아 있는 구조적 사실

**크롤러가 크롤링을 하지 않는다.** README는 "LIVE DATA CRAWLER ENGINE"이라고 하지만 `CrawlerService.java`는:
- `crawlAllPlayers()` (100~120줄) — 외부 요청 없이 `lastCrawledAt`만 갱신하고 "성공적으로 최신화" 반환
- `parseAndApplyProSettings()` (132~140줄) — DPI를 파싱해 지역변수에 담고 사용하지 않음 (죽은 코드)
- 67줄 — `getClass().getMethod(...)` 결과를 버림
- 새벽 4시 스케줄러도 타임스탬프만 갱신

**프론트의 나머지 탭은 여전히 정적이다.** 대회/히트엔딩 탭과 HOT 탭은 백엔드를 호출하지 않는다. PE탭 PWS만 동적이다.

### 코드 수정 시 함정

- **`ddl-auto: create`** — 백엔드 재기동마다 스키마와 데이터가 날아가고 시드에서 재적재된다. 시드 파일이 진실의 원천이라 정합성 문제는 없지만, `/api/admin`으로 고친 내용은 재시작 시 사라진다.
- **PostgreSQL null 파라미터** — JPQL에 nullable 파라미터를 바인딩하면 드라이버가 `bytea`로 추론해 `lower(bytea) does not exist`가 난다. `PlayerRepository`와 `TeamRepository`가 조건별 전용 메서드를 두는 이유. 새 쿼리도 같은 패턴을 따를 것.
- **컬렉션 2개 동시 fetch join 금지** — `Team.players` + `Team.trophies`를 한 쿼리에서 fetch join하면 `MultipleBagFetchException`. `trophies`는 `@BatchSize`로 처리 중.
- **`index.css`에 `spin` 키프레임이 없다.** 있는 것은 `fadeIn`, `pulseGlow` 둘뿐.

### 협업 관련

- 사용자는 한국어로 소통한다.
- **지시하지 않은 작업을 임의로 진행하지 말 것.** 세션 초반에 그 문제로 작업을 전부 되돌린 이력이 있다. 요청을 수행할 수 없으면 비슷한 다른 작업으로 대체하지 말고 알리고 멈출 것.
- 비자명한 작업은 **계획을 먼저 보고하고 승인받는다**(EnterPlanMode → ExitPlanMode). 이 흐름으로 진행했을 때 순조로웠다.
- **조사 에이전트의 보고도 그대로 믿지 말 것.** 이번 세션에서 Explore 에이전트가 "트로피 보유 13팀"이라고 보고했으나 실제는 7팀이었다. 수치를 쓰기 전에 원본으로 확인한다.

---

**이어받는 법**: `/clear` 로 대화를 정리한 뒤 `@HANDOFF.md` 를 참조해 이어서 작업하면 된다.
