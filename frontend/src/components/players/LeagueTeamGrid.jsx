import React, { useCallback, useEffect, useState } from 'react';
import { Shield } from 'lucide-react';
import { fetchTeamCards } from '../../api/teams';
import { fetchLeagueSources } from '../../api/leagues';
import { useApi } from '../../hooks/useApi';
import LoadingPanel from '../common/LoadingPanel';
import ErrorPanel from '../common/ErrorPanel';
import TeamCard from './TeamCard';

const EMPTY = [];

// 수집 출처는 리그를 바꿔도 안 변하므로 한 번만 받아 둔다.
// 실패해도 팀 목록은 그대로 보여야 하므로 에러를 삼킨다.
let sourcesPromise = null;
function loadSources() {
  if (!sourcesPromise) {
    sourcesPromise = fetchLeagueSources().catch(() => []);
  }
  return sourcesPromise;
}

// 목록 순서. 프로로 볼 수 있는 구단을 앞에, 그 뒤로 아마추어 구단을 잇는다.
// 구획을 나누지 않고 한 줄기로 늘어놓는다 — 리그마다 "프로"의 근거가 달라서
// 구획 제목을 붙이면 어느 리그에서는 반드시 사실과 어긋난다.
const SEED_ORDER = { pro: 0, amateur: 1 };

/**
 * 리그 하나의 팀 목록. 여섯 리그가 모두 이 컴포넌트를 쓴다.
 * 리그를 추가할 때는 league prop 만 바꿔서 렌더하면 된다.
 *
 * bannerTitle 은 대회 공식 명칭처럼 리그별로 다른 문구가 있을 때만 넘긴다.
 */
export default function LeagueTeamGrid({ league, searchQuery = '', bannerLogo, bannerTitle, sourceUrl, onSelectPlayer }) {
  const fetcher = useCallback(() => fetchTeamCards(league), [league]);
  const { data: teams, loading, error, reload } = useApi(fetcher, [league], EMPTY);

  const [sources, setSources] = useState(EMPTY);
  useEffect(() => { loadSources().then(setSources); }, []);
  const source = sources.find(s => s.league?.toUpperCase() === league.toUpperCase());

  if (loading) {
    return (
      <LoadingPanel
        title="공식 로스터를 불러오는 중입니다"
        detail={`백엔드 서버에서 ${league} 팀 데이터를 가져오고 있습니다.`}
      />
    );
  }

  if (error) {
    return (
      <ErrorPanel
        title="팀 데이터를 불러오지 못했습니다"
        message={error}
        hint="백엔드 서버(localhost:8080)와 PostgreSQL 컨테이너가 실행 중인지 확인해 주세요."
        onRetry={reload}
      />
    );
  }

  // API 응답에는 누락 필드가 있을 수 있어 옵셔널 체이닝 필수
  const q = searchQuery.toLowerCase();
  const filtered = (teams ?? []).filter(t => {
    const matchesTeam = t.name?.toLowerCase().includes(q) || t.tag?.toLowerCase().includes(q);
    const matchesRoster = t.roster?.some(p => p.nickname?.toLowerCase().includes(q));
    return matchesTeam || matchesRoster;
  });

  // Array.prototype.sort 는 안정 정렬이라 같은 seedType 안에서는 API 순서가 유지된다.
  const ordered = [...filtered].sort(
    (a, b) => (SEED_ORDER[a.seedType] ?? 9) - (SEED_ORDER[b.seedType] ?? 9)
  );

  if ((teams ?? []).length === 0) {
    return (
      <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center' }}>
        <Shield size={36} color="var(--accent-gold)" style={{ margin: '0 auto 16px auto' }} />
        <h3 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>
          {league} 등록된 팀이 없습니다
        </h3>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          검증된 {league} 참가 명단이 아직 DB에 적재되지 않았습니다.
        </p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
      {bannerTitle && (
        <div className="glass-panel" style={{
          padding: '16px 22px',
          borderRadius: 'var(--radius-sm)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px',
          border: '1px solid rgba(243, 166, 31, 0.3)',
          background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.1) 0%, rgba(22, 26, 38, 0.95) 100%)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            {bannerLogo && (
              <img src={bannerLogo} alt={league} style={{ width: '28px', height: '28px', objectFit: 'contain' }} />
            )}
            <span style={{ fontWeight: '900', color: '#fff', fontSize: '1.1rem', letterSpacing: '0.02em' }}>
              {bannerTitle}
            </span>
          </div>
          <span className="badge badge-gold" style={{ fontSize: '0.75rem', fontWeight: '800' }}>
            {ordered.length} TEAMS
          </span>
        </div>
      )}

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
        gap: '20px'
      }}>
        {ordered.map(team => (
          <TeamCard key={team.id} team={team} onSelectPlayer={onSelectPlayer} />
        ))}
      </div>

      <SourceAttribution sourceUrl={sourceUrl} source={source} />
    </div>
  );
}

/**
 * 리퀴피디아 콘텐츠는 CC-BY-SA 3.0 이라 화면에 출처를 밝혀야 한다.
 * sourceUrl 이 있으면 대조에 쓴 대회 문서로, 없으면 위키 첫 화면으로 연결한다.
 */
function SourceAttribution({ sourceUrl, source }) {
  const linkStyle = { color: 'var(--text-muted)', textDecoration: 'underline' };
  // 대회가 아직 진행 중이면 명단이 더 바뀔 수 있다는 것을 밝힌다.
  const ongoing = source?.tournamentEnd
    && source.tournamentEnd > new Date().toISOString().slice(0, 10);
  return (
    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textAlign: 'right', margin: 0 }}>
      {source?.collectedAt && (
        <>
          <strong style={{ color: 'var(--text-muted)' }}>{source.collectedAt} 기준</strong>
          {ongoing && ` · 대회 진행 중 (${source.tournamentEnd} 종료 예정)`}
          {' · '}
        </>
      )}
      팀·로스터 정보 출처:{' '}
      <a href={sourceUrl || 'https://liquipedia.net/pubg'} target="_blank" rel="noopener noreferrer" style={linkStyle}>
        Liquipedia
      </a>
      {' '}(
      <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noopener noreferrer" style={linkStyle}>
        CC BY-SA 3.0
      </a>
      )
    </p>
  );
}
