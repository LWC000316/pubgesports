import React, { useCallback, useEffect, useState } from 'react';
import { Trophy, Globe, Shield, Swords, Crosshair, Map as MapIcon, Route, AlertTriangle } from 'lucide-react';
import { fetchTournaments, fetchTournament, fetchMatchList, fetchMatchLog } from '../api/tournaments';
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
  // 2019~2020년 대회는 에란겔의 내부 이름이 Erangel_Main 이었다 (15개 단계).
  // 지금은 Baltic_Main 이다. 같은 맵이라 화면에는 똑같이 Erangel 로 쓴다.
  Erangel_Main: 'Erangel',
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
 *   분류(글로벌·지역·스크림) -> 시리즈 -> 연도 -> 대회(회차) -> 단계
 *     -> 리더보드 / 플레이어 스탯 / 매치로그
 *
 * 데이터는 공식 PUBG API 에서 받아 정리한 primary_data/tournaments/*.json 과
 * primary_data/matchlogs/ 다 (ingest/ 의 fetch_all.ps1 + build_all.py +
 * build_match_logs_all.py).
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
    // 공식 이름(리퀴피디아 문서 제목)이 있으면 그것으로 묶고 보여준다.
    // 없을 때만 id 에서 뽑은 시리즈·회차로 대신한다.
    const key = t.officialName
      ? t.officialName.split('/').slice(1).join(' ')
      : (t.edition ? `${t.series} ${t.edition}` : `${t.series} ${y}`);
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
  // 대회는 **고르기 전까지 아무것도 펼치지 않는다.** 칩 다섯 줄이 한 번에 쌓여
  // 지저분하던 것을 고친 것이라, 기본으로 하나를 열어 두면 도로 그 꼴이 된다.
  const activeEvent = eventKeys.includes(eventKey) ? eventKey : null;
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

  const seriesCount = code => (list ?? []).filter(t => t.series === code).length;

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      {/* 1단 분류 — 가장 큰 결정이라 밑줄 탭으로. 아래와 모양이 달라야 위계가 생긴다 */}
      <SegmentTabs items={CATEGORIES} active={category} onChange={setCategory} />

      {/* 2단 시리즈 — 타일. 단계 수를 적어 데이터가 어디 있는지 한눈에 */}
      {SERIES[category].length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(104px, 1fr))',
          gap: '8px', marginBottom: '20px'
        }}>
          {SERIES[category].map(code => (
            <SeriesTile key={code} code={code} count={seriesCount(code)}
                        active={series === code} onClick={() => setSeries(code)} />
          ))}
        </div>
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
          {/* 3단 연도 — 얇은 막대 하나. 2018~2026 이 다 차도 한 줄을 넘지 않는다 */}
          <YearBar years={years} active={activeYear} counts={byYear} onChange={setYear} />

          {/* 4단 대회 — 칩이 아니라 카드. 실제로 고르는 곳이라 규모를 먼저 보여준다 */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(230px, 1fr))',
            gap: '10px', marginBottom: activeEvent ? '24px' : 0
          }}>
            {eventKeys.map(k => (
              <EventCard key={k} name={k} stages={events.get(k)}
                         active={activeEvent === k}
                         onClick={() => setEventKey(activeEvent === k ? null : k)} />
            ))}
          </div>

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

/** 분류 — 밑줄 탭. 아래 단계도 칩으로 두면 무엇이 상위인지 구별이 안 된다. */
function SegmentTabs({ items, active, onChange }) {
  return (
    <div style={{
      display: 'flex', gap: '4px', marginBottom: '20px',
      borderBottom: '1px solid var(--border-subtle)', overflowX: 'auto'
    }}>
      {items.map(({ id, label, desc, icon: Icon }) => {
        const on = active === id;
        return (
          <button key={id} onClick={() => onChange(id)} style={{
            display: 'flex', alignItems: 'center', gap: '8px',
            padding: '12px 18px', background: 'none', border: 'none',
            borderBottom: `2px solid ${on ? 'var(--accent-gold)' : 'transparent'}`,
            marginBottom: '-1px', cursor: 'pointer', whiteSpace: 'nowrap',
            color: on ? '#fff' : 'var(--text-muted)',
            fontWeight: on ? '900' : '700', fontSize: '0.95rem'
          }}>
            {Icon && <Icon size={17} color={on ? 'var(--accent-gold)' : 'currentColor'} />}
            {label}
            <span style={{ fontSize: '0.8rem', fontWeight: '600', opacity: 0.7 }}>{desc}</span>
          </button>
        );
      })}
    </div>
  );
}

/** 시리즈 — 타일. 단계 수를 적어 "어디에 데이터가 있나"가 먼저 보이게 한다. */
function SeriesTile({ code, count, active, onClick }) {
  const empty = count === 0;
  return (
    <button onClick={empty ? undefined : onClick} disabled={empty} style={{
      display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: '2px',
      padding: '12px 14px', borderRadius: 'var(--radius-sm)', textAlign: 'left',
      background: active ? 'rgba(243,166,31,0.13)' : 'rgba(255,255,255,0.03)',
      border: `1px solid ${active ? 'var(--accent-gold)' : 'var(--border-subtle)'}`,
      cursor: empty ? 'default' : 'pointer', opacity: empty ? 0.35 : 1,
      transition: 'all .15s ease'
    }}>
      <span style={{
        fontSize: '1.05rem', fontWeight: '900', letterSpacing: '0.02em',
        color: active ? 'var(--accent-gold)' : '#fff'
      }}>{code}</span>
      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
        {empty ? '없음' : `단계 ${count}`}
      </span>
    </button>
  );
}

/** 연도 — 한 줄짜리 막대. 칩을 또 쓰면 시리즈와 구별이 안 된다. */
function YearBar({ years, active, counts, onChange }) {
  return (
    <div style={{
      display: 'inline-flex', gap: '2px', marginBottom: '16px', padding: '3px',
      borderRadius: 'var(--radius-sm)', maxWidth: '100%', overflowX: 'auto',
      background: 'rgba(255,255,255,0.03)', border: '1px solid var(--border-subtle)'
    }}>
      {years.map(y => {
        const on = active === y;
        return (
          <button key={y} onClick={() => onChange(y)} style={{
            padding: '7px 18px', border: 'none',
            borderRadius: 'calc(var(--radius-sm) - 2px)',
            background: on ? 'var(--accent-gold)' : 'transparent',
            color: on ? '#000' : 'var(--text-muted)',
            fontWeight: on ? '900' : '700', fontSize: '0.85rem',
            cursor: 'pointer', whiteSpace: 'nowrap'
          }}>
            {y || '연도 미상'}
            <span style={{ marginLeft: '6px', fontSize: '0.74rem', opacity: 0.6 }}>
              {counts.get(y).size}
            </span>
          </button>
        );
      })}
    </div>
  );
}

/** 대회 — 카드. 고르기 전에 규모(단계·경기·기간)를 알 수 있어야 한다. */
function EventCard({ name, stages, active, onClick }) {
  const matches = stages.reduce((n, t) => n + (t.matchCount || 0), 0);
  const from = stages[0]?.startDate;
  // 마지막 단계의 **끝나는 날**이 대회가 끝난 날이다. 시작일을 쓰면 마지막
  // 단계가 여러 날에 걸친 만큼 기간이 짧게 나온다.
  const last = stages[stages.length - 1];
  const to = last?.endDate ?? last?.startDate;
  const short = d => (d ? d.slice(5).replace('-', '/') : '');
  const span = from && to && from !== to ? `${short(from)} ~ ${short(to)}` : short(from);
  return (
    <button onClick={onClick} style={{
      display: 'flex', flexDirection: 'column', gap: '8px',
      padding: '14px 16px', borderRadius: 'var(--radius-sm)', textAlign: 'left',
      background: active
        ? 'linear-gradient(135deg, rgba(243,166,31,0.16) 0%, rgba(22,26,38,0.95) 100%)'
        : 'rgba(255,255,255,0.03)',
      border: `1px solid ${active ? 'var(--accent-gold)' : 'var(--border-subtle)'}`,
      cursor: 'pointer', transition: 'all .15s ease'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Trophy size={15} color={active ? 'var(--accent-gold)' : 'var(--text-muted)'} />
        <span style={{ fontWeight: '900', color: '#fff', fontSize: '0.98rem' }}>{name}</span>
      </div>
      {span && <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>{span}</div>}
      <div style={{ display: 'flex', gap: '12px', fontSize: '0.76rem', color: 'var(--text-muted)' }}>
        <span>단계 <b style={{ color: '#fff' }}>{stages.length}</b></span>
        <span>경기 <b style={{ color: '#fff' }}>{matches}</b></span>
      </div>
    </button>
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
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                {data.endDate && data.endDate !== data.startDate
                  ? `${data.startDate} ~ ${data.endDate.slice(5)}` : data.startDate}
              </span>
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

      {view === 'leaderboard' && (
        <Standings rows={data.standings ?? []} matchesPerTeam={data.matchesPerTeam} />
      )}
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
  const listFetcher = useCallback(() => fetchMatchList(tournamentId), [tournamentId]);
  const { data: matches, loading, error, reload } = useApi(listFetcher, [tournamentId], EMPTY);
  const [matchId, setMatchId] = useState(null);

  useEffect(() => { setMatchId((matches ?? [])[0]?.id ?? null); }, [matches]);

  const logFetcher = useCallback(
    () => (matchId ? fetchMatchLog(tournamentId, matchId) : Promise.resolve(null)),
    [tournamentId, matchId]);
  const { data: log, loading: logLoading } = useApi(logFetcher, [tournamentId, matchId], null);

  if (loading) return <LoadingPanel title="경기 목록을 불러오는 중입니다" detail="" />;
  if (error) return <ErrorPanel title="경기 목록을 불러오지 못했습니다" message={error} onRetry={reload} />;

  if ((matches ?? []).length === 0) {
    return (
      <EmptyPanel
        title="매치로그가 아직 없습니다"
        reason="이 대회는 텔레메트리에서 이동 경로를 아직 추출하지 않았습니다. ingest/build_match_log.py 로 만들 수 있습니다."
      />
    );
  }

  // 경기 번호는 **시작 시각을 알 때만** 붙인다. 파일 이름이 UUID 라 순서를 모르는
  // 단계에서 1,2,3 을 매기면 그 번호가 거짓이 된다 — 그럴 땐 맵 이름으로 고른다.
  const ordered = matches.every(m => m.startedAt);
  const current = matches.find(m => m.id === matchId);
  const currentNo = ordered && current ? matches.indexOf(current) + 1 : null;

  // 날짜별로 접어 둔다. 15경기가 한 줄로 늘어서면 어느 날 경기인지 안 보인다.
  const days = [];
  matches.forEach((m, i) => {
    const d = m.startedAt ? m.startedAt.slice(0, 10) : '';
    if (!days.length || days[days.length - 1].day !== d) days.push({ day: d, rows: [] });
    days[days.length - 1].rows.push({ ...m, no: i + 1 });
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {days.map(({ day, rows }) => (
          <div key={day || 'x'} style={{ display: 'flex', alignItems: 'center',
                                         gap: '8px', flexWrap: 'wrap' }}>
            {day && (
              <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)',
                             fontWeight: 900, minWidth: '46px' }}>
                {day.slice(5).replace('-', '/')}
              </span>
            )}
            {rows.map(m => (
              <Chip
                key={m.id}
                active={matchId === m.id}
                onClick={() => setMatchId(m.id)}
                label={ordered ? `${m.no}경기` : (m.map ?? '경기')}
                sub={ordered ? m.map : undefined}
                subtle
              />
            ))}
          </div>
        ))}
      </div>
      {current && <MatchHeadline match={current} />}
      {logLoading ? <LoadingPanel title="매치로그를 불러오는 중입니다" detail="이동 경로와 자기장을 그립니다." />
        : <MatchLogMap log={log} title={currentNo ? `매치 ${currentNo}` : undefined} />}
    </div>
  );
}

/** 고른 경기의 한 줄 요약. 값이 없는 것은 아예 빼고, 빈칸을 지어내지 않는다. */
function MatchHeadline({ match }) {
  const bits = [];
  if (match.startedAt) {
    bits.push(new Date(match.startedAt).toLocaleString('ko-KR', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit'
    }));
  }
  if (match.map) bits.push(match.map);
  if (match.duration) bits.push(`${Math.round(match.duration / 60)}분`);
  if (match.kills) bits.push(`킬 ${match.kills}`);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap',
                  fontSize: '0.84rem', color: 'var(--text-muted)' }}>
      <span>{bits.join(' · ')}</span>
      {match.winner && (
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px',
                       color: 'var(--accent-gold)', fontWeight: '900' }}>
          <Trophy size={14} /> {match.winner}
        </span>
      )}
    </div>
  );
}

function Standings({ rows, matchesPerTeam }) {
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
    <div>
      {/* 팀마다 뛴 경기 수가 다르면 합계로 줄 세우는 것이 공정하지 않다.
          여러 로비로 나뉘었거나 중간 탈락이 있는 단계다. 숨기지 않고 알린다. */}
      {matchesPerTeam && (
        <div style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          padding: '10px 14px', marginBottom: '10px',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(243, 166, 31, 0.08)',
          border: '1px solid rgba(243, 166, 31, 0.25)',
          fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5
        }}>
          <AlertTriangle size={15} color="var(--accent-gold)" style={{ flexShrink: 0 }} />
          <span>
            이 단계는 팀마다 뛴 경기 수가 다릅니다 (
            <b style={{ color: '#fff' }}>{matchesPerTeam.min}~{matchesPerTeam.max}경기</b>
            ). 합계 점수는 많이 뛴 팀이 유리하므로 순위를 그대로 결과로 읽지 마세요.
          </span>
        </div>
      )}
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
