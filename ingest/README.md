# ingest — 리그 시드 수집 도구

`scripts/` 는 지난 조사의 **기록**이고 다시 돌리는 물건이 아니다. 이 디렉터리는 반대로
**반복 실행하는 도구**다. PCL 을 채운 절차를 EMEA·AMER·APAC 에 그대로 다시 쓰기 위한 것이다.

## 데이터가 흐르는 길

```
리퀴피디아 LPDB v3
  → build_league_seed.py   초안 JSON (intermediate_results/)
  → verify_seed.py         형식 검사
  → 사람이 원문과 대조       ← 이 단계를 건너뛰지 않는다
  → primary_data/<리그>_teams_verified.json
  → DataInitializer 가 기동 때 적재 → /api/teams/cards?league=<리그>
```

## 준비

```bash
export LIQUIPEDIA_API_KEY=...          # 리퀴피디아에서 승인받은 LPDB v3 키
export LIQUIPEDIA_CONTACT=you@example.com   # 약관상 User-Agent 에 연락처가 필요
```

키는 자가 발급이 안 된다. <https://liquipedia.net/api-terms-of-use> 의 문의 양식으로
신청해 승인을 받아야 한다. 교육·비영리·커뮤니티 프로젝트는 무상이다.

**키를 추적 파일에 쓰지 않는다.** 예전에 PUBG API 키가 21곳에 복붙돼 있었고 커밋
`d8f04a7` 에서 전부 환경변수로 옮겼다.

## 리그 하나 추가하기

```bash
# 1. 응답의 진짜 필드명을 먼저 본다. 매핑은 아직 추정이다.
python ingest/build_league_seed.py --dump-fields --page "PUBG_Champions_League/2026"

# 2. 초안 생성 (seedType 은 대회 구조를 보고 사람이 정한다)
python ingest/build_league_seed.py \
    --page "PUBG_Champions_League/2026" \
    --league PCL --region CN \
    --seed-map ingest/seed_types_pcl.json \
    --out intermediate_results/pcl_seed_draft.json

# 3. 형식 검사
python ingest/verify_seed.py intermediate_results/pcl_seed_draft.json --compare-league PCL

# 4. 대조 후 승인되면 옮긴다
#    cp intermediate_results/pcl_seed_draft.json primary_data/pcl_teams_verified.json

# 5. 백엔드 DataInitializer.VERIFIED_SEEDS 에 경로 한 줄 추가
#    프론트 PlayersTab.jsx 의 LEAGUES 에는 PCL·EMEA·AMER·APAC 이 이미 있다
```

## 지키는 규칙

**약관** — LPDB 는 **시간당 60회**다. `liquipedia_client.py` 가 호출 수를 세어 초과하면
예외를 던지고 멈춘다. 모든 응답은 `intermediate_results/liquipedia_cache/` 에 캐시하며
재실행은 캐시를 먼저 읽는다. 한도를 다 쓴 뒤에도 `--offline` 으로 이어서 작업할 수 있다.

**출처 표기** — 리퀴피디아 콘텐츠는 CC-BY-SA 3.0 이다. 수집한 데이터를 화면에 쓰면
리퀴피디아를 출처로 명시해야 한다. 공개 서비스로 전환할 때 반드시 필요하다.

**지어내지 않는다** — `build_league_seed.py` 는 선수 세팅(`mouseDpi`, `generalSens`,
`mouseName`)을 넣지 않는다. 리퀴피디아에 없는 값이다. 값이 없으면 화면이 `미등록` 을
표시하게 두고, 그럴듯한 기본값으로 채우지 않는다.

`seedType` 도 자동으로 정하지 않는다. `pro` / `amateur` 두 값만 화면에 나오며
(`LeagueTeamGrid.jsx`), 다른 값을 넣으면 팀이 있어도 어느 구획에도 안 들어가 사라진다.
대회 구조를 확인하고 `--seed-map` 으로 명시한다.

**트로피는 자동 수집하지 않는다** — PWS 때 팀 페이지의 1위 기록을 사람이 읽어 확정했고
그 과정에서 두 번 정정이 있었다 (보고서 26·27). 같은 방식으로 확인한다.

## 파일

| 파일 | 하는 일 |
|---|---|
| `liquipedia_client.py` | LPDB v3 호출. 인증·호출 한도·캐시·gzip. 단독 실행하면 응답 덤프 |
| `build_league_seed.py` | 대회 문서 하나 → 시드 초안 JSON |
| `verify_seed.py` | 초안 형식 검사와 레거시 비교. 네트워크를 쓰지 않는다 |

## 아직 확인하지 못한 것

`build_league_seed.py` 상단의 `*_KEYS` 매핑은 **실제 응답으로 확인하기 전의 추정**이다.
키를 받으면 `--dump-fields` 를 먼저 돌려 진짜 필드명을 보고 그 부분을 고쳐야 한다.
로고 URL 을 LPDB `team` 이 주지 않으면 MediaWiki `imageinfo` 를 병행해야 한다
(`scripts/63` 에 전례가 있다).
