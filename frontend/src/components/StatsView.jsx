import React from 'react';
import { Target, Skull, Shield, Award, Zap } from 'lucide-react';

export default function StatsView({ stats }) {
  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      {/* Top MVP Highlights Card */}
      {stats.length > 0 && (
        <div className="glass-panel gold-glow-border" style={{
          padding: '24px',
          marginBottom: '28px',
          background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.12) 0%, rgba(22, 28, 41, 0.95) 100%)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '20px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #f3a61f 0%, #ff5200 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: 'var(--shadow-glow)'
            }}>
              <Award size={36} color="#0b0d13" />
            </div>

            <div>
              <span className="badge badge-gold" style={{ marginBottom: '4px' }}>TOURNAMENT TOP FRAGGER</span>
              <h2 style={{ fontSize: '1.8rem', color: '#fff', margin: 0, fontWeight: '900' }}>
                {stats[0].playerNickname} <span style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>({stats[0].teamName})</span>
              </h2>
              <p style={{ color: 'var(--accent-gold)', fontSize: '0.9rem', margin: '2px 0 0', fontWeight: '700' }}>
                {stats[0].kills} KILLS • {stats[0].damage.toLocaleString()} DAMAGE • TWIRE RATING {stats[0].twireRating}
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '16px' }}>
            <div style={{ background: 'rgba(11, 13, 19, 0.7)', padding: '12px 20px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>TOP DAMAGE</span>
              <p style={{ fontSize: '1.3rem', fontWeight: '900', color: 'var(--accent-gold)', margin: 0 }}>
                {stats[0].damage.toLocaleString()}
              </p>
            </div>
            <div style={{ background: 'rgba(11, 13, 19, 0.7)', padding: '12px 20px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>TWIRE RATING</span>
              <p style={{ fontSize: '1.3rem', fontWeight: '900', color: 'var(--accent-cyan)', margin: 0 }}>
                {stats[0].twireRating}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Twire.gg Style Player Stat Table */}
      <div className="glass-panel" style={{ padding: '20px', overflowX: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '0 8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Target size={20} color="var(--accent-cyan)" />
            <h3 style={{ fontSize: '1.2rem', color: '#fff', margin: 0 }}>선수 개인 스탯 랭킹 (PLAYER STATS LEADERBOARD)</h3>
          </div>
          <span className="badge badge-cyan">PGS 4 GRAND FINAL</span>
        </div>

        <table className="twire-table">
          <thead>
            <tr>
              <th style={{ width: '70px', textAlign: 'center' }}>RANK</th>
              <th>PLAYER</th>
              <th>TEAM</th>
              <th style={{ width: '100px', textAlign: 'center', color: 'var(--accent-gold)' }}>KILLS</th>
              <th style={{ width: '120px', textAlign: 'center' }}>DAMAGE</th>
              <th style={{ width: '100px', textAlign: 'center' }}>KNOCKS</th>
              <th style={{ width: '100px', textAlign: 'center' }}>ASSISTS</th>
              <th style={{ width: '110px', textAlign: 'center' }}>HEADSHOT %</th>
              <th style={{ width: '120px', textAlign: 'center', color: 'var(--accent-cyan)' }}>TWIRE RATING</th>
            </tr>
          </thead>
          <tbody>
            {stats.map((row) => (
              <tr key={row.rank}>
                <td style={{ textAlign: 'center', fontWeight: '800', fontSize: '1rem', color: row.rank === 1 ? 'var(--accent-gold)' : '#fff' }}>
                  #{row.rank}
                </td>
                <td>
                  <strong style={{ fontSize: '1.05rem', color: '#fff' }}>{row.playerNickname}</strong>
                </td>
                <td>
                  <span className="badge badge-gold" style={{ fontSize: '0.75rem' }}>{row.teamName}</span>
                </td>
                <td style={{ textAlign: 'center', fontWeight: '900', fontSize: '1.15rem', color: 'var(--accent-gold)' }}>
                  {row.kills}
                </td>
                <td style={{ textAlign: 'center', fontWeight: '700', color: '#fff' }}>
                  {row.damage?.toLocaleString()}
                </td>
                <td style={{ textAlign: 'center', fontWeight: '600' }}>
                  {row.knocks}
                </td>
                <td style={{ textAlign: 'center', fontWeight: '600' }}>
                  {row.assists}
                </td>
                <td style={{ textAlign: 'center', fontWeight: '600' }}>
                  {row.headshotRate}%
                </td>
                <td style={{ textAlign: 'center', fontWeight: '900', color: 'var(--accent-cyan)', fontSize: '1.1rem' }}>
                  {row.twireRating}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
