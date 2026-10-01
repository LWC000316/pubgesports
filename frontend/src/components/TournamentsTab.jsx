import React, { useCallback, useEffect, useState } from 'react';
import { Trophy, Globe, Shield, Swords, Crosshair, Map as MapIcon } from 'lucide-react';
import { fetchTournaments, fetchTournament } from '../api/tournaments';
import { useApi } from '../hooks/useApi';
import LoadingPanel from './common/LoadingPanel';
import ErrorPanel from './common/ErrorPanel';

const EMPTY = [];
const NOT_SET = '미등록';

// wwcd.lol 과 같은 3분류다 (사용자 지시).
const CATEGORIES = [
  { id: 'global', label: 'GLOBAL', desc: '글로벌 대회', icon: Globe },
  { id: 'regional', label: 'REGIONAL', desc: '지역 리그', icon: Shield },
  { id: 'scrim', label: 'SCRIM', desc: '연습 경기', icon: Swords }
];

const MAP_NAMES = {
  Baltic_Main: 'Erangel',
  Desert_Main: 'Miramar',
  Savage_Main: 'Sanhok',
  DihorOtok_Main: 'Vikendi',
  Tiger_Main: 'Taego',
  Neon_Main: 'Rondo',
  Kiki_Main: 'Deston',
  Chimera_Main: 'Paramo'
};

/**
 * 대회 탭. 글로벌 · 지역리그 · 스크림 3분류로 나누고 대회를 고르면
 * 순위표와 선수 기록을 보여준다.
 *
 * 데이터는 공식 PUBG API 에서 받아 정리한 primary_data/tournaments/*.json 이다
 * (ingest/fetch_tournament.ps1 + build_tournament_seed.py).
 *
 * **순위 점수는 없다.** 대회 규정마다 달라 계산하지 않았다 — API 가 직접 주는
 * 값(경기 수·킬·WWCD·평균 순위)만 보여준다. 점수를 지어내지 않는다.
 */
export default function TournamentsTab() {
  const [category, setCategory] = useState('global');
  const [selectedId, setSelectedId] = useState(null);

  const listFetcher = useCallback(() => fetchTournaments(category), [category]);
  const { data: list, loading, error, reload } = useApi(listFetcher, [category], EMPTY);

  // 분류를 바꾸면 그 분류의 첫 대회를 고른다.
  useEffect(() => {
    const first = (list ?? [])[0];
    setSelectedId(first ? first.id : null);
  }, [list]);

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
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '24px' }}>
        {CATEGORIES.map(c => {
          const isActive = category === c.id;
          const Icon = c.icon;
          return (
            <button
              key={c.id}
              onClick={() => setCategory(c.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 18px',
                borderRadius: 'var(--radius-sm)',
                background: isActive ? 'var(--accent-gold)' : 'rgba(255, 255, 255, 0.04)',
                color: isActive ? '#000' : 'var(--text-muted)',
                border: isActive ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                fontWeight: '900',
                fontSize: '0.88rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon size={16} color={isActive ? '#000' : 'var(--accent-gold)'} />
              <span>{c.label}</span>
              <span style={{ fontWeight: '600', fontSize: '0.78rem', opacity: 0.75 }}>
                {c.desc}
              </span>
            </button>
          );
        })}
      </div>

      {(list ?? []).length === 0 ? (
        <EmptyCategory category={category} />
      ) : (
        <>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '24px' }}>
            {list.map(t => {
              const isActive = selectedId === t.id;
              return (
                <button
                  key={t.id}
                  onClick={() => setSelectedId(t.id)}
                  style={{
                    padding: '9px 16px',
                    borderRadius: 'var(--radius-sm)',
                    background: isActive ? 'rgba(243, 166, 31, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                    color: isActive ? 'var(--accent-gold)' : 'var(--text-muted)',
                    border: `1px solid ${isActive ? 'rgba(243, 166, 31, 0.5)' : 'var(--border-subtle)'}`,
                    fontWeight: '800',
                    fontSize: '0.84rem',
                    cursor: 'pointer'
                  }}
                >
                  {t.name}
                </button>
              );
            })}
          </div>

          {selectedId && <TournamentDetail id={selectedId} />}
        </>
      )}
    </div>
  );
}

function EmptyCategory({ category }) {
  // 지어낸 데이터로 채우지 않는다. 왜 비어 있는지 밝힌다.
  const reason = {
    global: '글로벌 대회 기록이 아직 수집되지 않았습니다.',
    regional: '지역 리그 기록이 아직 수집되지 않았습니다.',
    scrim: '스크림은 비공식 연습 경기라 공식 PUBG API 대회 목록에 올라오지 않습니다.'
  }[category];

  return (
    <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center' }}>
      <Trophy size={36} color="var(--accent-gold)" style={{ margin: '0 auto 16px auto' }} />
      <h3 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>
        아직 등록된 대회가 없습니다
      </h3>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>{reason}</p>
    </div>
  );
}

function TournamentDetail({ id }) {
  const fetcher = useCallback(() => fetchTournament(id), [id]);
  const { data, loading, error, reload } = useApi(fetcher, [id], null);

  if (loading) {
    return <LoadingPanel title="대회 기록을 불러오는 중입니다" detail="순위표와 선수 기록을 가져오고 있습니다." />;
  }
  if (error) {
    return (
      <ErrorPanel
        title="대회 기록을 불러오지 못했습니다"
        message={error}
        hint="백엔드 서버가 실행 중인지 확인해 주세요."
        onRetry={reload}
      />
    );
  }
  if (!data) return null;

  const maps = (data.maps ?? []).map(m => MAP_NAMES[m] ?? m);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
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

      <Standings rows={data.standings ?? []} />
      <PlayerStats rows={data.players ?? []} />

      <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0, lineHeight: 1.6 }}>
        {data.note}
        {data.source && (
          <>
            {' '}출처:{' '}
            <a href={data.source} target="_blank" rel="noopener noreferrer"
               style={{ color: 'var(--text-muted)', textDecoration: 'underline' }}>
              PUBG 공식 API
            </a>
          </>
        )}
      </p>
    </div>
  );
}

function Standings({ rows }) {
  if (rows.length === 0) return null;
  return (
    <div>
      <SectionTitle icon={<Trophy size={18} color="var(--accent-gold)" />} text={`순위표 (${rows.length}팀)`} />
      <div className="glass-panel" style={{ borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
        <HeaderRow cols={['#', '팀', '경기', '치킨', '킬', '최고', '평균']} />
        {rows.map(r => (
          <div key={r.team} style={{
            display: 'grid',
            gridTemplateColumns: '48px 1fr 60px 60px 60px 60px 70px',
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
            <Cell value={r.matches} />
            <Cell value={r.wwcd} highlight={r.wwcd > 0} />
            <Cell value={r.kills} />
            <Cell value={r.bestRank} />
            <Cell value={r.avgRank} />
          </div>
        ))}
      </div>
    </div>
  );
}

function PlayerStats({ rows }) {
  const [expanded, setExpanded] = useState(false);
  if (rows.length === 0) return null;
  const shown = expanded ? rows : rows.slice(0, 15);

  return (
    <div>
      <SectionTitle icon={<Crosshair size={18} color="var(--accent-cyan)" />} text={`선수 기록 (${rows.length}명)`} />
      <div className="glass-panel" style={{ borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
        <HeaderRow cols={['#', '선수', '팀', '경기', '킬', '데미지']} grid="48px 1fr 1fr 60px 60px 90px" />
        {shown.map((p, i) => (
          <div key={`${p.nickname}-${p.team}`} style={{
            display: 'grid',
            gridTemplateColumns: '48px 1fr 1fr 60px 60px 90px',
            padding: '11px 16px',
            borderTop: '1px solid rgba(255,255,255,0.04)',
            alignItems: 'center',
            fontSize: '0.86rem'
          }}>
            <span style={{ fontWeight: '900', color: i < 3 ? 'var(--accent-cyan)' : 'var(--text-muted)' }}>
              {i + 1}
            </span>
            <span style={{ color: '#fff', fontWeight: '700' }}>{p.nickname}</span>
            <span style={{ color: 'var(--text-muted)' }}>{p.team ?? NOT_SET}</span>
            <Cell value={p.matches} />
            <Cell value={p.kills} highlight />
            <Cell value={Math.round(p.damage)} />
          </div>
        ))}
      </div>
      {rows.length > 15 && (
        <button
          onClick={() => setExpanded(v => !v)}
          style={{
            marginTop: '10px',
            padding: '8px 16px',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-muted)',
            fontSize: '0.8rem',
            fontWeight: '700',
            cursor: 'pointer'
          }}
        >
          {expanded ? '접기' : `전체 ${rows.length}명 보기`}
        </button>
      )}
    </div>
  );
}

function SectionTitle({ icon, text }) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      marginBottom: '12px',
      paddingBottom: '8px',
      borderBottom: '1px solid rgba(255,255,255,0.08)'
    }}>
      {icon}
      <h2 style={{
        fontSize: '1.05rem',
        fontWeight: '900',
        color: '#fff',
        margin: 0,
        letterSpacing: '0.04em',
        textTransform: 'uppercase'
      }}>
        {text}
      </h2>
    </div>
  );
}

function HeaderRow({ cols, grid = '48px 1fr 60px 60px 60px 60px 70px' }) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: grid,
      padding: '10px 16px',
      background: 'rgba(255,255,255,0.03)',
      fontSize: '0.74rem',
      color: 'var(--text-muted)',
      fontWeight: '800',
      textTransform: 'uppercase',
      letterSpacing: '0.04em'
    }}>
      {cols.map((c, i) => (
        <span key={c} style={{ textAlign: i >= 2 ? 'right' : 'left' }}>{c}</span>
      ))}
    </div>
  );
}

function Cell({ value, highlight = false }) {
  const missing = value === null || value === undefined;
  return (
    <span style={{
      textAlign: 'right',
      color: missing ? 'var(--text-muted)' : (highlight ? 'var(--accent-gold)' : '#fff'),
      fontWeight: highlight ? '800' : '600'
    }}>
      {missing ? '-' : value}
    </span>
  );
}
