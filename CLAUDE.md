# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PUBG PRO VAULT — a full-stack archive of PUBG (PLAYERUNKNOWN'S BATTLEGROUNDS) eSports player profiles/gear/settings plus tournament leaderboards, built as a Spring Boot REST API + React SPA, backed by data pulled from the official Krafton PUBG API and various scraped/Liquipedia sources.

## Tech stack

- **Backend**: Java 17, Spring Boot 3.2.3 (Web, Data JPA), PostgreSQL 16, Lombok. Gradle build. No tests, no Spring Security.
- **Frontend**: React 18, Vite 5, lucide-react, vanilla CSS (no CSS framework, no state library).
- **Infra**: Docker Compose (PostgreSQL only — the app itself runs on the host).
- **Data tooling**: standalone Python scripts under `scripts/` (see the data pipeline section below).

## Commands

### Database (required before running the backend)
```
docker compose up -d
```
Starts PostgreSQL 16 on port 5432 (db `pubg_esports`, user `pubg_user`).

Secrets are read from the environment, never committed. `application.yml` and `docker-compose.yml` reference `${PUBG_API_KEY}`, `${DB_PASSWORD}` etc. with local-dev defaults for the DB only; the PUBG API key has no default, so anything calling the official API needs it exported first:
```
export PUBG_API_KEY=... && cd backend && ./gradlew bootRun
```
The Python scripts under `scripts/` read the same variable via `os.environ["PUBG_API_KEY"]`. Do not paste a key into any tracked file — it was previously duplicated across `application.yml` and 20 scripts.

### Backend (Spring Boot, port 8080)
```
cd backend
./gradlew bootRun          # Windows: gradlew.bat bootRun
./gradlew build            # compile + run tests
./gradlew test             # run tests only
```
There are currently no test sources under `backend/src/test` — `./gradlew test` will pass trivially.

### Frontend (React + Vite, port 5173)
```
cd frontend
npm install
npm run dev       # dev server with /api proxy to localhost:8080
npm run build
npm run preview
```

The backend must be running for the PE tab's PWS section — it fetches from the API and shows an error screen with a retry button when the call fails. There is deliberately no static fallback. The other tabs still render bundled static data and work without the backend.

## Architecture

### Backend: `backend/src/main/java/com/pubg/esports/`
Standard layered Spring Boot app:
- `domain/` — JPA entities: `Team` (carries `tag` and `seedType`) 1—N `Player` 1—1 `PlayerSetting`, 1—N `PlayerGear`; `Team` 1—N `TeamTrophy`; `Tournament` 1—N `TournamentTeamResult` / `TournamentPlayerStat`. Nothing currently seeds the `Tournament` entities, so those tables are always empty and the five `TournamentController` endpoints return `[]` or 500. They are scaffolding kept for the planned 대회 tab.
- `repository/` — Spring Data JPA repos. Only `PlayerRepository` and `TeamRepository` are actually injected anywhere.
- `service/` — `PlayerService` (the only one serving live data), `TournamentService` (reads always-empty tables), `PubgOfficialApiService` (calls the official Krafton PUBG API at `pubg.api.base-url`, filters tournaments by keyword to PWS/PCL/PGS/PGC/PNC/EWC, in-memory cache for the 10 RPM limit). **`PubgOfficialApiService` returns an empty list when the API call fails** — it used to substitute a hardcoded tournament list labeled as official API data; do not reintroduce that.
- `controller/` — `PlayerController` (the live one), `TournamentController`, `PubgTournamentController`.

The crawler (`CrawlerService`/`CrawlerController`, Jsoup) and the unauthenticated admin CRUD (`AdminController`/`AdminService`) were deleted. The crawler never actually scraped anything — its parser discarded the value it parsed, and its 4 AM scheduled job only stamped `lastCrawledAt`, producing a false "just refreshed" timestamp. Player settings/gear will be collected via Discord instead, and under the current `ddl-auto: create` that data has to enter through a seed file, not an API (anything written at runtime is lost on restart).
- `config/DataInitializer.java` — on every startup, wipes and reloads the DB. It loads every file in the `VERIFIED_SEEDS` list first (one per league, same schema as `pws2_teams_verified.json`), then `primary_data/official_teams_and_rosters.json`, skipping any team whose name was already loaded. **The order is load-bearing**: `Team.name` is `unique`, and the legacy file's entries are placeholders (`via.placeholder.com` logos, templated descriptions), so reversing it either violates the constraint or lets placeholder rows win. A seed file that does not exist logs a warning and is skipped — that is the normal state for a league whose data has not been collected yet. Paths are looked up relative to the working directory with a `../` fallback.

**Adding a league on the backend** is one line in `VERIFIED_SEEDS`. `league` has no default: a seed team without a `league` value is skipped with a warning rather than silently loaded as PWS.

**Team card endpoint gotcha**: `GET /api/teams/cards?league=PWS` (backing the PE tab) filters on `seedType IS NOT NULL`, not on league alone. The legacy seed file also contains 25 teams with `league = "PWS"`, so filtering by league only returns 49 teams instead of the intended 24. `seedType` is what marks a team as part of a verified tournament bracket.

**`spring.jpa.hibernate.ddl-auto` is `create`**, so the schema (and all data) is dropped and rebuilt from `DataInitializer` on every backend restart. Don't expect data to persist across restarts, and don't rely on manually-inserted rows surviving a redeploy.

**Repository query gotcha**: `PlayerRepository` deliberately exposes separate `findAllWithTeam` / `findByTeamIdWithTeam` / `searchByQueryWithTeam` / `searchByTeamIdAndQueryWithTeam` query methods instead of one query with optional/nullable JPQL parameters. This is because PostgreSQL's driver infers a `bytea` type for `null`-bound parameters, which breaks `LOWER(?)` with a "function lower(bytea) does not exist" error. `PlayerService.getPlayers` explicitly branches on whether `teamId`/`query` are present and calls the matching method — follow this pattern (explicit branching, not nullable JPQL params) for any new filtered queries.

### Frontend: `frontend/src/`
- `api/client.js` + `api/teams.js` — every backend call goes through here. `apiGet` normalizes failures into Korean messages (a dead backend and a 500 read differently). Add one function per endpoint; do not call `fetch` from a component.
- `hooks/useApi.js` — `{ data, loading, error, reload }`. Re-runs when the caller's `deps` change and resets `data` to the fallback on failure so a previous league's rows never linger.
- `components/common/{LoadingPanel,ErrorPanel}.jsx` — shared states. `ErrorPanel` takes `onRetry`.

**How to add a league** (this is the point of the current structure): append one entry to `LEAGUES` in `components/players/PlayersTab.jsx` and seed that league's teams. `components/players/LeagueTeamGrid.jsx` takes a single `league` prop and handles fetching, search filtering, pro/qualifier splitting, and the loading/error/empty states — all five leagues are the same component with a different prop. `bannerTitle` is optional and only PWS sets it.

- `App.jsx` — top-level tab state machine: `pe` (`components/players/PlayersTab.jsx`), `tournaments` (`TournamentsTab.jsx`), `hit_ending` (`HitEndingTab.jsx`).
- `components/players/` — `PlayersTab` (chips + search + branch only), `LeagueTeamGrid` (the replication unit), `TeamCard`, `HotPlayerGrid`.
- `components/players/TeamCard.jsx` — renders the `{dpi}DPI` badge only when `dpi` is present. Leagues collected from Liquipedia have no measured settings, so the field is absent rather than defaulted.
- `components/PlayerDetailModal.jsx` — per-player popup. Reads `player.setting?.*` / `player.gears[]` first, then flat fields, and renders `미등록` when a value is genuinely absent. **Never reintroduce default values here** — every PWS player used to display a fabricated FOV, resolution and full gear rack as if verified.
- `components/HitEndingTab.jsx` — "준비 중" placeholder. Its previous content was invented match narration attributed to real players; the real feature needs the telemetry pipeline.
- `components/TournamentsTab.jsx` — static. `LEADERBOARD_PGS4` renders only when PGS4 is selected; the static data has no tournament key, so other tournaments show an empty state.
- `data/esportsData.js` — hand-maintained static dataset for the tabs not yet wired to the backend: `HOT_PLAYERS_12`, `TOURNAMENT_LOGOS`, `TOURNAMENTS_DATA`, `LEADERBOARD_PGS4`.
- Vite dev server proxies `/api/*` to `http://localhost:8080` (see `vite.config.js`); it does not proxy in `vite preview`/production builds.

**Startup race**: `DataInitializer` is a `CommandLineRunner`, so it runs *after* the web server accepts requests. For a few seconds after boot, `/api/teams/cards` returns `[]` from a freshly dropped schema. When waiting for readiness, poll for the expected row count (24 PWS teams), not for HTTP 200.

**CORS lives only in `WebConfig`** (`/api/**`, `allowCredentials(true)`). Do not add `@CrossOrigin` to a controller: combining `origins = "*"` with credentials makes Spring reject every request to that controller with a 500. That is exactly why `GET /api/tournaments/official` was broken until it was removed. Without `PUBG_API_KEY` the endpoint returns `[]`.

`TournamentController` and `PubgTournamentController` both use the `/api/tournaments` prefix. This is not a runtime conflict — Spring matches the literal `/official` before the `/{id}` pattern — but keep new literal paths out of `{id}`'s way.

**Known broken**: `GET /api/tournaments/{id}` for a tournament that does not exist returns 500 instead of 404 (`TournamentService` throws `IllegalArgumentException`). The tournament tables are always empty for now, so every id hits this. Fix it when the 대회 tab is built.

### Collecting a new league (`ingest/`)
`ingest/` is the repeatable tooling, as opposed to `scripts/` which is a historical record. `build_league_seed.py` turns one Liquipedia tournament page into a seed draft, `verify_seed.py` checks the draft's shape offline (schema, placeholder detection, roster sizes, diff against the legacy file), and `liquipedia_client.py` handles LPDB v3 auth, the **60-requests-per-hour** limit, and response caching under `intermediate_results/liquipedia_cache/`. See `ingest/README.md` for the full procedure.

Two rules the tooling enforces: it never writes player settings (`mouseDpi`/`generalSens`/`mouseName`) because Liquipedia does not have them, and it never picks `seedType` automatically — only `pro` and `amateur` render (`LeagueTeamGrid.jsx`), so any other value makes a team vanish from the page. Liquipedia content is CC-BY-SA 3.0 and requires attribution on screen.

`LIQUIPEDIA_API_KEY` and `LIQUIPEDIA_CONTACT` come from the environment; the key is not self-service and must be requested and approved.

### Data pipeline (`scripts/`, `primary_data/`, `intermediate_results/`)
`scripts/01_...py` through `scripts/69_...py` are one-off research scripts, numbered in the order they were run, used to source and reconcile tournament/team/roster data from the official PUBG API and Liquipedia. **Treat them as an audit trail, not a runnable pipeline** — several now reference files that were deleted, and the third-party scraped bundles that scripts 30/38–41 depended on are gone (they carried another site's Supabase endpoint and key). There is currently no repeatable ingestion step; the planned telemetry work will need one, and it should live separately from this archive.

Only **two** files under `primary_data/` are read by the application (`DataInitializer`); the other 13 are research artifacts. Do not delete `primary_data/match_*.json` — their `included[]` `asset` entries hold the official telemetry download URLs, which are the only first-party path to circle/zone data.

`primary_data/pws2_teams_verified.json` is the hand-maintained source of truth for the verified PWS bracket (24 teams: name, tag, seedType, logo, trophies, roster — 13 pro / 11 amateur, 7 with trophies). Edit it directly; nothing generates it.

`interim_reports/*.md` holds a dated Korean write-up per work stage — the best source for *why* a given data decision was made.

## Code conventions

Observed consistently in the existing backend code — follow these when adding to it:
- Constructor injection via Lombok `@RequiredArgsConstructor` with `final` fields; no `@Autowired` on fields.
- Read-only services are annotated `@Transactional(readOnly = true)` at class level (`PlayerService`, `TournamentService`).
- Entity→DTO conversion goes through a static `from()` factory on the DTO (`PlayerListResponseDto.from`, `TeamResponseDto.from`), not a mapper class.
- Logging via Lombok `@Slf4j`. Log messages, exception messages, and the `message` field of admin API responses are written in Korean.

## Notes for changes touching data accuracy
Tournament/roster data correctness has been an ongoing, carefully-verified effort (see `interim_reports/20_automated_esports_data_sync_pipeline_evaluation.md` for known limitations: nickname→team-tag parsing ambiguity, team rebrands not reflected in the official API, incomplete group-stage rosters mid-tournament, and per-tournament ruleset differences). When editing team/trophy/roster data in `esportsData.js` or `primary_data/official_teams_and_rosters.json`, cross-check against Liquipedia/official sources rather than assuming the existing pipeline output is authoritative — several interim reports (`26`, `27`) exist specifically to correct earlier verification mistakes.
