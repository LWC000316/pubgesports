import React, { useCallback } from 'react';
import { Crown, Target, Shield, Users } from 'lucide-react';
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
 *
 * seedLabels 는 두 시드 그룹의 화면 제목이다. 리그마다 본선 진입 경로의 근거가
 * 달라서(PWS 는 위키가 Pro/Amateur Seed 라고 명시, EMEA·AMER 은 파트너팀 제도,
 * PVS 는 직전 페이즈 성적) 같은 seedType 에 같은 이름을 붙이면 사실과 어긋난다.
 * null 을 넘기면 구분 근거가 없는 리그로 보고 단일 목록으로 그린다(PTS).
 */
export default function LeagueTeamGrid({ league, searchQuery = '', bannerLogo, bannerTitle, sourceUrl, seedLabels, onSelectPlayer }) {
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

  // seedLabels 가 없는 리그는 위키에 시드 구분 근거가 없다는 뜻이라 나누지 않는다.
  const groups = seedLabels
    ? [
        {
          key: 'pro',
          title: seedLabels.pro,
          teams: filtered.filter(t => t.seedType === 'pro'),
          icon: <Crown size={20} color="var(--accent-gold)" />,
          borderColor: 'rgba(243, 166, 31, 0.3)',
          highlight: true
        },
        {
          key: 'amateur',
          title: seedLabels.amateur,
          teams: filtered.filter(t => t.seedType === 'amateur'),
          icon: <Target size={20} color="#00e5ff" />,
          borderColor: 'rgba(255, 255, 255, 0.15)',
          highlight: false
        }
      ]
    : [
        {
          key: 'all',
          title: 'Participants',
          teams: filtered,
          icon: <Users size={20} color="var(--accent-gold)" />,
          borderColor: 'rgba(243, 166, 31, 0.3)',
          highlight: true
        }
      ];

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
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {groups.map(g => (
              <span
                key={g.key}
                className={g.highlight ? 'badge badge-gold' : 'badge'}
                style={g.highlight
                  ? { fontSize: '0.75rem', fontWeight: '800' }
                  : { fontSize: '0.75rem', fontWeight: '800', background: 'rgba(255,255,255,0.08)', color: '#fff' }}
              >
                {g.teams.length} {g.title.toUpperCase()}
              </span>
            ))}
          </div>
        </div>
      )}

      {groups.map(g => (
        <SeedSection
          key={g.key}
          title={`${g.title} (${g.teams.length})`}
          icon={g.icon}
          borderColor={g.borderColor}
          teams={g.teams}
          onSelectPlayer={onSelectPlayer}
        />
      ))}

      <SourceAttribution sourceUrl={sourceUrl} />
    </div>
  );
}

/**
 * 리퀴피디아 콘텐츠는 CC-BY-SA 3.0 이라 화면에 출처를 밝혀야 한다.
 * sourceUrl 이 있으면 대조에 쓴 대회 문서로, 없으면 위키 첫 화면으로 연결한다.
 */
function SourceAttribution({ sourceUrl }) {
  const linkStyle = { color: 'var(--text-muted)', textDecoration: 'underline' };
  return (
    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textAlign: 'right', margin: 0 }}>
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
