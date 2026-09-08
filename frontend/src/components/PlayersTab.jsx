import React, { useState } from 'react';
import { Search, Shield, Mouse, ChevronRight, Flame, Users, Crosshair, Award } from 'lucide-react';
import { LATEST_PWS2_TEAMS, HOT_PLAYERS_12 } from '../data/esportsData';

export default function PlayersTab({ onSelectPlayer }) {
  const [selectedTab, setSelectedTab] = useState('PWS');
  const [searchQuery, setSearchQuery] = useState('');

  const filterChips = [
    { id: 'HOT', label: 'HOT', icon: Flame, desc: '인기 선수 TOP 12' },
    { id: 'PWS', label: 'PWS (한국)', flag: '🇰🇷', desc: 'PWS 2 최신 공식 참가팀' },
    { id: 'PCL', label: 'PCL (중국)', flag: '🇨🇳', desc: '중국 챔피언스 리그' },
    { id: 'EMEA', label: 'EMEA (유럽)', flag: '🇪🇺', desc: '유럽 중동 아프리카' },
    { id: 'AMER', label: 'AMER (아메리카)', flag: '🇺🇸', desc: '아메리카 시리즈' },
    { id: 'APAC', label: 'APAC (아태)', flag: '🌏', desc: '아시아 태평양' }
  ];

  // PWS 탭일 때: 최신 PWS 2 공식 참가팀 필터링
  const filteredTeams = LATEST_PWS2_TEAMS.filter(t => {
    const q = searchQuery.toLowerCase();
    const matchesTeamName = t.name.toLowerCase().includes(q) || t.koreanName.includes(q) || t.tag.toLowerCase().includes(q);
    const matchesRoster = t.roster.some(p => p.nickname.toLowerCase().includes(q) || p.realName.includes(q));
    return matchesTeamName || matchesRoster;
  });

  // HOT 탭일 때: 최다 조회 스타 선수 12인 필터링
  const filteredHotPlayers = HOT_PLAYERS_12.filter(p => {
    const q = searchQuery.toLowerCase();
    return p.nickname.toLowerCase().includes(q) || p.realName.includes(q) || p.team.toLowerCase().includes(q);
  });

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      
      {/* 상단 탭 칩 및 검색창 */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '16px',
        marginBottom: '28px'
      }}>
        {/* 권역 탭 칩: HOT, PWS(한국), PCL, EMEA, AMER, APAC */}
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {filterChips.map(chip => {
            const isActive = selectedTab === chip.id;
            const Icon = chip.icon;
            return (
              <button
                key={chip.id}
                onClick={() => setSelectedTab(chip.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '9px 18px',
                  borderRadius: 'var(--radius-sm)',
                  background: isActive ? 'var(--accent-gold)' : 'rgba(255, 255, 255, 0.04)',
                  color: isActive ? '#000' : 'var(--text-muted)',
                  border: isActive ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                  fontWeight: '800',
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                {Icon && <Icon size={16} color={isActive ? '#000' : 'var(--accent-gold)'} />}
                {chip.flag && <span>{chip.flag}</span>}
                <span>{chip.label}</span>
              </button>
            );
          })}
        </div>

        {/* 검색 인풋 */}
        <div style={{ position: 'relative', minWidth: '300px' }}>
          <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            placeholder={selectedTab === 'PWS' ? "팀명 또는 선수 닉네임 검색..." : "선수명, 소속팀 검색..."}
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '10px 14px 10px 38px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid var(--border-subtle)',
              color: '#fff',
              fontSize: '0.88rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      {/* 1. PWS (한국) 선택 시: 최신 PWS 2 공식 참가팀 뷰 */}
      {selectedTab === 'PWS' && (
        <div>
          {/* PWS 2 최신화 안내 헤더 바 */}
          <div className="glass-panel" style={{
            padding: '16px 20px',
            borderRadius: 'var(--radius-sm)',
            marginBottom: '20px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '12px',
            border: '1px solid rgba(243, 166, 31, 0.25)',
            background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(22, 26, 38, 0.9) 100%)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Shield size={20} color="var(--accent-gold)" />
              <div>
                <span style={{ fontWeight: '900', color: '#fff', fontSize: '1.05rem' }}>
                  2024 PWS Phase 2 공식 파이널 참가팀
                </span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginLeft: '10px' }}>
                  (공식 PUBG API 텔레메트리 최신 실전 로스터 반영)
                </span>
              </div>
            </div>
            <div className="badge badge-gold" style={{ fontSize: '0.75rem' }}>
              최신 PWS 2 공식 로스터
            </div>
          </div>

          {/* 팀 카드 그리드 */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
            gap: '20px'
          }}>
            {filteredTeams.map((team) => (
              <div
                key={team.id}
                className="glass-panel"
                style={{
                  padding: '22px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-subtle)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '16px',
                  transition: 'all 0.2s ease'
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
                {/* 팀 헤더: 로고 심볼 + 팀명 + TAG */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <div style={{
                      width: '46px',
                      height: '46px',
                      borderRadius: '8px',
                      background: 'rgba(243, 166, 31, 0.15)',
                      border: '1px solid rgba(243, 166, 31, 0.3)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: '900',
                      fontSize: '1rem',
                      color: 'var(--accent-gold)'
                    }}>
                      {team.tag}
                    </div>
                    <div>
                      <div style={{ fontSize: '1.2rem', fontWeight: '900', color: '#fff' }}>
                        {team.name}
                      </div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {team.koreanName} • PWS Phase 2
                      </div>
                    </div>
                  </div>
                  <span className="badge badge-gold" style={{ fontSize: '0.72rem' }}>
                    #{team.rank}위
                  </span>
                </div>

                {/* 팀 소개 문구 */}
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', margin: 0 }}>
                  {team.description}
                </p>

                {/* 최신 실전 로스터 4인 카드 목록 */}
                <div style={{
                  borderTop: '1px solid rgba(255, 255, 255, 0.06)',
                  paddingTop: '12px'
                }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px', fontWeight: '700' }}>
                    공식 참가 로스터 (클릭 시 상세 세팅 조회)
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                    {team.roster.map((player) => (
                      <div
                        key={player.nickname}
                        onClick={() => onSelectPlayer && onSelectPlayer({
                          ...player,
                          team: team.name,
                          league: 'PWS',
                          country: 'KR',
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
                          <span style={{ fontSize: '0.7rem', color: 'var(--accent-gold)' }}>
                            {player.dpi}DPI
                          </span>
                        </div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {player.realName} • {player.role}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. HOT 선택 시: 제일 많이 찾아본 대표 스타 선수 12명 뷰 */}
      {selectedTab === 'HOT' && (
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
              HOT STAR PLAYERS (가장 많이 찾아본 선수 TOP 12)
            </span>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '20px'
          }}>
            {filteredHotPlayers.map((player, idx) => (
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
                    <span style={{ color: 'var(--text-muted)' }}>소속팀</span>
                    <span style={{ color: '#fff', fontWeight: '700' }}>{player.team}</span>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '0.8rem' }}>
                    <div style={{ padding: '8px 10px', background: 'rgba(0,0,0,0.2)', borderRadius: '4px' }}>
                      <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>DPI / 일반감도</div>
                      <div style={{ color: 'var(--accent-cyan)', fontWeight: '800' }}>
                        {player.dpi} / {player.generalSens}
                      </div>
                    </div>
                    <div style={{ padding: '8px 10px', background: 'rgba(0,0,0,0.2)', borderRadius: '4px' }}>
                      <div style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>해상도</div>
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
                    <span>상세</span>
                    <ChevronRight size={14} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 3. 기타 권역(PCL, EMEA, AMER, APAC) 준비 중 안내 */}
      {selectedTab !== 'PWS' && selectedTab !== 'HOT' && (
        <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center' }}>
          <Shield size={36} color="var(--accent-gold)" style={{ margin: '0 auto 16px auto' }} />
          <h3 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>
            {selectedTab} 권역 공식 최신 로스터 준비 중
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            현재 PWS(한국) 탭과 HOT 탭이 우선 개편되었습니다. 공식 PUBG API로부터 순차적으로 최신화될 예정입니다.
          </p>
        </div>
      )}
    </div>
  );
}
