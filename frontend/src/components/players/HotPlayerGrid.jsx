import React from 'react';
import { Flame, Mouse, ChevronRight } from 'lucide-react';
import { HOT_PLAYERS_12 } from '../../data/esportsData';

/**
 * HOT 탭. 아직 백엔드와 연결되지 않은 정적 데이터를 쓴다.
 * 조회수 기반 집계로 교체할 예정이며, 그때는 조회 기록을 영속 저장해야 한다
 * (현재 ddl-auto: create 는 재기동마다 DB 를 지운다).
 */
export default function HotPlayerGrid({ searchQuery = '', onSelectPlayer }) {
  const q = searchQuery.toLowerCase();
  const players = HOT_PLAYERS_12.filter(p =>
    p.nickname?.toLowerCase().includes(q) ||
    p.realName?.includes(q) ||
    p.team?.toLowerCase().includes(q)
  );

  return (
    <div>
      <div className="glass-panel" style={{
        padding: '16px 20px',
        borderRadius: 'var(--radius-sm)',
        marginBottom: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        border: '1px solid rgba(243, 166, 31, 0.25)',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(22, 26, 38, 0.9) 100%)'
      }}>
        <Flame size={20} color="var(--accent-gold)" />
        <span style={{ fontWeight: '900', color: '#fff', fontSize: '1.05rem' }}>
          HOT STAR PLAYERS (TOP 12)
        </span>
      </div>

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
                  <div>
                    <div style={{ fontSize: '1.15rem', fontWeight: '900', color: '#fff' }}>
                      {player.nickname}
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                      {player.realName} • {player.country}
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

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.8rem' }}>
                <div style={{ padding: '8px 10px', background: 'rgba(0,0,0,0.2)', borderRadius: '4px' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>DPI / Sensitivity</div>
                  <div style={{ color: 'var(--accent-cyan)', fontWeight: '800' }}>
                    {player.dpi} / {player.generalSens}
                  </div>
                </div>
                <div style={{ padding: '8px 10px', background: 'rgba(0,0,0,0.2)', borderRadius: '4px' }}>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>Resolution</div>
                  <div style={{ color: '#fff', fontWeight: '700' }}>
                    {player.resolution}
                  </div>
                </div>
              </div>
            </div>

            <div style={{
              borderTop: '1px solid rgba(255, 255, 255, 0.06)',
              paddingTop: '12px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              fontSize: '0.78rem',
              color: 'var(--text-muted)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Mouse size={14} color="var(--accent-gold)" />
                <span style={{ color: '#ccc' }}>{player.mouseName}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '2px', color: 'var(--accent-gold)', fontWeight: '700' }}>
                <span>Detail</span>
                <ChevronRight size={14} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
