-- HOT 탭: 선수 조회수와 초기 순위.
--
-- 두 테이블 모두 **선수를 자연키(리그+팀+닉네임)로 가리킨다.** players.id 를 쓰면
-- SEED_MODE=always 재적재 때 id 가 새로 부여돼 조회수가 엉뚱한 선수에게 붙는다
-- (실제로 T1 이 3 -> 204 로 바뀌는 것을 확인했다).
--
-- 선수 정보 자체는 여기 두지 않는다. 화면에 필요한 감도·장비·소속은 조회 시점에
-- players 를 조인해 가져온다. 예전 HOT_PLAYERS_12 는 12명의 세팅을 따로 적어 뒀고
-- 그 값이 실제와 전부 달랐다 (seoul 800/32 로 적혀 있었으나 실제는 1600/30).

-- 기간별 조회수. period 는 ISO 주차(2026-W40). 기간이 바뀌면 새 행이 쌓이므로
-- 초기화 스케줄러가 필요 없고 지난 주 기록도 남는다.
CREATE TABLE player_views (
    id bigserial PRIMARY KEY,
    league varchar(20) NOT NULL,
    team_name varchar(255) NOT NULL,
    nickname varchar(255) NOT NULL,
    period varchar(10) NOT NULL,
    view_count bigint NOT NULL DEFAULT 0,
    updated_at timestamp(6),
    CONSTRAINT uk_player_views UNIQUE (league, team_name, nickname, period)
);

CREATE INDEX idx_player_views_period ON player_views (period, view_count DESC);

-- 조회수가 쌓이기 전에 HOT 탭을 채우는 초기 12명. 세계대회 성적 기준이며
-- 어느 대회에서 온 순위인지 source 에 남긴다. 조회수가 쌓이면 자연히 밀려난다.
CREATE TABLE hot_seeds (
    id bigserial PRIMARY KEY,
    league varchar(20) NOT NULL,
    team_name varchar(255) NOT NULL,
    nickname varchar(255) NOT NULL,
    seed_rank int NOT NULL,
    source varchar(500),
    note varchar(500),
    CONSTRAINT uk_hot_seeds UNIQUE (league, team_name, nickname)
);
