-- PUBG PRO VAULT 초기 스키마
--
-- 2026-09-29 까지는 spring.jpa.hibernate.ddl-auto: create 가 기동마다 스키마를
-- 통째로 다시 만들었다. 재기동할 때마다 데이터가 전멸해서 HOT 탭 조회수처럼
-- 런타임에 쌓이는 값을 담을 수 없었다.
--
-- 이 파일은 그때 Hibernate 가 만들던 스키마를 그대로 옮겨 적은 것이다.
-- 앞으로 스키마 변경은 V2, V3... 로 추가한다. 이 파일은 고치지 않는다.

CREATE TABLE player_gears (
    id bigint NOT NULL,
    player_id bigint NOT NULL,
    brand character varying(255),
    category character varying(255) NOT NULL,
    image_url character varying(255),
    name character varying(255) NOT NULL,
    purchase_link character varying(255)
);

CREATE SEQUENCE player_gears_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE player_gears_id_seq OWNED BY player_gears.id;

CREATE TABLE player_highlights (
    id bigint NOT NULL,
    player_id bigint NOT NULL,
    title character varying(255) NOT NULL,
    tournament character varying(255),
    video_url character varying(255) NOT NULL
);

CREATE SEQUENCE player_highlights_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE player_highlights_id_seq OWNED BY player_highlights.id;

CREATE TABLE player_settings (
    ads_sens double precision,
    aiming_sens double precision,
    fov integer,
    general_sens double precision,
    mouse_dpi integer,
    render_scale integer,
    scope2x_sens double precision,
    scope3x_sens double precision,
    scope4x_sens double precision,
    scope6x_sens double precision,
    vertical_multiplier double precision,
    id bigint NOT NULL,
    player_id bigint NOT NULL,
    resolution character varying(255),
    screen_mode character varying(255)
);

CREATE SEQUENCE player_settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE player_settings_id_seq OWNED BY player_settings.id;

CREATE TABLE players (
    is_active boolean NOT NULL,
    id bigint NOT NULL,
    last_crawled_at timestamp(6) without time zone,
    team_id bigint,
    chzzk_url character varying(255),
    country character varying(255),
    nickname character varying(255) NOT NULL,
    profile_image_url character varying(255),
    real_name character varying(255),
    role character varying(255),
    soop_url character varying(255),
    youtube_url character varying(255)
);

CREATE SEQUENCE players_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE players_id_seq OWNED BY players.id;

CREATE TABLE teams (
    founded_year integer,
    id bigint NOT NULL,
    achievements character varying(1000),
    description character varying(1000),
    coach character varying(255),
    league character varying(255),
    logo_url character varying(255),
    name character varying(255) NOT NULL,
    region character varying(255) NOT NULL,
    seed_type character varying(255),
    tag character varying(255)
);

CREATE SEQUENCE teams_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE teams_id_seq OWNED BY teams.id;

CREATE TABLE tournament_player_stats (
    assists integer,
    damage double precision,
    headshot_rate double precision,
    kills integer,
    knocks integer,
    rank integer,
    survival_time_avg double precision,
    twire_rating double precision,
    id bigint NOT NULL,
    player_id bigint NOT NULL,
    tournament_id bigint NOT NULL
);

CREATE SEQUENCE tournament_player_stats_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tournament_player_stats_id_seq OWNED BY tournament_player_stats.id;

CREATE TABLE tournament_team_results (
    kill_points integer,
    matches_played integer,
    placement_points integer,
    rank integer,
    total_points integer,
    wwcd_count integer,
    id bigint NOT NULL,
    team_id bigint NOT NULL,
    tournament_id bigint NOT NULL,
    prize character varying(255)
);

CREATE SEQUENCE tournament_team_results_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tournament_team_results_id_seq OWNED BY tournament_team_results.id;

CREATE TABLE tournaments (
    end_date date,
    start_date date,
    id bigint NOT NULL,
    location character varying(255),
    logo_url character varying(255),
    name character varying(255) NOT NULL,
    prize_pool character varying(255),
    region character varying(255),
    slug character varying(255),
    status character varying(255),
    tier character varying(255),
    CONSTRAINT tournaments_status_check CHECK (((status)::text = ANY ((ARRAY['UPCOMING'::character varying, 'ONGOING'::character varying, 'COMPLETED'::character varying])::text[])))
);

CREATE SEQUENCE tournaments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tournaments_id_seq OWNED BY tournaments.id;

ALTER TABLE ONLY player_gears ALTER COLUMN id SET DEFAULT nextval('player_gears_id_seq'::regclass);

ALTER TABLE ONLY player_highlights ALTER COLUMN id SET DEFAULT nextval('player_highlights_id_seq'::regclass);

ALTER TABLE ONLY player_settings ALTER COLUMN id SET DEFAULT nextval('player_settings_id_seq'::regclass);

ALTER TABLE ONLY players ALTER COLUMN id SET DEFAULT nextval('players_id_seq'::regclass);

ALTER TABLE ONLY teams ALTER COLUMN id SET DEFAULT nextval('teams_id_seq'::regclass);

ALTER TABLE ONLY tournament_player_stats ALTER COLUMN id SET DEFAULT nextval('tournament_player_stats_id_seq'::regclass);

ALTER TABLE ONLY tournament_team_results ALTER COLUMN id SET DEFAULT nextval('tournament_team_results_id_seq'::regclass);

ALTER TABLE ONLY tournaments ALTER COLUMN id SET DEFAULT nextval('tournaments_id_seq'::regclass);

ALTER TABLE ONLY player_gears
    ADD CONSTRAINT player_gears_pkey PRIMARY KEY (id);

ALTER TABLE ONLY player_highlights
    ADD CONSTRAINT player_highlights_pkey PRIMARY KEY (id);

ALTER TABLE ONLY player_settings
    ADD CONSTRAINT player_settings_pkey PRIMARY KEY (id);

ALTER TABLE ONLY player_settings
    ADD CONSTRAINT player_settings_player_id_key UNIQUE (player_id);

ALTER TABLE ONLY players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);

ALTER TABLE ONLY teams
    ADD CONSTRAINT teams_name_key UNIQUE (name);

ALTER TABLE ONLY teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);

ALTER TABLE ONLY tournament_player_stats
    ADD CONSTRAINT tournament_player_stats_pkey PRIMARY KEY (id);

ALTER TABLE ONLY tournament_team_results
    ADD CONSTRAINT tournament_team_results_pkey PRIMARY KEY (id);

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_name_key UNIQUE (name);

ALTER TABLE ONLY tournaments
    ADD CONSTRAINT tournaments_pkey PRIMARY KEY (id);

ALTER TABLE ONLY players
    ADD CONSTRAINT fk5nglidr00c4dyybl171v6kask FOREIGN KEY (team_id) REFERENCES teams(id);

ALTER TABLE ONLY player_settings
    ADD CONSTRAINT fkcdpad8bawu9ys8u1k5dnmfeir FOREIGN KEY (player_id) REFERENCES players(id);

ALTER TABLE ONLY tournament_player_stats
    ADD CONSTRAINT fke1k8wr3mcfh4s4cbhjjghnhtu FOREIGN KEY (tournament_id) REFERENCES tournaments(id);

ALTER TABLE ONLY tournament_team_results
    ADD CONSTRAINT fkfgddf40qcqf1e32xyw2m8nrgf FOREIGN KEY (tournament_id) REFERENCES tournaments(id);

ALTER TABLE ONLY tournament_player_stats
    ADD CONSTRAINT fkgjwv8tsnu275bdu350jyxsbf2 FOREIGN KEY (player_id) REFERENCES players(id);

ALTER TABLE ONLY tournament_team_results
    ADD CONSTRAINT fkiarxt4227xj2tylu03xliimhj FOREIGN KEY (team_id) REFERENCES teams(id);

ALTER TABLE ONLY player_gears
    ADD CONSTRAINT fkqtlm3o3ee7ijrme6tq3hfo5q0 FOREIGN KEY (player_id) REFERENCES players(id);
