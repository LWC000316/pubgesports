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

**트로피는 더 이상 다루지 않는다** (2026-09-29 결정). 엔티티·DTO·시드 필드를 전부 제거했다.
PWS 때 사람이 읽어 확정했으나 두 번 정정이 있었고(보고서 26·27) 화면에서도 쓰이지 않았다.
당시 기록은 `scripts/66·68·69` 와 보고서 25·26·29 에 감사 기록으로 남아 있다.

## 리그별 결정

`seedType` 은 **화면 제목이 아니라 정렬 키**다. 팀 목록은 **구획 없이 한 줄기**로 나오고,
프로로 볼 수 있는 구단이 앞, 아마추어 구단이 그 뒤에 이어진다. 구획 제목도 구분선도 없다
(`LeagueTeamGrid.jsx` 의 `SEED_ORDER`). **그룹에 이름을 붙이려는 시도를 두 번 했고 두 번 다
위키가 뒷받침하지 않는 주장을 만들어냈다.** 리그마다 `pro` 의 근거가 다르기 때문이다.

| 리그 | 대상 | 상단 / 하단 | `pro` 가 실제로 근거하는 것 |
|---|---|---|---|
| PWS | 2026 Phase 2 · 24팀 | 13 / 11 | 위키가 직접 `text=Pro Seed` 로 표기 |
| PCL | 2026 Autumn **Stage S** · 24팀 | 8 / 16 | Stage S 직행 시드 8팀. 위키에 `invite` 가 없어 사람이 확정 |
| EMEA | 2026 Fall · 29팀 | 9 / 20 | Global Partner 3 · Regional Partner 5 · PGS Attending 1 |
| AMER | 2026 Series 2 · 29팀 | 7 / 22 | Global Partner 1 · Regional Partner 5 · PGS Attending 1 |
| PVS | 2026 Phase 2 · 16팀 | 3 / 13 | 직전 Phase 1 파이널 1~3위 |
| PTS | 2026 **Phase 2** · 24팀 | 18 / 6 | **없음** — `{{Qualification\|method=invite}}` 뿐. 이 리그의 순서에는 실질적 의미가 없다 |

`seedType` 은 여전히 **모든 팀에 값이 있어야 한다.** `findByLeagueWithPlayers` 가
`seedType IS NOT NULL` 로 거르므로 비우면 팀이 화면에서 사라진다.

**`--seed-from-qualification` 의 결과를 그대로 믿지 말 것.** 이 플래그는 `invite→pro`,
`qual→amateur` 로 기계적으로 옮길 뿐이고, 그 매핑이 맞는지는 **리그마다 `text=` 값을 직접
봐야 안다.** 처음 여섯 리그를 수집할 때 PWS 에서만 참인 규칙을 전부에 적용해서, PTS 는 근거
없이 20팀이 프로가 되고 PVS 는 **컵 1위 팀이 아마추어로** 들어갔다 (2026-09-29 정정).

여섯 리그 모두 수집 완료. **재수집이 필요한 것은 EMEA·AMER·PTS 셋**이다
(EMEA·AMER 2026-10-04, PTS 2026-10-08 종료 예정. 셋 다 진행 중에 수집했다).

## 먼저 돌릴 것 — 최신성 점검

```bash
python ingest/check_freshness.py            # 여섯 리그 전부 (약 1분)
python ingest/check_freshness.py --league PTS
```

**아무것도 쓰지 않는다.** 세 가지를 본다.

1. 같은 시리즈에 더 최근 대회가 생겼는가
2. 지금 대회의 참가팀·로스터가 시드와 달라졌는가
3. 대회가 끝났는데 그 뒤로 다시 수집하지 않았는가

`STALE` 이면 재수집, `WARN` 이면 진행 중이라 예상된 변동일 수 있다. 조치가 필요하면 종료 코드 1.

기준이 되는 파일은 `primary_data/_sources.json` 이다. **리그를 다시 수집하면 이 파일의
`page`·`collectedAt` 도 반드시 같이 고칠 것.** 리그별 예외도 여기 적는다.

| 키 | 뜻 |
|---|---|
| `teamAliases` | 시드 표기 → 위키 표기. PWS 6팀이 `scripts/59` 시절 표기라 다르다 |
| `subset` | 시드가 문서 참가팀의 부분집합. PCL 은 40팀 중 Stage S 24팀 |
| `rostersFromHtml` | 로스터를 렌더 HTML 에서 읽어야 하는 대회 (PTS Phase 2) |
| `latestConfirmedAt` | 시작일이 없어 자동 판정이 안 되는 대회를 사람이 최신이라 확인한 날 (PVS) |

## 대회를 고를 때 — 종료 여부가 아니라 최신 여부를 본다

PTS 는 처음에 **Phase 1(2026-04-28~05-12)** 로 수집했다. "종료된 대회라 안전하다"고 판단했는데
그때 이미 **Phase 2 가 09-21 에 시작**해 있었다. 결과적으로 5개월 지난 명단이 화면에 떠 있었고,
Phase 2 로 바꾸니 **24팀 중 9팀이 교체**되고 유지된 15팀 중 12팀의 주전이 달라졌다.

새 리그·새 시즌을 수집할 때는 먼저 시리즈의 하위 문서를 전부 나열해 **가장 최근 것**을 고른다:

```bash
python - <<'EOF'
import sys; sys.path.insert(0,'ingest')
from mediawiki_client import MediaWikiClient
c=MediaWikiClient()
r=c.get({'action':'query','list':'allpages','apprefix':'PUBG Thailand Series/2026',
         'aplimit':'200','apfilterredir':'nonredirects'})
for p in r['query']['allpages']:
    if p['title'].count('/')==2: print(p['title'])
EOF
```

## `import=true` — 로스터가 원문에 없는 경우

`{{Opponent|FULL SENSE|import=true}}` 로 적힌 팀은 로스터를 **팀 문서에서 주입**하므로
위키 원문에 선수가 없다. 원문만 읽으면 그 팀이 **선수 0명으로 조용히 들어간다.**
PTS 2026 Phase 2 의 7팀이 이 경우였다.

수집기는 원문에 `import=true` 가 하나라도 있으면 **멈추고** `--rosters-from-html` 을 요구한다.
이 옵션은 렌더된 HTML 의 `team-participant-card` 를 읽는다. 카드의 Main/Subs/Staff 탭을
라벨로 구분해 스태프를 빼고, `DNP`(출전하지 않음) 역할은 교체 선수로 다룬다.

**PVS 는 종료됐다.** Results 의 Week 3·4 가 `finished=` 로 비어 있지만 이는 미진행이 아니라
대회가 2주차까지만 치르고 끝났기 때문이다(사용자 확인, 2026-09-29). 참가 16팀은 확정이며
재수집 대상이 아니다. **위키의 빈 `finished=` 를 "진행 중"으로 단정하지 말 것.**

**스태프 제외 규칙**: `type=staff` 뿐 아니라 `role=` 이 붙은 사람은 전부 비선수다.
확인된 값은 Coach / head coach / Assistant Coach / Analyst 이며 선수에는 `role=` 이 없다.
예전에는 `type=staff` 와 `role=Coach` 만 걸러서 `role=analyst` 가 선수로 새어 들어갔다
(PVS Team Flash 의 NielT).

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

---

# 선수 감도·장비 수집 (디스코드)

리퀴피디아에도 공식 API 에도 **감도·장비 데이터는 없다.** 사람이 모아서 시드 파일에
직접 적는다. 자동 수집 경로는 존재하지 않는다 (해외 사이트들도 전부 수작업이다).

## 시드 형식

선수 항목에 `setting` 과 `gears` 를 넣는다. **있는 값만 적는다 — 모르는 값은 키를 뺀다.**
빠진 값은 화면에 `미등록` 으로 나온다. 그게 올바른 상태다.

```json
{
  "nickname": "Rain1ng",
  "realName": "Rain1ng",
  "role": "Player",
  "setting": {
    "mouseDpi": 800,
    "generalSens": 47,
    "aimingSens": 45,
    "adsSens": 35,
    "scope2xSens": 30,
    "scope3xSens": 28,
    "scope4xSens": 25,
    "scope6xSens": 20,
    "verticalMultiplier": 1.0,
    "fov": 103,
    "resolution": "1920x1080",
    "screenMode": "전체 화면",
    "renderScale": 100
  },
  "gears": [
    { "category": "MOUSE",    "name": "Razer Viper V3 Pro", "brand": "Razer" },
    { "category": "MOUSEPAD", "name": "..." },
    { "category": "KEYBOARD", "name": "..." },
    { "category": "HEADSET",  "name": "..." },
    { "category": "MONITOR",  "name": "..." }
  ]
}
```

- `setting` 13개 필드는 모두 선택이다. 없으면 키를 넣지 않는다
- `gears` 의 `category`·`name` 은 필수, `brand`·`imageUrl`·`purchaseLink` 는 선택
- 화면에 구획이 나오는 카테고리는 `MOUSE`·`MOUSEPAD`·`KEYBOARD`·`HEADSET`·`MONITOR` 다
- **기본값을 넣지 말 것.** 예전에 전원에게 800/32/동일 마우스를 찍어 넣어 실측처럼
  보이게 한 적이 있다. 2026-09-29 에 392명분(3840개 값)을 전부 지웠다

## 반영 방법

시드 파일을 고친 뒤 **`SEED_MODE=always` 로 한 번 기동**해야 DB 에 들어간다.
기본값 `auto` 는 `teams` 가 비었을 때만 적재하므로 변경이 반영되지 않는다.

```bash
cd backend && SEED_MODE=always ./gradlew bootRun
```

## 선수 식별

닉네임은 리그 간에 겹칠 수 있다. 화면에 나오는 팀끼리 겹치는 건 현재 `Lu` 하나뿐이지만
(PCL Golden Quester Gaming / EMEA Twisted Minds), 수집이 늘면 더 나온다.
**`리그 + 팀 + 닉네임`** 으로 특정한다. `players.id` 는 쓰면 안 된다 — 재적재 때 바뀐다.

## 화면까지 도달하는 경로

```
시드 파일 setting/gears
  -> DataInitializer.applySettingAndGears()   13개 필드 + 장비 전부
  -> player_settings / player_gears
  -> GET /api/players/{id}                    SettingDto + GearDto
  -> PlayerDetailModal                        모달을 열 때 이 API 를 호출한다
```

팀 카드(`/api/teams/cards`)의 roster 에는 `dpi`·`sens`·`mouse` 세 개만 실린다.
146팀 전부에 전체 세팅을 실으면 응답이 과해지기 때문이다. 나머지는 모달이 따로 받는다.
