# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PUBG PRO VAULT — a full-stack archive of PUBG (PLAYERUNKNOWN'S BATTLEGROUNDS) eSports player profiles/gear/settings plus tournament leaderboards, built as a Spring Boot REST API + React SPA, backed by data pulled from the official Krafton PUBG API and various scraped/Liquipedia sources.

## Tech stack

- **Backend**: Java 17, Spring Boot 3.2.3 (Web, Data JPA), PostgreSQL 16, Jsoup 1.17.2, Lombok. Gradle build.
- **Frontend**: React 18, Vite 5, lucide-react, vanilla CSS (no CSS framework, no state library).
- **Infra**: Docker Compose (PostgreSQL only — the app itself runs on the host).
- **Data tooling**: standalone Python scripts under `scripts/` (see the data pipeline section below).

## Commands

### Database (required before running the backend)
```
docker compose up -d
```
Starts PostgreSQL 16 on port 5432 (db `pubg_esports`, user `pubg_user`). Credentials live in `docker-compose.yml` and `backend/src/main/resources/application.yml`.

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

Backend must be running for the frontend to show live data; `frontend/src/data/mockData.js` is a fallback used when the API is unreachable.

## Architecture

### Backend: `backend/src/main/java/com/pubg/esports/`
Standard layered Spring Boot app:
- `domain/` — JPA entities: `Team` 1—N `Player` 1—1 `PlayerSetting`, 1—N `PlayerGear`, 1—N `PlayerHighlight`; `Tournament` 1—N `TournamentTeamResult` / `TournamentPlayerStat`.
- `repository/` — Spring Data JPA repos.
- `service/` — business logic, including `CrawlerService` (Jsoup-based scraping of ProSettings/wiki pages, run on a `@Scheduled(cron = "0 0 4 * * ?")` daily job) and `PubgOfficialApiService` (calls the official Krafton PUBG API at `pubg.api.base-url`, filters tournaments by keyword to PWS/PCL/PGS/PGC/PNC/EWC, with an in-memory cache to respect the 10 RPM rate limit).
- `controller/` — `PlayerController`, `TournamentController`, `PubgTournamentController`, `CrawlerController`, `AdminController` (CRUD for teams/players used by an admin flow).
- `config/DataInitializer.java` — on every startup, wipes and reloads the DB from `primary_data/official_teams_and_rosters.json` (looked up relative to the working directory, with a `../` fallback — run `bootRun` from `backend/` or the repo root accordingly).

**`spring.jpa.hibernate.ddl-auto` is `create`**, so the schema (and all data) is dropped and rebuilt from `DataInitializer` on every backend restart. Don't expect data to persist across restarts, and don't rely on manually-inserted rows surviving a redeploy.

**Repository query gotcha**: `PlayerRepository` deliberately exposes separate `findAllWithTeam` / `findByTeamIdWithTeam` / `searchByQueryWithTeam` / `searchByTeamIdAndQueryWithTeam` query methods instead of one query with optional/nullable JPQL parameters. This is because PostgreSQL's driver infers a `bytea` type for `null`-bound parameters, which breaks `LOWER(?)` with a "function lower(bytea) does not exist" error. `PlayerService.getPlayers` explicitly branches on whether `teamId`/`query` are present and calls the matching method — follow this pattern (explicit branching, not nullable JPQL params) for any new filtered queries.

### Frontend: `frontend/src/`
- `App.jsx` — top-level tab state machine with three tabs: `pe` (players, `PlayersTab.jsx`), `tournaments` (`TournamentsTab.jsx`, which also renders `TeamRosterView.jsx`), and `hit_ending` (`HitEndingTab.jsx`, a sensitivity/FOV-style calculator).
- `components/PlayerDetailModal.jsx` — per-player popup (settings/eDPI, gear rack, highlight video, stream links).
- `data/esportsData.js` — large hand/script-maintained static dataset (team rosters, logos, trophies) used directly by the tournament/roster views, independent of the backend API. `data/mockData.js` is the separate fallback used when the backend is offline.
- Vite dev server proxies `/api/*` to `http://localhost:8080` (see `vite.config.js`); it does not proxy in `vite preview`/production builds.

### Data pipeline (`scripts/`, `primary_data/`, `secondary_data/`, `intermediate_results/`)
This repo also contains an ad hoc, numbered pipeline of one-off Python scripts (`scripts/01_...py` through `scripts/69_...py`) used to source and reconcile tournament/team/roster data from the official PUBG API, Liquipedia, Twire, and the pubgesports.com Nuxt site (including reverse-engineering its JS chunks/Supabase client). Each script's output JSON typically lands in `primary_data/`, `secondary_data/`, or `intermediate_results/`, and later scripts progressively filter/merge/verify that data before it is hand-applied into `frontend/src/data/esportsData.js` and `primary_data/official_teams_and_rosters.json` (the latter is what `DataInitializer` seeds the DB from). Scripts are numbered in the order they were run and are not a reusable CLI — treat them as an audit trail of how the current dataset was derived, not as a pipeline to invoke end-to-end. `interim_reports/*.md` contains a dated write-up for most numbered stages/features, useful for understanding *why* a given data decision or fix was made.

## Code conventions

Observed consistently in the existing backend code — follow these when adding to it:
- Constructor injection via Lombok `@RequiredArgsConstructor` with `final` fields; no `@Autowired` on fields.
- Read-only services are annotated `@Transactional(readOnly = true)` at class level (`PlayerService`, `TournamentService`).
- Entity→DTO conversion goes through a static `from()` factory on the DTO (`PlayerListResponseDto.from`, `TeamResponseDto.from`), not a mapper class.
- Logging via Lombok `@Slf4j`. Log messages, exception messages, and the `message` field of admin API responses are written in Korean.

## Notes for changes touching data accuracy
Tournament/roster data correctness has been an ongoing, carefully-verified effort (see `interim_reports/20_automated_esports_data_sync_pipeline_evaluation.md` for known limitations: nickname→team-tag parsing ambiguity, team rebrands not reflected in the official API, incomplete group-stage rosters mid-tournament, and per-tournament ruleset differences). When editing team/trophy/roster data in `esportsData.js` or `primary_data/official_teams_and_rosters.json`, cross-check against Liquipedia/official sources rather than assuming the existing pipeline output is authoritative — several interim reports (`26`, `27`) exist specifically to correct earlier verification mistakes.
