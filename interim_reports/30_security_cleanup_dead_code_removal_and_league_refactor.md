# 보안 정리, 죽은 코드 제거, 데이터 무결성 수정 및 리그 복제 구조 리팩터

## 개요

PWS 탭을 레퍼런스로 완성해 다른 대회로 복제하기 전에, 프로젝트 전반을 감사하고 정비함.
감사 결과 뼈대(계층 분리, REST+SPA, 시드 파일 기반 데이터 원천)는 유지하기로 결정하고, 평문 커밋된 자격증명, 도달 불가능한 코드, 검증되지 않은 값을 검증된 것처럼 표시하는 구조, 복제에 부적합한 프론트엔드 형태를 개선함.

---

## 수행 작업 및 조치 내용

### 1. API 키 노출 구조 제거

• 현상
`backend/src/main/resources/application.yml`에 PUBG 공식 API 키가 평문으로 커밋되어 git에 추적 중이었음. 전수 조사 결과 같은 키가 **파이썬 스크립트 20개에도 복붙**되어 총 21곳에 존재.

• 원인
비밀값을 코드에 직접 적는 구조. `.gitignore`에 `application_local.yml` 자리가 예약돼 있었으나 사용되지 않았고, `.env` 관련 항목은 아예 없어 향후 `.env` 파일을 만들어도 커밋될 상태였음.

• 조치
- `application.yml`: `key: ${PUBG_API_KEY:}` 로 변경. DB 접속 정보도 `${DB_URL}`·`${DB_USERNAME}`·`${DB_PASSWORD}` 참조로 변경(로컬 개발 기본값 유지)
- 파이썬 스크립트 20개: `api_key = os.environ["PUBG_API_KEY"]` 로 일괄 변경, `import os` 보장. 20개 전부 문법 검사 통과
- `docker-compose.yml`: `POSTGRES_PASSWORD: ${DB_PASSWORD:-...}` 형태로 변경
- `.gitignore`: `.env`, `.env.*`, `*.pem`, `*.key`, `secrets/` 추가

**미해결**: 옛 키는 커밋 `ba3a8d5` 히스토리에 그대로 남아 있음. 파일 수정으로는 무효화되지 않으므로 **크래프톤 개발자 포털에서 키 재발급이 필요**함. 저장소가 Private이라 즉각적 위험은 낮으나, 협업자 추가 또는 public 전환 시 노출됨.

### 2. 타사 자격증명 및 스크랩 산출물 제거

• 현상
`intermediate_results/`에 타사 사이트(wwcd.lol / pubg-tracker)의 컴파일된 JS 번들 15개와 `supabase_client_snippet.txt`가 커밋되어 있었음. 스니펫에는 해당 사이트의 Supabase 엔드포인트·키, Vercel 배포 ID, 커밋 작성자명, 커밋 메시지 전문이 포함.

• 원인
`scripts/38_extract_supabase_keys.py`가 타사 번들에서 Supabase URL과 키를 추출해 그 백엔드에 인증 요청을 보내는 방식으로 조사를 진행했고, 그 입력·출력이 모두 레포에 남았음. `scripts/41`이 받아온 `sample_match_data.json`(4.76MB)도 타사가 가공한 데이터.

• 조치
- 번들 15개, `supabase_client_snippet.txt`, `sample_match_data.json` 삭제
- `scripts/40`·`41`의 하드코딩된 엔드포인트·키를 환경변수 참조로 바꾸고 폐기 주석 추가(조사 이력은 보존)
- 참조가 전무한 `secondary_data/` 4개 파일 삭제
- `intermediate_results/` 용량 6.4MB → 216KB
- **자기장 데이터는 타사 경로를 쓰지 않고**, `primary_data/match_*.json`의 `asset` 항목에 있는 크래프톤 공식 텔레메트리 URL을 쓰는 방향으로 정리

`scripts/`의 조사 기록 자체는 남김. 다만 38~41번이 참조하던 파일이 삭제되어 해당 스크립트들은 실행 불가 상태임을 명시.

### 3. 크롤러 제거

• 현상
README가 "LIVE DATA CRAWLER ENGINE"으로 소개하고 매일 새벽 4시 스케줄러가 동작했으나, 실제로는 아무것도 크롤링하지 않음.

• 원인
`parseAndApplyProSettings()`가 DPI를 파싱해 지역변수에 담고 사용하지 않았고(죽은 코드), `crawlAllPlayers()`는 외부 요청 없이 `lastCrawledAt`만 현재시각으로 갱신한 뒤 "전체 선수 N명의 데이터가 성공적으로 최신화되었습니다"를 반환. 즉 **실제로는 갱신되지 않았는데 "방금 최신화됨"이라는 거짓 타임스탬프를 매일 남기고 있었음.**

• 조치
선수 감도·장비 데이터를 디스코드로 수집하기로 방향이 정해져 ProSettings 크롤링 경로가 계획에서 제외됨. `CrawlerService`·`CrawlerController`·`CrawlerStatusDto` 삭제, `WebConfig`의 `@EnableScheduling` 및 `build.gradle`의 Jsoup 의존성 제거.

### 4. 관리자 API 제거

• 현상
`/api/admin/*` 6개 엔드포인트에 인증이 없어 8080 포트에 접근 가능한 누구나 팀·선수를 삭제할 수 있었음. 호출자는 0곳.

• 원인
Spring Security 의존성 자체가 없음. 더불어 `ddl-auto: create` 때문에 **이 API로 입력한 데이터는 재기동 시 사라지므로 애초에 사용할 수 없는 구조**였음.

• 조치
`AdminController`·`AdminService`·`AdminTeamRequestDto`·`AdminPlayerRequestDto` 삭제. 향후 관리자 화면이 필요하면 인증과 함께 신규 구현하는 것이 낫다고 판단.
아울러 디스코드로 수집한 데이터는 API가 아니라 **시드 파일 경로**로 유입해야 함을 문서화(`ddl-auto` 전환 전까지).

### 5. 선수 상세 모달의 창작 데이터 제거

• 현상
모든 PWS 선수의 상세 모달이 FOV 103, 해상도 1920x1080, 마우스패드·키보드·헤드셋·모니터를 **검증된 값인 것처럼 표시**하고 있었음.

• 원인
`PlayerDetailModal.jsx`가 `player.setting?.X || player.X || <하드코딩 기본값>` 형태의 폴백 체인을 사용. API(`RosterPlayerDto`)는 `dpi`·`sens`·`mouse`만 전송하고, `DataInitializer`는 실측값이 없어 FOV·해상도를 의도적으로 null로 두므로, 모든 선수가 동일한 하드코딩 값을 표시함. 트로피 하나를 확인하려 보고서 2건을 작성한 프로젝트에서 가장 눈에 띄는 화면이 데이터를 지어내고 있었음.

• 조치
폴백 상수를 전부 제거하고 `pick()` 헬퍼로 실제 값만 선택, 값이 없으면 `미등록` 표시(흐린 색). 기어 5개 카테고리는 계속 노출하되 비어 있는 항목을 드러내 **디스코드로 수집해야 할 항목이 화면에서 보이도록** 함. 백엔드 `SettingDto`가 `aimingSens`로 내보내는데 모달이 `aimSens`를 읽던 불일치도 함께 수정.

### 6. 공식 API 서비스의 가짜 대회 폴백 제거

• 현상
`PubgOfficialApiService.getStandardMajorTournaments()`가 API 호출 실패 시 하드코딩된 대회 목록("Esports World Cup 2026 / $2,000,000", "PNC 2026 / 서울" 등)을 `source: "KRAFTON_OFFICIAL_API"` 라벨과 함께 반환. 5번 항목과 동일한 문제의 백엔드판.

• 조치
하드코딩 목록 61줄 삭제. 실패 시 빈 목록을 그대로 반환하고 경고 로그를 남기도록 변경. 실패 응답은 캐시하지 않음.

### 7. 히트엔딩 탭의 창작 서술 제거

• 현상
`HitEndingTab.jsx`에 실존 프로 선수(Xmpl, seoul, Salute, TGLTN)에 대한 출처 없는 경기 서술이 하드코딩되어 있었음("연막 속에서 침착하게 헤드샷 2킬을 꽂아 넣으며…" 등). 검증 근거가 전무.

• 조치
전부 제거하고 "준비 중" 안내로 대체. 실제 기능(서클 축소 재생, 지형 편향 분석, 맵별 비교, 이미지·영상 출력)과 선행 조건(텔레메트리 수집 파이프라인)을 명시.

### 8. 대회 탭 순위표 버그 수정

• 현상
대회 선택 탭이 동작하는데 순위표는 항상 PGS4를 표시. PWS를 선택해도 PGS4 순위가 나왔음.

• 원인
`TournamentsTab.jsx:9`의 `const leaderboard = LEADERBOARD_PGS4;` 가 `selectedTourneyId`를 무시.

• 조치
정적 데이터에 대회 연결 키가 없으므로, PGS4 선택 시에만 렌더하고 다른 대회는 "순위 데이터가 없습니다" 빈 상태를 표시.

### 9. 리그 복제 구조 리팩터

• 현상
`PlayersTab.jsx` 600줄 한 파일에 칩 필터·검색·`fetch`·프로시드 그리드·퀄리파이어 그리드·카드 렌더러·HOT 그리드·플레이스홀더가 모두 있었음. 프론트엔드 전체에서 백엔드 호출은 이 파일의 인라인 `fetch` 한 줄뿐.

• 원인
데이터 계층이 없어, PCL·EMEA·AMER·APAC·HOT·대회로 확장하면 로딩·에러·재시도 코드가 5~7벌 복사될 구조였음. "PWS를 템플릿으로 복제한다"는 전략에서 템플릿이 복제에 부적합한 형태.

• 조치
```
api/client.js                     백엔드 호출 공통 래퍼 (에러 메시지 정규화)
api/teams.js                      fetchTeamCards(league)
hooks/useApi.js                   { data, loading, error, reload }
components/common/LoadingPanel.jsx
components/common/ErrorPanel.jsx  재시도 버튼 포함
components/players/PlayersTab.jsx     칩 + 검색 + 분기만 (600줄 → 108줄)
components/players/LeagueTeamGrid.jsx league prop 하나로 동작 — 복제 단위
components/players/TeamCard.jsx
components/players/HotPlayerGrid.jsx
```
`LeagueTeamGrid`가 조회·검색 필터·프로/퀄리파이어 분리·로딩/에러/빈 상태를 모두 담당. 5개 리그가 **같은 컴포넌트에 prop만 다른 5개 인스턴스**가 되어, 리그 추가는 `PlayersTab.jsx`의 `LEAGUES` 배열에 한 항목을 넣는 작업으로 축소됨.
"Coming Soon" 플레이스홀더를 제거하고 PCL·EMEA·AMER·APAC을 실제로 API에 연결.

### 10. 죽은 코드 및 매달린 클래스 정리

참조 0건을 grep으로 확인한 뒤 삭제:
`frontend/src/data/mockData.js`(빈 배열만 export), `frontend/src/components/TeamRosterView.jsx`(255줄, 스키마 불일치), `frontend/public/logos/teams/sl.png`(탈락 팀), `PlayerHighlightRepository`, `PlayerSettingRepository`, `PlayerGearRepository`, `PlayerHighlight`+`HighlightDto`(생성 코드 없어 항상 빈 배열, `Player.highlights`·`addHighlight()`·`PlayerDetailResponseDto.highlights` 함께 제거), `PROJECT_OVERVIEW.md`(CLAUDE.md와 80% 중복이며 어긋나는 곳은 전부 사실과 다름), `scripts/70`(입력이 사라져 무용).

`esportsData.js`의 `LATEST_PWS2_TEAMS` 1,092줄 제거 — 어떤 컴포넌트도 읽지 않고 `primary_data/pws2_teams_verified.json`이 단일 원천이 되었기 때문. **다만 번들 크기 효과는 없었음**(192.07 → 191.39 kB). Vite가 이미 tree-shaking으로 미사용 export를 제외하고 있었고, 계획 단계에서 "1,090줄이 브라우저로 전송된다"고 판단한 것은 오류였음. 제거의 실제 근거는 동일 데이터가 두 곳에 존재해 드리프트할 수 있는 상태를 없앤 것.

### 11. 문서 정정

`CLAUDE.md`는 매 세션 자동 로드되므로 사실 오류가 누적되면 이후 작업 판단을 오염시킴. 다음을 정정:
- `mockData.js`가 폴백이라는 서술(실제로는 참조 0건의 빈 파일) — 초기 작성 시 README·PROJECT_OVERVIEW를 근거로 삼아 들어간 오류
- `TournamentsTab`이 `TeamRosterView`를 렌더한다는 서술(실제로는 import 0건)
- 히트엔딩 탭을 "감도/FOV 계산기"로 설명(실제로는 명장면 아카이브였고 현재는 준비 중)
- 이번 세션의 삭제 반영(Jsoup, 크롤러, 관리자 API, `PlayerHighlight`, `secondary_data/`, script 70)
- 신규 반영: 리그 추가 방법, `api/`·`hooks/` 사용 규칙, 환경변수 주입 실행법, 기동 레이스, 알려진 고장

---

## 검증 결과

### 빌드
- `./gradlew compileJava` 통과
- `npm run build` 통과 (번들 192.07 → 189.54 kB)
- 삭제한 심볼에 대한 참조 grep **0건** (백엔드·프론트 양쪽)
- 파이썬 스크립트 20개 `py_compile` 통과
- 추적 파일 전수 자격증명 스캔 **0건** (`eyJ0eXAiOiJKV1Q`, `sb_publishable_`, `sb_secret_`)

### API
- `GET /api/teams/cards?league=PWS` → 24팀 (pro 13 / amateur 11, 트로피 보유 7팀, 로스터 96명)
- `GET /api/teams/cards?league=PCL` → `[]`
- DB 직접 조회로 `seed_type`이 있는 팀 24개, PWS+pro 13 / PWS+amateur 11 확인

### 브라우저 실측
- PE탭 PWS: 리팩터 전과 동일 (팀 카드, 로고, 태그, 로스터, 검색)
- PE탭 PCL: "PCL 등록된 팀이 없습니다" 빈 상태 — 복제 구조 동작 확인
- 선수 모달: 실제 값(800 DPI / 감도 32 / 마우스)만 표시, 나머지 6개 항목 `미등록`
- HOT 탭: 정적 데이터에 실제 값이 있는 선수는 전부 표시 (회귀 없음)
- 대회 탭: PGS4 선택 시 순위표 정상, PWS 선택 시 "순위 데이터가 없습니다"
- 히트엔딩 탭: "준비 중" + 계획 기능 4개 안내
- 백엔드 종료 후 새로고침 → 에러 패널 + 재시도 버튼, 재기동 후 재시도 클릭 시 정상 로드
- 콘솔 에러 0건
- 기동 로그에 스케줄러 흔적 0건

### 검증하지 못한 항목
**`GET /api/tournaments/official` 은 500을 반환하여 6번 항목(가짜 폴백 제거)을 실제 응답으로 확인하지 못했음.** 코드 변경과 컴파일만 확인함.
원인은 이번 변경과 무관한 기존 결함으로, `PubgTournamentController`의 `@CrossOrigin(origins = "*")`와 `WebConfig`의 `allowCredentials(true)`가 충돌해 Spring이 요청을 거부함(`IllegalArgumentException`). 이 엔드포인트는 작성 이후 한 번도 동작한 적이 없으며, 프론트엔드가 사용하지 않은 이유이기도 함.

### 작업 중 발견한 기동 레이스
`DataInitializer`가 `CommandLineRunner`라 웹 서버가 요청을 받기 시작한 **이후에** 실행됨. 기동 직후 수 초간 `/api/teams/cards`가 빈 배열을 반환하며, 이로 인해 한 차례 오진이 있었음. 준비 상태 확인은 HTTP 200이 아니라 기대 행 수(24팀)로 판단해야 함. `CLAUDE.md`에 기록.

---

## 다음 단계

### 즉시 필요 (사용자 조치)
**PUBG API 키 재발급.** 코드는 환경변수 참조로 바꿨으나 옛 키는 커밋 `ba3a8d5` 히스토리에 잔존. 저장소가 Private이라 즉각적 위험은 낮지만, 파일 수정으로는 무효화되지 않음.

### 다음 작업 후보와 각각의 선행 조건

| 작업 | 선행 조건 | 현재 상태 |
|---|---|---|
| 다른 리그(PCL·EMEA·AMER·APAC) | 검증된 시드 데이터 | **코드는 준비 완료.** 시드만 넣으면 화면이 채워짐 |
| 선수 상세 실데이터 | 디스코드 수집 체계 | 유입 경로는 시드 파일로 확정. 화면에 `미등록`이 드러나 수집 대상이 명확 |
| HOT 탭 (기간별 조회수) | `ddl-auto: create` → Flyway 전환 | 조회수는 시드에서 재생성 불가. 현재 구조에서는 재기동마다 0이 되고 "주간 초기화"와 구분되지 않음. 조회 이벤트 기록(롤링 윈도우) 방식 권장 |
| 대회 탭 (순위·선수 스탯) | `scripts/49~51`의 집계 로직을 Java로 이식 | 파이썬 파이프라인이 실제 PWS2 S11 데이터로 SUPER 룰셋 순위표와 선수 스탯을 이미 산출. 엔티티(`TournamentTeamResult`·`TournamentPlayerStat`)도 존재. 약 80% 완성 |
| 히트엔딩 (서클·지형 분석) | 반복 실행 텔레메트리 파이프라인 | 공식 텔레메트리 URL이 `primary_data/match_*.json`에 있음. 다수 경기 집계가 필요하므로 일회성 스크립트가 아닌 반복 가능한 수집 단계가 선행돼야 함. 맵 이미지 에셋 확보도 과제 |

### 미룬 정비
- `/api/tournaments/official` CORS 충돌 (대회 탭 착수 시 함께)
- `TournamentController`와 `PubgTournamentController`의 `/api/tournaments` 중복 매핑 — 현재는 Spring이 리터럴 경로를 우선해 우연히 동작
- 로고 이미지 최적화 (`vex.png` 1.6MB 포함 총 3.1MB, 화면에서는 54px로 렌더)
- `README.md` 재작성 (현재 존재하지 않는 탭 4개와 파일 4개를 설명, 모순 17건)
- LICENSE 파일 부재 (README는 MIT라고 명시)
- 테스트 부재 (`backend/src/test` 디렉터리 자체가 없음)
