import React from 'react';

/**
 * 팀 카드 1개. 리그와 무관하게 TeamCardDto 형태만 받는다.
 * 선수를 클릭하면 팀 문맥(팀명·리그·지역)을 합쳐 상위로 올린다.
 */
export default function TeamCard({ team, onSelectPlayer }) {
  return (
    <div
      className="glass-panel"
      style={{
        padding: '20px',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-subtle)',
        display: 'flex',
        flexDirection: 'column',
        gap: '16px',
        transition: 'all 0.2s ease',
        background: 'rgba(22, 26, 38, 0.75)'
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = 'var(--border-active)';
        e.currentTarget.style.transform = 'translateY(-2px)';
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = 'var(--border-subtle)';
        e.currentTarget.style.transform = 'translateY(0)';
      }}
    >
      {/* 팀 헤더: 공식 로고 + 팀명 + 태그 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '54px',
          height: '54px',
          borderRadius: '10px',
          background: 'rgba(255, 255, 255, 0.04)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'hidden',
          flexShrink: 0,
          padding: '4px'
        }}>
          {team.logo ? (
            <img
              src={team.logo}
              alt={team.name}
              style={{ width: '100%', height: '100%', objectFit: 'contain' }}
              onError={(e) => {
                e.target.style.display = 'none';
                const fb = e.target.nextElementSibling;
                if (fb) fb.style.display = 'flex';
              }}
            />
          ) : null}
          {/* 로고가 없거나 로드 실패하면 태그를 보여준다 */}
          <div style={{
            display: team.logo ? 'none' : 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '100%',
            height: '100%',
            fontWeight: '900',
            fontSize: '1rem',
            color: 'var(--accent-gold)'
          }}>
            {team.tag}
          </div>
        </div>

        <div style={{ overflow: 'hidden', flex: 1 }}>
          <div style={{
            fontSize: '1.15rem',
            fontWeight: '900',
            color: '#fff',
            letterSpacing: '0.02em',
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis'
          }}>
            {team.name}
          </div>
          {team.tag && (
            <div style={{
              fontSize: '0.78rem',
              color: 'var(--text-muted)',
              fontWeight: '700',
              letterSpacing: '0.05em',
              marginTop: '3px'
            }}>
              {team.tag}
            </div>
          )}
        </div>
      </div>

      {/* 공식 로스터 */}
      <div style={{
        borderTop: '1px solid rgba(255, 255, 255, 0.06)',
        paddingTop: '14px'
      }}>
        <div style={{
          fontSize: '0.72rem',
          color: 'var(--text-muted)',
          marginBottom: '8px',
          fontWeight: '800',
          textTransform: 'uppercase',
          letterSpacing: '0.05em'
        }}>
          Official Roster
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
          {(team.roster ?? []).map((player) => (
            <div
              key={player.id ?? player.nickname}
              onClick={() => onSelectPlayer && onSelectPlayer({
                ...player,
                team: team.name,
                league: team.league,
                country: team.region,
                dpi: player.dpi,
                generalSens: player.sens,
                mouseName: player.mouse
              })}
              style={{
                padding: '8px 10px',
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(255, 255, 255, 0.03)',
                border: '1px solid rgba(255, 255, 255, 0.05)',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(243, 166, 31, 0.12)'}
              onMouseLeave={e => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: '800', color: '#fff', fontSize: '0.88rem' }}>
                  {player.nickname}
                </span>
                {/* 실측 DPI 가 있는 선수만 표시한다. 없는 값을 지어내지 않는다. */}
                {player.dpi != null && (
                  <span style={{ fontSize: '0.7rem', color: 'var(--accent-gold)' }}>
                    {player.dpi}DPI
                  </span>
                )}
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                {player.role}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
