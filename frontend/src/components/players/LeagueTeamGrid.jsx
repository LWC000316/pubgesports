import React, { useCallback } from 'react';
import { Crown, Target, Shield } from 'lucide-react';
import { fetchTeamCards } from '../../api/teams';
import { useApi } from '../../hooks/useApi';
import LoadingPanel from '../common/LoadingPanel';
import ErrorPanel from '../common/ErrorPanel';
import TeamCard from './TeamCard';

const EMPTY = [];

/**
 * 리그 하나의 팀 목록. PWS·PCL·EMEA·AMER·APAC 이 모두 이 컴포넌트를 쓴다.
 * 리그를 추가할 때는 league prop 만 바꿔서 렌더하면 된다.
 *
 * bannerTitle 은 대회 공식 명칭처럼 리그별로 다른 문구가 있을 때만 넘긴다.
 */
export default function LeagueTeamGrid({ league, searchQuery = '', bannerLogo, bannerTitle, onSelectPlayer }) {
  const fetcher = useCallback(() => fetchTeamCards(league), [league]);
  const { data: teams, loading, error, reload } = useApi(fetcher, [league], EMPTY);

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

  const proTeams = filtered.filter(t => t.seedType === 'pro');
  const qualifierTeams = filtered.filter(t => t.seedType === 'amateur');

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
    <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
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
          <div style={{ display: 'flex', gap: '8px' }}>
            <span className="badge badge-gold" style={{ fontSize: '0.75rem', fontWeight: '800' }}>
              {proTeams.length} PRO SEEDS
            </span>
            <span className="badge" style={{ fontSize: '0.75rem', fontWeight: '800', background: 'rgba(255,255,255,0.08)', color: '#fff' }}>
              {qualifierTeams.length} QUALIFIER SEEDS
            </span>
          </div>
        </div>
      )}

      <SeedSection
        title={`Pro Seeds (${proTeams.length})`}
        icon={<Crown size={20} color="var(--accent-gold)" />}
        borderColor="rgba(243, 166, 31, 0.3)"
        teams={proTeams}
        onSelectPlayer={onSelectPlayer}
      />

      <SeedSection
        title={`Qualifier Seeds (${qualifierTeams.length})`}
        icon={<Target size={20} color="#00e5ff" />}
        borderColor="rgba(255, 255, 255, 0.15)"
        teams={qualifierTeams}
        onSelectPlayer={onSelectPlayer}
      />
    </div>
  );
}

function SeedSection({ title, icon, borderColor, teams, onSelectPlayer }) {
  if (teams.length === 0) return null;

  return (
    <div>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        marginBottom: '16px',
        paddingBottom: '8px',
        borderBottom: `1px solid ${borderColor}`
      }}>
        {icon}
        <h2 style={{
          fontSize: '1.1rem',
          fontWeight: '900',
          color: '#fff',
          margin: 0,
          letterSpacing: '0.05em',
          textTransform: 'uppercase'
        }}>
          {title}
        </h2>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
        gap: '20px'
      }}>
        {teams.map(team => (
          <TeamCard key={team.id} team={team} onSelectPlayer={onSelectPlayer} />
        ))}
      </div>
    </div>
  );
}
