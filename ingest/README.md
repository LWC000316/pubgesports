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

## 리퀴피디아 API 는 두 개다 — 어느 쪽을 쓸지 먼저 정한다

| | MediaWiki API | LPDB v3 |
|---|---|---|
| 주소 | `liquipedia.net/pubg/api.php` | `api.liquipedia.net/api/v3` |
| 키 | **불필요 (공개)** | 승인 필요 |
| 받는 것 | 위키 원문(wikitext) → 직접 파싱 | 정규화된 레코드 |
| 이 레포의 사용 이력 | **`scripts/59`·`63` 등 8개가 이미 사용** | 아직 없음 |

**이 디렉터리(`ingest/`)는 LPDB v3 용이다.** 키가 없으면 돌릴 수 없다.

**키가 없어도 리그를 추가할 수 있다.** 현재 PWS 24팀 데이터가 MediaWiki 경로로 들어왔다.
`scripts/59_fetch_liquipedia_pws_teams.py` 가 `action=parse` 로 대회 문서 원문을 받아
`{{Opponent|팀명}}` / `{{Person|닉네임}}` 을 정규식으로 뽑고, `scripts/63` 이 `action=query`
로 로고 이미지 URL 을, `65` 가 파일을 받았다. 같은 방식을 다른 리그에 쓸 수 있다.

**선택 기준**: 지금 당장 필요하면 MediaWiki, 문서 형식 변경에 덜 깨지는 안정성을 원하면
LPDB. MediaWiki 는 위키 문법을 정규식으로 파싱하므로 문서 구조가 바뀌면 깨진다.

## LPDB v3 준비

```bash
export LIQUIPEDIA_API_KEY=...          # 승인받은 LPDB v3 키
export LIQUIPEDIA_CONTACT=you@example.com   # 약관상 User-Agent 에 연락처가 필요
```

키는 자가 발급이 안 된다. 약관(<https://liquipedia.net/api-terms-of-use>)에는
"Upon approved request Liquipedia grants access" 와 문의 창구가
**디스코드(<https://liquipedia.net/discord>)** 라는 것만 적혀 있다. 신청 양식도,
접수 상태를 조회하는 페이지도 없다 — 디스코드로 직접 문의해야 한다.
(비영리·커뮤니티 프로젝트의 무상 여부는 약관 문서에서 확인하지 못했다. 문의할 때 같이 확인할 것.)

**키를 추적 파일에 쓰지 않는다.** 예전에 PUBG API 키가 21곳에 복붙돼 있었고 커밋
`d8f04a7` 에서 전부 환경변수로 옮겼다.

MediaWiki 경로도 약관상 **연락처가 포함된 User-Agent** 와 gzip 수락이 필요하다.
`scripts/59` 의 User-Agent 에 있는 `contact@pubgproject.local` 은 존재하지 않는 도메인이므로
재사용할 때 실제 연락처로 바꿀 것.

## 리그 하나 추가하기 (MediaWiki 경로 — 키 불필요, PCL 을 이걸로 했다)

```bash
# 1. 문서 구조를 눈으로 먼저 본다. 파서를 추측으로 쓰지 않는다.
python ingest/mediawiki_client.py "PUBG_Champions_League/2026/Autumn" --what wikitext

# 2. 초안 생성 + 로고 내려받기
python ingest/build_league_seed_mediawiki.py \
    --page "PUBG_Champions_League/2026/Autumn" \
    --league PCL --region CN \
    --seed-map ingest/seed_types_pcl.json --include-subs --download-logos \
    --out intermediate_results/pcl_seed_draft.json

# 3. 형식 검사
python ingest/verify_seed.py intermediate_results/pcl_seed_draft.json --compare-league PCL

# 4. 사람이 원문과 대조한 뒤 확정
#    primary_data/<리그>_teams_verified.json

# 5. 배선: DataInitializer.VERIFIED_SEEDS 에 경로 한 줄,
#    PlayersTab.jsx 의 해당 리그에 bannerTitle 과 sourceUrl
```

**PCL 에서 실제로 걸린 것들** (다른 리그에서도 나올 수 있다)
- 위키 원문의 `{{Opponent|jdg}}` 는 **팀 이름이 아니라 리퀴피디아 내부 코드**다. 정식명은
  렌더된 HTML(`prop=text`)의 참가팀 카드에서만 얻을 수 있다. 원문 코드 순서와 HTML 카드
  순서를 대응시키되, **개수가 다르면 멈춘다**(순서 대응을 신뢰할 수 없으므로).
- **팀 약칭(`tag`) 데이터가 리퀴피디아에 없다.** 팀 문서 인포박스에도, `Template:<코드>` 에도
  없다. 현재는 내부 코드를 대문자로 올리고 동명 구분자(`cn` 등)를 뗀 **추정값**을 쓰며,
  시드의 `tagSource` 에 그 사실을 남긴다.
- 동명 팀은 문서명이 `ZEAL (Chinese team)` 처럼 된다. `clean_team_name()` 이 `(... team)` 을 뗀다.
- 참가팀이 스테이지별 소절로 나뉠 수 있다. PCL 은 Stage S 8 / A 8 / B 24 = 40 이고,
  Stage S 에 오르는 24팀은 세 소절에 흩어져 있어 `--seed-map` 으로 골라냈다.
- 로고 `src` 는 썸네일이라 원본 경로로 바꿔야 한다(`_full_size_image`).

## 리그 하나 추가하기 (LPDB 경로 — 키가 있을 때)

3~4단계(검사·대조)와 5단계(배선)는 경로와 무관하게 동일하다.

```bash
# 1. 응답의 진짜 필드명을 먼저 본다. 매핑은 아직 추정이다.
python ingest/build_league_seed.py --dump-fields --page "PUBG_Champions_League/2026"

# 2. 초안 생성 (seedType 은 대회 구조를 보고 사람이 정한다)
python ingest/build_league_seed.py \
    --page "PUBG_Champions_League/2026" \
    --league PCL --region CN \
    --seed-map ingest/seed_types_pcl.json --only-mapped \
    --out intermediate_results/pcl_seed_draft.json

# 3. 형식 검사
python ingest/verify_seed.py intermediate_results/pcl_seed_draft.json --compare-league PCL

# 4. 대조 후 승인되면 옮긴다
#    cp intermediate_results/pcl_seed_draft.json primary_data/pcl_teams_verified.json

# 5. 백엔드 DataInitializer.VERIFIED_SEEDS 에 경로 한 줄 추가
#    프론트 PlayersTab.jsx 의 LEAGUES 에는 PCL·EMEA·AMER·APAC 이 이미 있다.
#    해당 리그 항목에 sourceUrl(대조에 쓴 리퀴피디아 문서)을 넣는다 — 출처 표기에 쓰인다
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

## 리그별 결정

| 리그 | 대상 | seedType 구분 | 구분표 |
|---|---|---|---|
| PWS | 2026 Phase 2 참가 24팀 | pro 13 / amateur 11 (프로 시드 / 예선 통과) | 시드 파일에 직접 기록 |
| PCL | 2026 Autumn **Stage S** 참가 24팀 | pro 8 (Stage S 직행) / amateur 16 (하위 스테이지에서 올라옴) | `seed_types_pcl.json` |
| EMEA | 2026 Fall 참가 29팀 | pro 9 (`method=invite`) / amateur 20 (`method=qual`) | **자동** — `--seed-from-qualification` |
| AMER | 2026 Series 2 참가 29팀 | pro 7 (`method=invite`) / amateur 22 (`method=qual`) | **자동** — `--seed-from-qualification` |

아직 안 한 리그: **PTS**(태국, 최신 `PUBG_Thailand_Series/2026/Phase_1`, 24팀, 종료됨),
**PVS**(베트남, 최신 `PUBG_Vietnam_Series/2026/Phase_2`, 16팀, 인포박스에 날짜가 비어 있어
시작 여부 확인 필요). 탭과 로고는 이미 있고 시드 파일만 없다.

**EMEA 는 구분표가 필요 없다.** Stage 소절이 없는 대신 팀마다 `|qualification={{Qualification|method=...}}`
가 있어서 초청(invite)과 예선 통과(qual)를 위키 데이터에서 그대로 가를 수 있다.
다른 리그도 이 형식이면 `--seed-from-qualification` 을 먼저 시도할 것.

`tag` 는 리그마다 성격이 다르다. PCL 은 코드가 진짜 약칭(`jdg`→JDG)이지만 EMEA 는 코드가
팀 이름 그대로(`Natus Vincere`)라 대문자로 올려봐야 의미가 없다. `code_to_tag()` 가
코드와 팀명이 같으면 빈 값을 돌려주고, 그때는 로고 파일명을 팀명에서 만든다.

PCL 은 40팀이 Stage B·A·S 세 단계로 나뉘어 PWS 와 구조가 다르다. 사용자 결정으로 Stage S 24팀만
싣고, 직행/승격을 pro/amateur 로 대응시켰다. 공식 API 대회 ID 는 `cn-pclas26`.

## 파일

| 파일 | 하는 일 |
|---|---|
| `liquipedia_client.py` | LPDB v3 호출. 인증·호출 한도·캐시·gzip. 단독 실행하면 응답 덤프 |
| `build_league_seed.py` | 대회 문서 하나 → 시드 초안 JSON |
| `verify_seed.py` | 초안 형식 검사와 레거시 비교. 네트워크를 쓰지 않는다 |
| `seed_types_pcl.json` | PCL 팀명 → seedType 구분표 |

## 아직 확인하지 못한 것

`build_league_seed.py` 상단의 `*_KEYS` 매핑은 **실제 응답으로 확인하기 전의 추정**이다.
키를 받으면 `--dump-fields` 를 먼저 돌려 진짜 필드명을 보고 그 부분을 고쳐야 한다.
로고 URL 을 LPDB `team` 이 주지 않으면 MediaWiki `imageinfo` 를 병행해야 한다
(`scripts/63` 에 전례가 있다).
