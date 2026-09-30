import React, { useCallback } from 'react';
import { Flame, Mouse, Eye } from 'lucide-react';
import { fetchHotPlayers } from '../../api/hot';
import { useApi } from '../../hooks/useApi';
import LoadingPanel from '../common/LoadingPanel';
import ErrorPanel from '../common/ErrorPanel';

const EMPTY = [];
const NOT_SET = '미등록';

/**
 * HOT 탭. 이번 주 조회수가 많은 선수 순으로 보여준다.
 *
 * **선수 데이터를 따로 들고 있지 않는다.** 백엔드가 자연키(리그+팀+닉네임)로
 * players 를 찾아 감도·마우스·소속을 채워 준다. 예전에는 12명의 세팅을
 * esportsData.js 에 따로 적어 뒀는데 그 값이 실제와 전부 달랐다
 * (seoul 이 800/32 로 적혀 있었으나 실제는 1600/30).
 *
 * 조회수가 아직 쌓이지 않았으면 세계대회 성적으로 정한 초기 순위가 대신 나온다.
 */
export default function HotPlayerGrid({ searchQuery = '', onSelectPlayer }) {
  const fetcher = useCallback(() => fetchHotPlayers(12), []);
  const { data: hot, loading, error, reload } = useApi(fetcher, [], EMPTY);

  if (loading) {
    return <LoadingPanel title="HOT 선수를 불러오는 중입니다" detail="조회수를 집계하고 있습니다." />;
  }

  if (error) {
    return (
      <ErrorPanel
        title="HOT 선수를 불러오지 못했습니다"
        message={error}
        hint="백엔드 서버(localhost:8080)와 PostgreSQL 컨테이너가 실행 중인지 확인해 주세요."
        onRetry={reload}
      />
    );
  }

  const q = searchQuery.toLowerCase();
  const players = (hot ?? []).filter(p =>
    p.nickname?.toLowerCase().includes(q) ||
    p.realName?.toLowerCase().includes(q) ||
    p.team?.toLowerCase().includes(q)
  );

  const anyViews = (hot ?? []).some(p => p.viewCount > 0);

  return (
    <div>
      <div className="glass-panel" style={{
        padding: '16px 20px',
        borderRadius: 'var(--radius-sm)',
        marginBottom: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        flexWrap: 'wrap',
        border: '1px solid rgba(243, 166, 31, 0.25)',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(22, 26, 38, 0.9) 100%)'
      }}>
        <Flame size={20} color="var(--accent-gold)" />
        <span style={{ fontWeight: '900', color: '#fff', fontSize: '1.05rem' }}>
          HOT STAR PLAYERS (TOP 12)
        </span>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          {anyViews ? '이번 주 조회수 순' : '아직 조회 기록이 없어 세계대회 성적 순으로 보여줍니다'}
        </span>
      </div>

      {players.length === 0 ? (
        <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center' }}>
          <Flame size={36} color="var(--accent-gold)" style={{ margin: '0 auto 16px auto' }} />
          <h3 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>
            아직 보여줄 선수가 없습니다
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            선수를 눌러 보면 조회수가 쌓이고 여기에 나타납니다.
          </p>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: '20px'
        }}>
          {players.map((player, idx) => (
            <div
              key={player.id}
              onClick={() => onSelectPlayer && onSelectPlayer(player)}
              className="glass-panel"
              style={{
                padding: '20px',
                borderRadius: 'var(--radius-md)',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                border: '1px solid var(--border-subtle)',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: '16px'
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
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {player.teamLogo ? (
                      <img
                        src={player.teamLogo}
                        alt={player.team}
                        style={{ width: '46px', height: '46px', objectFit: 'contain' }}
                      />
                    ) : (
                      <div style={{
                        width: '46px',
                        height: '46px',
                        borderRadius: '50%',
                        background: 'rgba(243, 166, 31, 0.12)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: '900',
                        fontSize: '1.1rem',
                        color: 'var(--accent-gold)'
                      }}>
                        {player.nickname?.[0] || 'P'}
                      </div>
                    )}
                    <div>
                      <div style={{ fontSize: '1.15rem', fontWeight: '900', color: '#fff' }}>
                        {player.nickname}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {player.league} • {player.country}
                      </div>
                    </div>
                  </div>
                  <span className="badge badge-gold" style={{ fontSize: '0.7rem' }}>
                    HOT #{idx + 1}
                  </span>
                </div>

                <div style={{
                  padding: '8px 12px',
                  borderRadius: 'var(--radius-sm)',
                  background: 'rgba(255, 255, 255, 0.02)',
                  marginBottom: '14px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '0.82rem'
                }}>
                  <span style={{ color: 'var(--text-muted)' }}>Team</span>
                  <span style={{ color: '#fff', fontWeight: '700' }}>{player.team}</span>
                </div>

                <div style={{ padding: '8px 10px', background: 'rgba(0,0,0,0.2)', borderRadius: '4px', fontSize: '0.8rem' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>DPI / 일반 감도</div>
                  <div style={{
                    color: (player.dpi === null && player.sens === null) ? 'var(--text-muted)' : 'var(--accent-cyan)',
                    fontWeight: '800'
                  }}>
                    {(player.dpi === null && player.sens === null)
                      ? NOT_SET
                      : `${player.dpi ?? '?'} / ${player.sens ?? '?'}`}
                  </div>
                </div>
              </div>

              <div style={{
                borderTop: '1px solid rgba(255, 255, 255, 0.06)',
                paddingTop: '12px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontSize: '0.78rem'
              }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-muted)' }}>
                  <Mouse size={14} />
                  {player.mouse ?? NOT_SET}
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '5px', color: 'var(--text-muted)' }}>
                  <Eye size={14} />
                  {player.viewCount}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
