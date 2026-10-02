import React, { useCallback, useEffect, useState } from 'react';
import { Trophy, Globe, Shield, Swords, Crosshair, Map as MapIcon, Route } from 'lucide-react';
import { fetchTournaments, fetchTournament, fetchMatchIds, fetchMatchLog } from '../api/tournaments';
import { useApi } from '../hooks/useApi';
import LoadingPanel from './common/LoadingPanel';
import ErrorPanel from './common/ErrorPanel';
import PlayerStatsTable from './tournaments/PlayerStatsTable';
import MatchLogMap from './tournaments/MatchLogMap';

const EMPTY = [];

// wwcd.lol 과 같은 3분류다 (사용자 지시).
const CATEGORIES = [
  { id: 'global', label: 'GLOBAL', desc: '글로벌 대회', icon: Globe },
  { id: 'regional', label: 'REGIONAL', desc: '지역 리그', icon: Shield },
  { id: 'scrim', label: 'SCRIM', desc: '연습 경기', icon: Swords }
];

// 분류 안에서 시리즈를 한 번 더 고른다. 글로벌은 대회 시리즈, 지역은 권역이다.
// 데이터가 아직 없는 시리즈도 칸을 보여줘 "무엇이 비어 있는지" 드러나게 한다.
const SERIES = {
  global: ['PGS', 'PNC', 'EWC', 'PGC'],
  regional: ['PWS', 'PCL', 'EMEA', 'AMER', 'PTS', 'PVS'],
  scrim: []
};

const SERIES_NOTE = {
  EWC: 'EWC 2026 은 공식 API 의 참가자 이름이 전원 익명 처리돼 있어 선수와 팀을 알 수 없습니다.',
  PGC: 'PGC 2026 은 아직 열리지 않았습니다. PGC 는 매년 12월에 열립니다.'
};

const MAP_NAMES = {
  Baltic_Main: 'Erangel', Desert_Main: 'Miramar', Savage_Main: 'Sanhok',
  DihorOtok_Main: 'Vikendi', Tiger_Main: 'Taego', Neon_Main: 'Rondo',
  Kiki_Main: 'Deston', Chimera_Main: 'Paramo', Summerland_Main: 'Karakin',
  Heaven_Main: 'Haven'
};

const VIEWS = [
  { id: 'leaderboard', label: '리더보드', icon: Trophy },
  { id: 'players', label: '플레이어 스탯', icon: Crosshair },
  { id: 'matchlog', label: '매치로그', icon: Route }
];

/**
 * 대회 탭.
 *
 *   분류(글로벌·지역·스크림) -> 시리즈(PGS·PWS 등) -> 대회 -> 리더보드 / 플레이어 스탯 / 매치로그
 *
 * 데이터는 공식 PUBG API 에서 받아 정리한 primary_data/tournaments/*.json 과
 * primary_data/matchlogs/ 다 (ingest/fetch_tournament.ps1 + build_tournament_seed.py
 * + build_match_log.py).
 */
/**
 * 한 시리즈의 대회들을 (연도 -> 회차) 로 묶는다.
 *
 * 공식 API 의 대회 id 하나는 **대회가 아니라 단계**다. PGS 7 은 네 개 — 조별
 * (gsg) · ws · ss · 결승(fsg) — 로 나뉘어 있다. 그래서 회차로 다시 묶어
 * "PGS 7" 한 칸 안에서 단계를 고르게 한다.
 */
function groupByYear(list) {
  const years = new Map();
  for (const t of list) {
    const y = t.year ?? 0;
    if (!years.has(y)) years.set(y, new Map());
    // 회차가 없는 시리즈(PGC 2019 처럼)는 연도 자체가 한 대회다.
    const key = t.edition ? `${t.series} ${t.edition}` : `${t.series} ${y}`;
    const events = years.get(y);
    if (!events.has(key)) events.set(key, []);
    events.get(key).push(t);
  }
  for (const events of years.values()) {
    for (const stages of events.values()) {
      stages.sort((a, b) => (a.startDate ?? '').localeCompare(b.startDate ?? ''));
    }
  }
  return years;
}

/** 단계 칩에 쓸 이름. 이름을 모르면 날짜로 구별한다 — 지어내지 않는다. */
function stageLabel(t) {
  if (t.stage) return t.stage;
  if (t.stageCode) return t.stageCode.toUpperCase();
  return t.startDate ? t.startDate.slice(5).replace('-', '/') : t.id;
}

export default function TournamentsTab() {
  const [category, setCategory] = useState('global');
  const [series, setSeries] = useState('PGS');
  const [year, setYear] = useState(null);
  const [eventKey, setEventKey] = useState(null);
  const [stageId, setStageId] = useState(null);

  const listFetcher = useCallback(() => fetchTournaments(category), [category]);
  const { data: list, loading, error, reload } = useApi(listFetcher, [category], EMPTY);

  const inSeries = (list ?? []).filter(t => t.series === series);
  const byYear = groupByYear(inSeries);
  const years = [...byYear.keys()].sort((a, b) => b - a);
  const activeYear = years.includes(year) ? year : years[0];
  const events = byYear.get(activeYear) ?? new Map();
  const eventKeys = [...events.keys()];
  const activeEvent = eventKeys.includes(eventKey) ? eventKey : eventKeys[0];
  const stages = events.get(activeEvent) ?? [];
  const activeStage = stages.some(t => t.id === stageId) ? stageId : stages[0]?.id;

  useEffect(() => { setSeries(SERIES[category]?.[0] ?? null); }, [category]);
  useEffect(() => { setYear(null); setEventKey(null); setStageId(null); }, [series]);
  useEffect(() => { setEventKey(null); setStageId(null); }, [activeYear]);
  useEffect(() => { setStageId(null); }, [activeEvent]);

  if (loading) {
    return <LoadingPanel title="대회 목록을 불러오는 중입니다" detail="백엔드 서버에서 가져오고 있습니다." />;
  }
  if (error) {
    return (
      <ErrorPanel
        title="대회 목록을 불러오지 못했습니다"
        message={error}
        hint="백엔드 서버(localhost:8080)와 PostgreSQL 컨테이너가 실행 중인지 확인해 주세요."
        onRetry={reload}
      />
    );
  }

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      <ChipRow>
        {CATEGORIES.map(c => (
          <Chip key={c.id} active={category === c.id} onClick={() => setCategory(c.id)}
                icon={c.icon} label={c.label} sub={c.desc} big />
        ))}
      </ChipRow>

      {SERIES[category].length > 0 && (
        <ChipRow>
          {SERIES[category].map(s => {
            const count = (list ?? []).filter(t => t.series === s).length;
            return (
              <Chip key={s} active={series === s} onClick={() => setSeries(s)}
                    label={s} sub={count > 0 ? `${count}` : '없음'} dim={count === 0} />
            );
          })}
        </ChipRow>
      )}

      {category === 'scrim' ? (
        <EmptyPanel
          title="아직 등록된 대회가 없습니다"
          reason="스크림은 비공식 연습 경기라 공식 PUBG API 대회 목록에 올라오지 않습니다."
        />
      ) : inSeries.length === 0 ? (
        <EmptyPanel
          title={`${series} 대회가 아직 없습니다`}
          reason={SERIES_NOTE[series] ?? '이 시리즈의 경기 기록이 아직 수집되지 않았습니다.'}
        />
      ) : (
        <>
          <ChipRow>
            {years.map(y => (
              <Chip key={y} active={activeYear === y} onClick={() => setYear(y)}
                    label={y ? `${y}` : '연도 미상'}
                    sub={`${byYear.get(y).size}`} />
            ))}
          </ChipRow>

          <ChipRow>
            {eventKeys.map(k => (
              <Chip key={k} active={activeEvent === k} onClick={() => setEventKey(k)}
                    label={k}
                    sub={events.get(k).length > 1 ? `${events.get(k).length}단계` : null}
                    subtle />
            ))}
          </ChipRow>

          {activeStage && (
            <TournamentDetail
              id={activeStage}
              stages={stages}
              onStage={setStageId}
              stageLabel={stageLabel}
            />
          )}
        </>
      )}
    </div>
  );
}

function TournamentDetail({ id, stages, onStage, stageLabel }) {
  const [view, setView] = useState('leaderboard');
  const fetcher = useCallback(() => fetchTournament(id), [id]);
  const { data, loading, error, reload } = useApi(fetcher, [id], null);

  useEffect(() => { setView('leaderboard'); }, [id]);

  // 단계가 둘 이상일 때만 고를 줄을 낸다. 리더보드는 단계별로 봐야 맞다 —
  // 조별예선과 결승은 참가 팀도 경기 수도 달라 합치면 뜻이 없다.
  const stageRow = stages && stages.length > 1 ? (
    <ChipRow>
      {stages.map(t => (
        <Chip key={t.id} active={t.id === id} onClick={() => onStage(t.id)}
              label={stageLabel(t)} sub={`${t.matchCount}경기`} />
      ))}
    </ChipRow>
  ) : null;

  if (loading) {
    return (<>{stageRow}
      <LoadingPanel title="대회 기록을 불러오는 중입니다" detail="순위표와 선수 기록을 가져오고 있습니다." />
    </>);
  }
  if (error) {
    return (<>{stageRow}
      <ErrorPanel title="대회 기록을 불러오지 못했습니다" message={error} onRetry={reload} />
    </>);
  }
  if (!data) return null;

  const maps = (data.maps ?? []).map(m => MAP_NAMES[m] ?? m);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {stageRow}
      <div className="glass-panel" style={{
        padding: '18px 22px',
        borderRadius: 'var(--radius-sm)',
        border: '1px solid rgba(243, 166, 31, 0.3)',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.1) 0%, rgba(22, 26, 38, 0.95) 100%)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Trophy size={20} color="var(--accent-gold)" />
            <span style={{ fontWeight: '900', color: '#fff', fontSize: '1.1rem' }}>{data.name}</span>
            {data.startDate && (
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{data.startDate}</span>
            )}
          </div>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <span className="badge badge-gold" style={{ fontSize: '0.75rem', fontWeight: '800' }}>
              {data.matchCount} MATCHES
            </span>
            <span className="badge" style={{ fontSize: '0.75rem', fontWeight: '800', background: 'rgba(255,255,255,0.08)', color: '#fff' }}>
              {data.standings?.length ?? 0} TEAMS
            </span>
          </div>
        </div>
        {maps.length > 0 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '12px', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            <MapIcon size={14} />
            {maps.join(' · ')}
          </div>
        )}
      </div>

      <ChipRow>
        {VIEWS.map(v => (
          <Chip
            key={v.id}
            active={view === v.id}
            onClick={() => setView(v.id)}
            icon={v.icon}
            label={v.label}
          />
        ))}
      </ChipRow>

      {view === 'leaderboard' && <Standings rows={data.standings ?? []} />}
      {view === 'players' && <PlayerStatsTable rows={data.players ?? []} />}
      {view === 'matchlog' && <MatchLogView tournamentId={id} />}

      <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0, lineHeight: 1.6 }}>
        {view === 'leaderboard' && data.note ? data.note + ' ' : ''}
        출처:{' '}
        <a href={data.source} target="_blank" rel="noopener noreferrer"
           style={{ color: 'var(--text-muted)', textDecoration: 'underline' }}>
          PUBG 공식 API
        </a>
        {view === 'matchlog' && ' · 맵 이미지: PUBG 공식 api-assets'}
      </p>
    </div>
  );
}

function MatchLogView({ tournamentId }) {
  const idsFetcher = useCallback(() => fetchMatchIds(tournamentId), [tournamentId]);
  const { data: ids, loading, error, reload } = useApi(idsFetcher, [tournamentId], EMPTY);
  const [matchId, setMatchId] = useState(null);

  useEffect(() => { setMatchId((ids ?? [])[0] ?? null); }, [ids]);

  const logFetcher = useCallback(
    () => (matchId ? fetchMatchLog(tournamentId, matchId) : Promise.resolve(null)),
    [tournamentId, matchId]);
  const { data: log, loading: logLoading } = useApi(logFetcher, [tournamentId, matchId], null);

  if (loading) return <LoadingPanel title="경기 목록을 불러오는 중입니다" detail="" />;
  if (error) return <ErrorPanel title="경기 목록을 불러오지 못했습니다" message={error} onRetry={reload} />;

  if ((ids ?? []).length === 0) {
    return (
      <EmptyPanel
        title="매치로그가 아직 없습니다"
        reason="이 대회는 텔레메트리에서 이동 경로를 아직 추출하지 않았습니다. ingest/build_match_log.py 로 만들 수 있습니다."
      />
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <ChipRow>
        {ids.map((id, i) => (
          <Chip
            key={id}
            active={matchId === id}
            onClick={() => setMatchId(id)}
            label={`${i + 1}경기`}
            subtle
          />
        ))}
      </ChipRow>
      {logLoading ? <LoadingPanel title="매치로그를 불러오는 중입니다" detail="이동 경로와 자기장을 그립니다." />
        : <MatchLogMap log={log} />}
    </div>
  );
}

function Standings({ rows }) {
  if (rows.length === 0) return null;

  // 사용자가 지정한 열 순서다. 순위점수·킬점수는 화면에서 "순위"·"킬" 로 줄여 쓴다.
  const COLS = [
    { key: 'matches', label: '경기' },
    { key: 'wwcd', label: '치킨', gold: true },
    { key: 'placementPoints', label: '순위' },
    { key: 'killPoints', label: '킬' },
    { key: 'avgPoints', label: '평균' },
    { key: 'totalPoints', label: '합계', strong: true }
  ];
  const GRID = `48px 1fr repeat(${COLS.length}, 64px)`;

  return (
    <div className="glass-panel" style={{ borderRadius: 'var(--radius-sm)', overflowX: 'auto' }}>
      <div style={{ minWidth: '640px' }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: GRID,
          padding: '10px 16px',
          background: 'rgba(255,255,255,0.03)',
          fontSize: '0.73rem',
          color: 'var(--text-muted)',
          fontWeight: '800',
          textTransform: 'uppercase'
        }}>
          <span>#</span>
          <span>팀</span>
          {COLS.map(c => (
            <span key={c.key} style={{ textAlign: 'right' }}>{c.label}</span>
          ))}
        </div>

        {rows.map(r => (
          <div key={r.team} style={{
            display: 'grid',
            gridTemplateColumns: GRID,
            padding: '11px 16px',
            borderTop: '1px solid rgba(255,255,255,0.04)',
            alignItems: 'center',
            fontSize: '0.86rem',
            background: r.rank <= 3 ? 'rgba(243, 166, 31, 0.05)' : 'transparent'
          }}>
            <span style={{ fontWeight: '900', color: r.rank <= 3 ? 'var(--accent-gold)' : 'var(--text-muted)' }}>
              {r.rank}
            </span>
            <span style={{ color: '#fff', fontWeight: '700' }}>
              {r.team}
              {!r.teamResolved && (
                <span title="우리 선수 명단에서 팀을 찾지 못해 인게임 아이디 접두사를 씁니다"
                      style={{ marginLeft: '6px', fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                  (태그)
                </span>
              )}
              {r.league && (
                <span style={{ marginLeft: '8px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                  {r.league}
                </span>
              )}
            </span>
            {COLS.map(c => {
              const v = r[c.key];
              const empty = v === null || v === undefined;
              return (
                <span key={c.key} style={{
                  textAlign: 'right',
                  color: empty ? 'var(--text-muted)'
                    : c.strong ? 'var(--accent-gold)'
                    : (c.gold && v > 0) ? 'var(--accent-gold)'
                    : '#fff',
                  fontWeight: c.strong ? '900' : (c.gold && v > 0) ? '800' : '600'
                }}>
                  {empty ? '-' : (c.key === 'avgPoints' ? v.toFixed(1) : v)}
                </span>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

function ChipRow({ children }) {
  return (
    <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '18px' }}>
      {children}
    </div>
  );
}

function Chip({ active, onClick, icon: Icon, label, sub, big, subtle, dim }) {
  return (
    <button
      onClick={dim ? undefined : onClick}
      disabled={dim}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: big ? '10px 18px' : '8px 15px',
        borderRadius: 'var(--radius-sm)',
        background: active
          ? (subtle ? 'rgba(243, 166, 31, 0.15)' : 'var(--accent-gold)')
          : 'rgba(255, 255, 255, 0.04)',
        color: active ? (subtle ? 'var(--accent-gold)' : '#000') : 'var(--text-muted)',
        border: `1px solid ${active ? (subtle ? 'rgba(243,166,31,0.5)' : 'var(--accent-gold)') : 'var(--border-subtle)'}`,
        fontWeight: '900',
        fontSize: big ? '0.88rem' : '0.84rem',
        cursor: dim ? 'not-allowed' : 'pointer',
        opacity: dim ? 0.4 : 1,
        transition: 'all 0.2s ease'
      }}
    >
      {Icon && <Icon size={15} color={active && !subtle ? '#000' : 'var(--accent-gold)'} />}
      <span>{label}</span>
      {sub && (
        <span style={{ fontWeight: '600', fontSize: '0.76rem', opacity: 0.75 }}>{sub}</span>
      )}
    </button>
  );
}

function EmptyPanel({ title, reason }) {
  return (
    <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center' }}>
      <Trophy size={36} color="var(--accent-gold)" style={{ margin: '0 auto 16px auto' }} />
      <h3 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>{title}</h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>{reason}</p>
    </div>
  );
}
