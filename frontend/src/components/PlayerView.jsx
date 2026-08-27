import React, { useState } from 'react';
import { Search, Mouse, Crosshair, ExternalLink, ShieldCheck, Zap } from 'lucide-react';

export default function PlayerView({ players, onSelectPlayer }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTeam, setSelectedTeam] = useState('ALL');

  // 중복 없는 팀 목록 추출
  const teams = ['ALL', ...new Set(players.map(p => p.teamName).filter(Boolean))];

  // 필터링 로직
  const filteredPlayers = players.filter(player => {
    const matchesSearch = 
      player.nickname.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (player.realName && player.realName.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (player.mouseName && player.mouseName.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesTeam = selectedTeam === 'ALL' || player.teamName === selectedTeam;

    return matchesSearch && matchesTeam;
  });

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      {/* Top Filter & Search Bar */}
      <div className="glass-panel" style={{
        padding: '20px 24px',
        marginBottom: '28px',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '16px',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* Search Input */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          background: 'rgba(11, 13, 19, 0.8)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-sm)',
          padding: '10px 16px',
          width: '340px'
        }}>
          <Search size={18} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="선수 닉네임, 본명, 마우스 검색 (예: Seoul, G PRO)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#fff',
              outline: 'none',
              width: '100%',
              fontSize: '0.9rem',
              fontFamily: 'var(--font-primary)'
            }}
          />
        </div>

        {/* Team Filter Pills */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '700', marginRight: '4px' }}>
            TEAM:
          </span>
          {teams.map(team => (
            <button
              key={team}
              onClick={() => setSelectedTeam(team)}
              style={{
                padding: '6px 14px',
                borderRadius: 'var(--radius-sm)',
                border: selectedTeam === team ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                background: selectedTeam === team ? 'rgba(243, 166, 31, 0.15)' : 'rgba(22, 28, 41, 0.6)',
                color: selectedTeam === team ? 'var(--accent-gold)' : 'var(--text-muted)',
                fontWeight: '700',
                fontSize: '0.8rem',
                cursor: 'pointer',
                fontFamily: 'var(--font-display)',
                transition: 'all 0.2s ease'
              }}
            >
              {team}
            </button>
          ))}
        </div>
      </div>

      {/* Player Card Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(290px, 1fr))',
        gap: '20px'
      }}>
        {filteredPlayers.map((player) => (
          <div
            key={player.id}
            onClick={() => onSelectPlayer(player.id)}
            className="glass-panel"
            style={{
              cursor: 'pointer',
              overflow: 'hidden',
              transition: 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)',
              border: '1px solid var(--border-subtle)',
              position: 'relative'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-6px)';
              e.currentTarget.style.borderColor = 'var(--accent-gold)';
              e.currentTarget.style.boxShadow = 'var(--shadow-glow)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.borderColor = 'var(--border-subtle)';
              e.currentTarget.style.boxShadow = 'var(--shadow-card)';
            }}
          >
            {/* Team Banner / Badge */}
            <div style={{
              padding: '12px 16px',
              background: 'linear-gradient(90deg, rgba(243, 166, 31, 0.1) 0%, transparent 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              borderBottom: '1px solid var(--border-subtle)'
            }}>
              <span className="badge badge-gold">{player.teamName || 'FREE AGENT'}</span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '600' }}>
                {player.country} 🇰🇷
              </span>
            </div>

            {/* Main Profile Info */}
            <div style={{ padding: '20px 18px', display: 'flex', gap: '16px', alignItems: 'center' }}>
              <div style={{
                width: '74px',
                height: '74px',
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                border: '2px solid var(--border-active)',
                background: '#1a2233',
                flexShrink: 0
              }}>
                <img
                  src={player.profileImageUrl}
                  alt={player.nickname}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>

              <div>
                <h3 style={{ fontSize: '1.4rem', color: '#fff', margin: 0, fontWeight: '800' }}>
                  {player.nickname}
                </h3>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: '2px 0 6px' }}>
                  {player.realName}
                </p>
                <span className="badge badge-cyan" style={{ fontSize: '0.7rem' }}>
                  {player.role || 'ATTACKER'}
                </span>
              </div>
            </div>

            {/* Quick Spec Bar (DPI, Sens, Mouse) */}
            <div style={{
              padding: '12px 18px',
              background: 'rgba(11, 13, 19, 0.7)',
              borderTop: '1px solid var(--border-subtle)',
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '10px',
              fontSize: '0.8rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Crosshair size={14} color="var(--accent-gold)" />
                <span style={{ color: 'var(--text-muted)' }}>DPI/감도:</span>
                <strong style={{ color: '#fff' }}>{player.mouseDpi || 800} / {player.generalSens || 30}</strong>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                <Mouse size={14} color="var(--accent-cyan)" />
                <span style={{ color: 'var(--text-main)', fontSize: '0.75rem' }} title={player.mouseName}>
                  {player.mouseName ? player.mouseName.replace('Logitech ', '').replace('Razer ', '') : 'G PRO X'}
                </span>
              </div>
            </div>

            {/* Click to view detail footer */}
            <div style={{
              padding: '8px 18px',
              background: 'rgba(243, 166, 31, 0.05)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              fontSize: '0.75rem',
              color: 'var(--accent-gold)'
            }}>
              <span>상세 세팅 & 장비 보기</span>
              <ExternalLink size={13} />
            </div>
          </div>
        ))}
      </div>

      {filteredPlayers.length === 0 && (
        <div className="glass-panel" style={{ padding: '60px', textAlign: 'center', marginTop: '20px' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>검색 조건에 맞는 선수가 없습니다.</p>
        </div>
      )}
    </div>
  );
}
