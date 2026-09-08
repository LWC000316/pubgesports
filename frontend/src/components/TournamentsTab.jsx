import React, { useState } from 'react';
import { Trophy, MapPin, Calendar, DollarSign, Medal, Award, Flame } from 'lucide-react';
import { TOURNAMENTS_DATA, LEADERBOARD_PGS4 } from '../data/esportsData';

export default function TournamentsTab() {
  const [selectedTourneyId, setSelectedTourneyId] = useState(TOURNAMENTS_DATA[0].id);

  const currentTourney = TOURNAMENTS_DATA.find(t => t.id === selectedTourneyId) || TOURNAMENTS_DATA[0];
  const leaderboard = LEADERBOARD_PGS4;

  const topThree = leaderboard.slice(0, 3);

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      
      {/* 대회 셀렉터 탭 */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '24px', flexWrap: 'wrap' }}>
        {TOURNAMENTS_DATA.map(t => {
          const isActive = selectedTourneyId === t.id;
          return (
            <button
              key={t.id}
              onClick={() => setSelectedTourneyId(t.id)}
              style={{
                padding: '10px 20px',
                borderRadius: 'var(--radius-sm)',
                background: isActive ? 'var(--accent-gold)' : 'rgba(255, 255, 255, 0.04)',
                color: isActive ? '#000' : 'var(--text-muted)',
                border: isActive ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                fontWeight: '800',
                fontSize: '0.88rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Trophy size={16} />
              <span>{t.name}</span>
            </button>
          );
        })}
      </div>

      {/* 대회 개요 메타 바 */}
      <div className="glass-panel" style={{
        padding: '20px 24px',
        borderRadius: 'var(--radius-md)',
        marginBottom: '28px',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '20px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
            <h2 style={{ fontSize: '1.4rem', fontWeight: '900', color: '#fff', margin: 0 }}>
              {currentTourney.name}
            </h2>
            <span className="badge badge-gold">{currentTourney.tier}</span>
            <span className="badge badge-cyan">{currentTourney.status}</span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: 0 }}>
            그랜드 파이널 18개 매치 종합 결과 (SUPER 룰셋 공식 포인트 규정 적용)
          </p>
        </div>

        {/* 메타 인포 칩들 */}
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', fontSize: '0.85rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-muted)' }}>
            <MapPin size={16} color="var(--accent-cyan)" />
            <span style={{ color: '#fff' }}>{currentTourney.location}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-muted)' }}>
            <Calendar size={16} color="var(--accent-cyan)" />
            <span style={{ color: '#fff' }}>{currentTourney.period}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-muted)' }}>
            <DollarSign size={16} color="var(--accent-gold)" />
            <span style={{ color: 'var(--accent-gold)', fontWeight: '800' }}>총상금 {currentTourney.prizePool}</span>
          </div>
        </div>
      </div>

      {/* 상위 1~3위 포디움 카드 */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '20px',
        marginBottom: '28px'
      }}>
        {topThree.map((item, idx) => {
          const colors = [
            { border: '#f3a61f', bg: 'rgba(243, 166, 31, 0.08)', title: '1ST CHAMPION', badge: 'badge-gold' },
            { border: '#00e5ff', bg: 'rgba(0, 229, 255, 0.08)', title: '2ND RUNNER UP', badge: 'badge-cyan' },
            { border: '#cd7f32', bg: 'rgba(205, 127, 50, 0.08)', title: '3RD PLACE', badge: 'badge-gold' }
          ][idx];

          return (
            <div
              key={item.rank}
              className="glass-panel"
              style={{
                padding: '20px',
                borderRadius: 'var(--radius-md)',
                border: `1px solid ${colors.border}`,
                background: colors.bg,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                  <Award size={18} color={colors.border} />
                  <span style={{ fontSize: '0.8rem', fontWeight: '900', color: colors.border, letterSpacing: '0.5px' }}>
                    {colors.title}
                  </span>
                </div>
                <div style={{ fontSize: '1.35rem', fontWeight: '900', color: '#fff', marginBottom: '4px' }}>
                  {item.team}
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {item.region} 권역 • 상금 {item.prize}
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.8rem', fontWeight: '900', color: colors.border, fontFamily: 'var(--font-display)' }}>
                  {item.total}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  치킨 {item.wwcd}회 • {item.killPoints}킬
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* 종합 리더보드 테이블 */}
      <div className="glass-panel" style={{ borderRadius: 'var(--radius-md)', overflow: 'hidden' }}>
        <div style={{ padding: '18px 24px', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: '800', color: '#fff', margin: 0 }}>
            종합 순위표 (Leaderboard)
          </h3>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            총 16개 프로팀 참가
          </span>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
            <thead>
              <tr style={{ background: 'rgba(255, 255, 255, 0.02)', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '14px 20px', width: '70px', textAlign: 'center' }}>순위</th>
                <th style={{ padding: '14px 20px' }}>팀명</th>
                <th style={{ padding: '14px 16px', textAlign: 'center' }}>권역</th>
                <th style={{ padding: '14px 16px', textAlign: 'center' }}>치킨(WWCD)</th>
                <th style={{ padding: '14px 16px', textAlign: 'center' }}>킬 포인트</th>
                <th style={{ padding: '14px 16px', textAlign: 'center' }}>순위 포인트</th>
                <th style={{ padding: '14px 20px', textAlign: 'center' }}>토탈 점수</th>
                <th style={{ padding: '14px 20px', textAlign: 'right' }}>상금</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((row) => {
                const isTop3 = row.rank <= 3;
                return (
                  <tr
                    key={row.rank}
                    style={{
                      borderBottom: '1px solid rgba(255, 255, 255, 0.04)',
                      background: isTop3 ? 'rgba(243, 166, 31, 0.03)' : 'transparent',
                      transition: 'background 0.15s ease'
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.04)'}
                    onMouseLeave={e => e.currentTarget.style.background = isTop3 ? 'rgba(243, 166, 31, 0.03)' : 'transparent'}
                  >
                    <td style={{ padding: '14px 20px', textAlign: 'center', fontWeight: '900', color: isTop3 ? 'var(--accent-gold)' : 'var(--text-muted)' }}>
                      #{row.rank}
                    </td>
                    <td style={{ padding: '14px 20px', fontWeight: '800', color: '#fff' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span style={{
                          display: 'inline-block',
                          width: '24px',
                          height: '24px',
                          borderRadius: '4px',
                          background: 'rgba(255, 255, 255, 0.08)',
                          textAlign: 'center',
                          lineHeight: '24px',
                          fontSize: '0.72rem',
                          fontWeight: '800',
                          color: 'var(--accent-gold)'
                        }}>
                          {row.tag}
                        </span>
                        <span>{row.team}</span>
                      </div>
                    </td>
                    <td style={{ padding: '14px 16px', textAlign: 'center', color: 'var(--text-muted)' }}>
                      {row.region}
                    </td>
                    <td style={{ padding: '14px 16px', textAlign: 'center', fontWeight: '700', color: row.wwcd > 0 ? 'var(--accent-gold)' : 'var(--text-muted)' }}>
                      {row.wwcd > 0 ? `${row.wwcd}회 🍗` : '0회'}
                    </td>
                    <td style={{ padding: '14px 16px', textAlign: 'center', color: 'var(--accent-cyan)', fontWeight: '700' }}>
                      {row.killPoints}
                    </td>
                    <td style={{ padding: '14px 16px', textAlign: 'center', color: 'var(--text-muted)' }}>
                      {row.rankPoints}
                    </td>
                    <td style={{ padding: '14px 20px', textAlign: 'center', fontWeight: '900', color: '#fff', fontSize: '1.05rem', fontFamily: 'var(--font-display)' }}>
                      {row.total}
                    </td>
                    <td style={{ padding: '14px 20px', textAlign: 'right', color: 'var(--text-muted)', fontWeight: '600' }}>
                      {row.prize}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
