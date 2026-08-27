import React, { useState } from 'react';
import { Trophy, Flame, DollarSign, MapPin, Calendar, CheckCircle2 } from 'lucide-react';

export default function TournamentView({ tournaments, leaderboards }) {
  const [selectedTournamentId, setSelectedTournamentId] = useState(tournaments[0]?.id || 1);

  const activeTournament = tournaments.find(t => t.id === selectedTournamentId) || tournaments[0];

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      {/* Tournament Selector Header Banner */}
      <div className="glass-panel gold-glow-border" style={{
        padding: '24px 28px',
        marginBottom: '28px',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(18, 24, 38, 0.95) 100%)'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <span className="badge badge-gold">{activeTournament?.tier || 'S-TIER'}</span>
            <span className="badge badge-cyan">{activeTournament?.region || 'GLOBAL'}</span>
            <span className="badge badge-green">TWIRE.GG VERIFIED</span>
          </div>
          <h2 style={{ fontSize: '1.8rem', color: '#fff', margin: 0, fontWeight: '900' }}>
            {activeTournament?.name || 'PUBG Global Series 4 (PGS 4)'}
          </h2>
          <div style={{ display: 'flex', gap: '16px', marginTop: '8px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <MapPin size={14} color="var(--accent-gold)" /> {activeTournament?.location || 'Shanghai, China'}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <DollarSign size={14} color="var(--accent-green)" /> {activeTournament?.prizePool || '$300,000'}
            </span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Calendar size={14} color="var(--accent-cyan)" /> {activeTournament?.startDate} ~ {activeTournament?.endDate}
            </span>
          </div>
        </div>

        {/* Tournament Switcher Buttons */}
        <div style={{ display: 'flex', gap: '8px' }}>
          {tournaments.map(t => (
            <button
              key={t.id}
              onClick={() => setSelectedTournamentId(t.id)}
              className={selectedTournamentId === t.id ? 'btn-primary' : 'btn-secondary'}
              style={{ fontSize: '0.85rem' }}
            >
              <Trophy size={16} />
              {t.name.replace('PUBG Global Series', 'PGS')}
            </button>
          ))}
        </div>
      </div>

      {/* Twire.gg Style Leaderboard Table */}
      <div className="glass-panel" style={{ padding: '20px', overflowX: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '0 8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Flame size={20} color="var(--accent-gold)" />
            <h3 style={{ fontSize: '1.2rem', color: '#fff', margin: 0 }}>그랜드 파이널 종합 순위표 (LEADERBOARD)</h3>
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            SUPER 룰셋 (18 MATCHES)
          </span>
        </div>

        <table className="twire-table">
          <thead>
            <tr>
              <th style={{ width: '80px', textAlign: 'center' }}>RANK</th>
              <th>TEAM</th>
              <th style={{ width: '100px', textAlign: 'center' }}>REGION</th>
              <th style={{ width: '100px', textAlign: 'center' }}>🍗 WWCD</th>
              <th style={{ width: '110px', textAlign: 'center' }}>KILL PTS</th>
              <th style={{ width: '110px', textAlign: 'center' }}>PLACE PTS</th>
              <th style={{ width: '130px', textAlign: 'center', color: 'var(--accent-gold)' }}>TOTAL PTS</th>
              <th style={{ width: '120px', textAlign: 'right' }}>PRIZE</th>
            </tr>
          </thead>
          <tbody>
            {leaderboards.map((row) => {
              const isTop3 = row.rank <= 3;
              const rankColor = row.rank === 1 ? 'var(--accent-gold)' : row.rank === 2 ? '#e2e8f0' : row.rank === 3 ? '#d97706' : 'var(--text-muted)';

              return (
                <tr key={row.rank} style={{ borderLeft: isTop3 ? `4px solid ${rankColor}` : 'none' }}>
                  <td style={{ textAlign: 'center', fontWeight: '800', fontSize: '1.1rem', color: rankColor }}>
                    #{row.rank}
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <strong style={{ fontSize: '1.05rem', color: '#fff' }}>{row.teamName}</strong>
                    </div>
                  </td>
                  <td style={{ textAlign: 'center' }}>
                    <span className={`badge ${row.teamRegion === 'KR' ? 'badge-gold' : 'badge-cyan'}`}>
                      {row.teamRegion}
                    </span>
                  </td>
                  <td style={{ textAlign: 'center', fontWeight: '700', color: row.wwcdCount > 0 ? 'var(--accent-gold)' : 'var(--text-dim)' }}>
                    {row.wwcdCount}
                  </td>
                  <td style={{ textAlign: 'center', fontWeight: '600' }}>
                    {row.killPoints}
                  </td>
                  <td style={{ textAlign: 'center', fontWeight: '600' }}>
                    {row.placementPoints}
                  </td>
                  <td style={{ textAlign: 'center', fontWeight: '900', fontSize: '1.2rem', color: 'var(--accent-gold)' }}>
                    {row.totalPoints}
                  </td>
                  <td style={{ textAlign: 'right', fontWeight: '700', color: 'var(--accent-green)' }}>
                    {row.prize || '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
