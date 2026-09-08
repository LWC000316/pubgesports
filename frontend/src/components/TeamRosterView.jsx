import React, { useState } from 'react';
import { Search, Shield, Trophy, Users, Crosshair, Mouse, ExternalLink, ChevronRight, UserCheck } from 'lucide-react';

export default function TeamRosterView({ teams = [], onSelectPlayer }) {
  const [selectedLeague, setSelectedLeague] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTeamId, setActiveTeamId] = useState(teams[0]?.id || null);

  const leagues = [
    { id: 'ALL', label: '전체 리그', flag: '🌐' },
    { id: 'PWS', label: 'PWS (한국)', flag: '🇰🇷' },
    { id: 'PCL', label: 'PCL (중국)', flag: '🇨🇳' },
    { id: 'EMEA', label: 'EMEA (유럽)', flag: '🇪🇺' },
    { id: 'AMER', label: 'AMER (아메리카)', flag: '🇺🇸' },
    { id: 'APAC', label: 'APAC (아시아태평양)', flag: '🌏' }
  ];

  // 필터링된 팀 목록
  const filteredTeams = teams.filter(team => {
    const matchesLeague = selectedLeague === 'ALL' || team.league === selectedLeague;
    const matchesSearch =
      team.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (team.players && team.players.some(p =>
        p.nickname?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (p.realName && p.realName.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (p.mouseName && p.mouseName.toLowerCase().includes(searchQuery.toLowerCase()))
      ));
    return matchesLeague && matchesSearch;
  });

  const currentTeam = teams.find(t => t.id === activeTeamId) || filteredTeams[0] || null;

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      
      {/* 검색창 및 리그 탭 */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '16px',
        marginBottom: '24px'
      }}>
        {/* 리그 필터 */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {leagues.map(l => {
            const isActive = selectedLeague === l.id;
            return (
              <button
                key={l.id}
                onClick={() => setSelectedLeague(l.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 16px',
                  borderRadius: 'var(--radius-sm)',
                  background: isActive ? 'var(--accent-gold)' : 'rgba(255, 255, 255, 0.04)',
                  color: isActive ? '#000' : 'var(--text-muted)',
                  border: isActive ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                  fontWeight: '700',
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                <span>{l.flag}</span>
                <span>{l.label}</span>
              </button>
            );
          })}
        </div>

        {/* 검색 인풋 */}
        <div style={{ position: 'relative', minWidth: '280px' }}>
          <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            placeholder="팀명, 선수 닉네임, 장비 검색..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '9px 12px 9px 36px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid var(--border-subtle)',
              color: '#fff',
              fontSize: '0.85rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* 데이터가 없을 때 표시할 클린 안내 화면 (Empty State) */}
      {(!teams || teams.length === 0) ? (
        <div className="glass-panel" style={{
          padding: '80px 40px',
          textAlign: 'center',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
          margin: '20px 0'
        }}>
          <div style={{
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            background: 'rgba(243, 166, 31, 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 20px auto'
          }}>
            <Shield size={32} color="var(--accent-gold)" />
          </div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: '800', color: '#fff', marginBottom: '10px' }}>
            등록된 PUBG ESPORTS 데이터가 없습니다
          </h2>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '500px', margin: '0 auto 24px auto', lineHeight: '1.6' }}>
            기존의 부정확한 데이터 및 불필요한 설정 가이드가 완전히 삭제되었습니다.
            앞으로 새로운 요구사항에 맞추어 정확한 선수 및 팀 정보, 기능을 구축할 준비가 완료되었습니다.
          </p>
        </div>
      ) : (
        /* 데이터가 있을 경우 팀 리스트 및 로스터 표시 */
        <div style={{
          display: 'grid',
          gridTemplateColumns: '320px 1fr',
          gap: '24px',
          alignItems: 'start'
        }}>
          {/* 좌측 팀 목록 */}
          <div className="glass-panel" style={{ padding: '16px', borderRadius: 'var(--radius-md)' }}>
            <h3 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '12px', paddingLeft: '8px' }}>
              팀 목록 ({filteredTeams.length})
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '700px', overflowY: 'auto' }}>
              {filteredTeams.map(team => {
                const isSelected = (currentTeam && currentTeam.id === team.id);
                return (
                  <div
                    key={team.id}
                    onClick={() => setActiveTeamId(team.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '12px 14px',
                      borderRadius: 'var(--radius-sm)',
                      background: isSelected ? 'rgba(243, 166, 31, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                      border: isSelected ? '1px solid var(--border-active)' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      {team.logoUrl ? (
                        <img src={team.logoUrl} alt={team.name} style={{ width: '28px', height: '28px', objectFit: 'contain' }} />
                      ) : (
                        <Shield size={22} color={isSelected ? 'var(--accent-gold)' : 'var(--text-muted)'} />
                      )}
                      <div>
                        <div style={{ fontWeight: '800', color: isSelected ? 'var(--accent-gold)' : '#fff', fontSize: '0.95rem' }}>
                          {team.name}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          {team.league} • {team.players?.length || 0}인
                        </div>
                      </div>
                    </div>
                    <ChevronRight size={16} color={isSelected ? 'var(--accent-gold)' : 'var(--text-muted)'} />
                  </div>
                );
              })}
            </div>
          </div>

          {/* 우측 선택된 팀 상세 및 로스터 */}
          {currentTeam && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div className="glass-panel" style={{ padding: '24px', borderRadius: 'var(--radius-md)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '20px' }}>
                  {currentTeam.logoUrl && (
                    <img src={currentTeam.logoUrl} alt={currentTeam.name} style={{ width: '48px', height: '48px', objectFit: 'contain' }} />
                  )}
                  <div>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: '900', color: '#fff', margin: 0 }}>
                      {currentTeam.name}
                    </h2>
                    <span className="badge badge-gold" style={{ marginTop: '4px' }}>
                      {currentTeam.league}
                    </span>
                  </div>
                </div>

                {/* 선수 로스터 카드 그리드 */}
                <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '14px' }}>
                  선수 로스터 ({currentTeam.players?.length || 0})
                </h4>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: '16px' }}>
                  {currentTeam.players?.map(player => (
                    <div
                      key={player.id}
                      onClick={() => onSelectPlayer && onSelectPlayer(player)}
                      className="glass-panel"
                      style={{
                        padding: '16px',
                        borderRadius: 'var(--radius-sm)',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        border: '1px solid var(--border-subtle)'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                        <div style={{
                          width: '40px',
                          height: '40px',
                          borderRadius: '50%',
                          background: 'rgba(255, 255, 255, 0.05)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontWeight: '800',
                          color: 'var(--accent-gold)'
                        }}>
                          {player.nickname?.[0] || 'P'}
                        </div>
                        <div>
                          <div style={{ fontWeight: '800', color: '#fff', fontSize: '1rem' }}>
                            {player.nickname}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                            {player.realName || '프로 선수'}
                          </div>
                        </div>
                      </div>

                      {/* 주요 스펙 미니 표시 */}
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <div>DPI: <span style={{ color: '#fff', fontWeight: '700' }}>{player.dpi || '미등록'}</span></div>
                        <div>마우스: <span style={{ color: '#fff', fontWeight: '700' }}>{player.mouseName || '미등록'}</span></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
