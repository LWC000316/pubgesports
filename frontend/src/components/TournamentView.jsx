import React, { useState } from 'react';
import { Trophy, Flame, DollarSign, MapPin, Calendar, Globe, Shield, Sparkles } from 'lucide-react';

export default function TournamentView({ tournaments, leaderboards }) {
  // 사용자가 요청한 세부 대회 탭 목록: ALL, PGS, PGC, EWC, PNC, PWS, PCL, APAC
  const [selectedTournamentType, setSelectedTournamentType] = useState('ALL');
  const [selectedTournamentId, setSelectedTournamentId] = useState(tournaments[0]?.id || 1);

  const tournamentTabs = [
    { id: 'ALL', label: '전체 대회 (ALL)', icon: Trophy },
    { id: 'PGS', label: 'PGS (글로벌 시리즈)', icon: Globe },
    { id: 'PGC', label: 'PGC (글로벌 챔피언십)', icon: Trophy },
    { id: 'EWC', label: 'EWC (사우디 e스포츠 월드컵)', icon: Sparkles },
    { id: 'PNC', label: 'PNC (펍지 네이션스 컵)', icon: Globe },
    { id: 'PWS', label: 'PWS (대한민국)', icon: Shield },
    { id: 'PCL', label: 'PCL (중국)', icon: Shield },
    { id: 'APAC', label: 'APAC (아시아태평양)', icon: Shield }
  ];

  // 선택된 대회 탭으로 필터링
  const filteredTournaments = tournaments.filter(t => {
    if (selectedTournamentType === 'ALL') return true;
    const nameUpper = t.name.toUpperCase();
    const slugUpper = (t.slug || '').toUpperCase();
    return nameUpper.includes(selectedTournamentType) || slugUpper.includes(selectedTournamentType);
  });

  const activeTournament = tournaments.find(t => t.id === selectedTournamentId) || filteredTournaments[0] || tournaments[0];

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      
      {/* 🏆 대회별 세부 탭 네비게이션 (PGS, PGC, EWC, PNC, PWS, PCL, APAC 등) */}
      <div style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '20px',
        overflowX: 'auto',
        paddingBottom: '6px'
      }}>
        {tournamentTabs.map(tab => {
          const Icon = tab.icon;
          const isActive = selectedTournamentType === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => {
                setSelectedTournamentType(tab.id);
                const firstMatched = tournaments.find(t => 
                  tab.id === 'ALL' || t.name.toUpperCase().includes(tab.id) || (t.slug && t.slug.toUpperCase().includes(tab.id))
                );
                if (firstMatched) setSelectedTournamentId(firstMatched.id);
              }}
              style={{
                padding: '9px 16px',
                borderRadius: 'var(--radius-sm)',
                border: isActive ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                background: isActive ? 'rgba(243, 166, 31, 0.18)' : 'rgba(22, 28, 41, 0.6)',
                color: isActive ? 'var(--accent-gold)' : 'var(--text-muted)',
                fontWeight: '800',
                fontSize: '0.85rem',
                cursor: 'pointer',
                fontFamily: 'var(--font-display)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                whiteSpace: 'nowrap',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon size={16} color={isActive ? 'var(--accent-gold)' : 'var(--text-muted)'} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* 해당 탭에 속한 토너먼트 리스트 카드 그리드 */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '14px',
        marginBottom: '24px'
      }}>
        {filteredTournaments.map(t => {
          const isSelected = activeTournament?.id === t.id;
          return (
            <div
              key={t.id}
              onClick={() => setSelectedTournamentId(t.id)}
              className="glass-panel"
              style={{
                padding: '16px 20px',
                cursor: 'pointer',
                border: isSelected ? '2px solid var(--accent-gold)' : '1px solid rgba(255,255,255,0.08)',
                background: isSelected
                  ? 'linear-gradient(135deg, rgba(243, 166, 31, 0.15) 0%, rgba(18, 24, 38, 0.95) 100%)'
                  : 'rgba(18, 24, 38, 0.6)',
                transition: 'all 0.2s ease',
                transform: isSelected ? 'translateY(-2px)' : 'none'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span className={`badge ${t.category === 'GLOBAL' ? 'badge-gold' : 'badge-cyan'}`}>
                  {t.tier || 'S-Tier'}
                </span>
                <span style={{ fontSize: '0.75rem', color: t.status === 'COMPLETED' ? 'var(--accent-green)' : 'var(--accent-gold)' }}>
                  {t.status === 'COMPLETED' ? '● 경기 완료' : '● 진행 예정'}
                </span>
              </div>
              <h4 style={{ color: '#fff', margin: '0 0 6px 0', fontSize: '1.05rem', fontWeight: '800' }}>
                {t.name}
              </h4>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                <span><MapPin size={12} style={{ verticalAlign: 'middle' }} /> {t.location}</span>
                <span style={{ color: 'var(--accent-green)' }}>{t.prizePool}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* 선택된 대회 메인 배너 */}
      <div className="glass-panel gold-glow-border" style={{
        padding: '24px 28px',
        marginBottom: '28px',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(18, 24, 38, 0.95) 100%)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <span className="badge badge-gold">{activeTournament?.tier || 'S-TIER'}</span>
              <span className="badge badge-cyan">{activeTournament?.region || 'GLOBAL'}</span>
              <span className="badge badge-green">KRAFTON OFFICIAL API</span>
            </div>
            <h2 style={{ fontSize: '1.8rem', color: '#fff', margin: '0 0 10px 0', fontWeight: '900' }}>
              {activeTournament?.name}
            </h2>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', color: 'var(--text-muted)', fontSize: '0.88rem' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <MapPin size={15} color="var(--accent-gold)" /> {activeTournament?.location}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <DollarSign size={15} color="var(--accent-green)" /> {activeTournament?.prizePool}
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Calendar size={15} color="var(--accent-cyan)" /> {activeTournament?.startDate} ~ {activeTournament?.endDate}
              </span>
            </div>
          </div>

          {activeTournament?.champion && (
            <div style={{
              background: 'rgba(243, 166, 31, 0.12)',
              border: '1px solid var(--accent-gold)',
              borderRadius: '8px',
              padding: '12px 20px',
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}>
              <Sparkles size={24} color="var(--accent-gold)" />
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', fontWeight: '800' }}>OFFICIAL CHAMPION</div>
                <div style={{ fontSize: '1.1rem', color: '#fff', fontWeight: '900' }}>{activeTournament.champion}</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 리더보드 순위표 */}
      <div className="glass-panel" style={{ padding: '20px', overflowX: 'auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', padding: '0 8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Flame size={20} color="var(--accent-gold)" />
            <h3 style={{ fontSize: '1.2rem', color: '#fff', margin: 0 }}>
              {activeTournament?.name} 그랜드 파이널 종합 순위표 (LEADERBOARD)
            </h3>
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
                  <td style={{ textAlign: 'center', fontWeight: '700', color: row.wwcdCount > 0 ? 'var(--accent-gold)' : 'var(--text-muted)' }}>
                    {row.wwcdCount}
                  </td>
                  <td style={{ textAlign: 'center', color: 'var(--text-main)' }}>{row.killPoints}</td>
                  <td style={{ textAlign: 'center', color: 'var(--text-muted)' }}>{row.placementPoints}</td>
                  <td style={{ textAlign: 'center', fontWeight: '900', fontSize: '1.1rem', color: 'var(--accent-gold)' }}>
                    {row.totalPoints}
                  </td>
                  <td style={{ textAlign: 'right', fontWeight: '700', color: 'var(--accent-green)' }}>
                    {row.prize}
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
