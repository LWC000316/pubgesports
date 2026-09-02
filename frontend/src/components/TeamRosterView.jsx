import React, { useState } from 'react';
import { Search, Shield, Trophy, Users, Crosshair, Mouse, ExternalLink, ChevronRight, UserCheck, Calculator, ArrowRightLeft } from 'lucide-react';

export default function TeamRosterView({ teams, onSelectPlayer, onSelectTeam }) {
  const [selectedLeague, setSelectedLeague] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTeamId, setActiveTeamId] = useState(teams[0]?.id || 1);

  // 15스텝 감도 간이 계산기 상태
  const [calcDpi, setCalcDpi] = useState(800);
  const [calcSens, setCalcSens] = useState(30);

  const leagues = [
    { id: 'ALL', label: 'ALL LEAGUES', flag: '🌐' },
    { id: 'PWS', label: 'PWS (한국)', flag: '🇰🇷' },
    { id: 'PCL', label: 'PCL (중국)', flag: '🇨🇳' },
    { id: 'EMEA', label: 'EMEA (유럽)', flag: '🇪🇺' },
    { id: 'AMER', label: 'AMER (아메리카)', flag: '🇺🇸' },
    { id: 'APAC', label: 'APAC (아시아태평양)', flag: '🌏' }
  ];

  // 15스텝 계산 함수
  const calculate15Steps = (baseDpi, baseSens) => {
    let sens400 = baseSens;
    let sens800 = baseSens;
    let sens1600 = baseSens;

    if (baseDpi === 400) {
      sens400 = baseSens;
      sens800 = Math.max(0, baseSens - 15);
      sens1600 = Math.max(0, baseSens - 30);
    } else if (baseDpi === 800) {
      sens400 = baseSens + 15;
      sens800 = baseSens;
      sens1600 = Math.max(0, baseSens - 15);
    } else if (baseDpi === 1600) {
      sens400 = baseSens + 30;
      sens800 = baseSens + 15;
      sens1600 = baseSens;
    }
    return { sens400, sens800, sens1600 };
  };

  const currentCalc = calculate15Steps(calcDpi, calcSens);

  // 필터링된 팀 목록
  const filteredTeams = teams.filter(team => {
    const matchesLeague = selectedLeague === 'ALL' || team.league === selectedLeague;
    const matchesSearch = 
      team.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (team.players && team.players.some(p => 
        p.nickname.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (p.realName && p.realName.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (p.mouseName && p.mouseName.toLowerCase().includes(searchQuery.toLowerCase()))
      ));
    return matchesLeague && matchesSearch;
  });

  const currentTeam = teams.find(t => t.id === activeTeamId) || filteredTeams[0] || teams[0];

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      
      {/* 🎯 PUBG 15스텝 감도 법칙 상단 하이라이트 배너 */}
      <div className="glass-panel gold-glow-border" style={{
        padding: '18px 24px',
        marginBottom: '20px',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.12) 0%, rgba(18, 24, 38, 0.95) 100%)',
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        alignItems: 'center',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            background: 'rgba(243, 166, 31, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <ArrowRightLeft size={22} color="var(--accent-gold)" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '1.05rem', fontWeight: '900', color: '#fff' }}>PUBG 15스텝 감도 법칙 가이드</span>
              <span className="badge badge-gold">15 STEP RULE</span>
            </div>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', margin: '2px 0 0 0' }}>
              배틀그라운드는 DPI를 400 ↔ 800 ↔ 1600으로 2배 증감할 때 인게임 감도를 <strong style={{ color: 'var(--accent-gold)' }}>15씩 가감</strong>하면 정확히 동등한 체감 감도가 유지됩니다.
            </p>
          </div>
        </div>

        {/* 미니 15스텝 퀵 환산기 */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          background: 'rgba(11, 13, 19, 0.8)',
          padding: '8px 16px',
          borderRadius: '8px',
          border: '1px solid var(--border-subtle)'
        }}>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <span>기준: </span>
            <select
              value={calcDpi}
              onChange={(e) => setCalcDpi(Number(e.target.value))}
              style={{ background: '#1c2436', color: '#fff', border: '1px solid #334155', borderRadius: '4px', padding: '2px 6px', fontSize: '0.8rem' }}
            >
              <option value={400}>400 DPI</option>
              <option value={800}>800 DPI</option>
              <option value={1600}>1600 DPI</option>
            </select>
            <input
              type="number"
              value={calcSens}
              onChange={(e) => setCalcSens(Number(e.target.value))}
              style={{ width: '50px', marginLeft: '6px', background: '#1c2436', color: '#fff', border: '1px solid #334155', borderRadius: '4px', padding: '2px 6px', fontSize: '0.8rem' }}
            />
          </div>
          <div style={{ fontSize: '0.8rem', color: '#fff', display: 'flex', gap: '8px' }}>
            <span>👉 400DPI: <strong style={{ color: 'var(--accent-gold)' }}>{currentCalc.sens400}</strong></span>
            <span>800DPI: <strong style={{ color: 'var(--accent-cyan)' }}>{currentCalc.sens800}</strong></span>
            <span>1600DPI: <strong style={{ color: 'var(--accent-green)' }}>{currentCalc.sens1600}</strong></span>
          </div>
        </div>
      </div>

      {/* 1. 상단 권역별 리그 셀렉터 & 검색바 */}
      <div className="glass-panel" style={{
        padding: '18px 24px',
        marginBottom: '24px',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '16px',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        {/* 권역 탭 버튼들 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '800', marginRight: '4px' }}>
            권역별 리그:
          </span>
          {leagues.map(league => (
            <button
              key={league.id}
              onClick={() => setSelectedLeague(league.id)}
              style={{
                padding: '7px 14px',
                borderRadius: 'var(--radius-sm)',
                border: selectedLeague === league.id ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                background: selectedLeague === league.id ? 'rgba(243, 166, 31, 0.15)' : 'rgba(22, 28, 41, 0.6)',
                color: selectedLeague === league.id ? 'var(--accent-gold)' : 'var(--text-muted)',
                fontWeight: '800',
                fontSize: '0.8rem',
                cursor: 'pointer',
                fontFamily: 'var(--font-display)',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                transition: 'all 0.2s ease'
              }}
            >
              <span>{league.flag}</span>
              <span>{league.label}</span>
            </button>
          ))}
        </div>

        {/* 검색 인풋 */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          background: 'rgba(11, 13, 19, 0.8)',
          border: '1px solid var(--border-subtle)',
          borderRadius: 'var(--radius-sm)',
          padding: '8px 14px',
          width: '320px'
        }}>
          <Search size={16} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="팀명, 선수 닉네임, 마우스 검색..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#fff',
              outline: 'none',
              width: '100%',
              fontSize: '0.85rem',
              fontFamily: 'var(--font-primary)'
            }}
          />
        </div>
      </div>

      {/* 2. 메인 컨텐츠: 2분할 뷰 (좌측: 선택된 팀 상세 & 로스터 / 우측: 권역 팀 목록) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'minmax(0, 1.8fr) minmax(320px, 1fr)',
        gap: '24px'
      }}>
        
        {/* === 좌측: 선택된 팀의 상세 배너 및 선수 로스터 카드 === */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {currentTeam ? (
            <>
              {/* 팀 헤더 배너 */}
              <div className="glass-panel gold-glow-border" style={{
                padding: '24px 28px',
                background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(18, 24, 38, 0.95) 100%)',
                position: 'relative'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '20px', flexWrap: 'wrap' }}>
                  <img
                    src={currentTeam.logoUrl || 'https://via.placeholder.com/100'}
                    alt={currentTeam.name}
                    style={{
                      width: '76px',
                      height: '76px',
                      objectFit: 'contain',
                      background: 'rgba(255, 255, 255, 0.05)',
                      padding: '8px',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid var(--border-subtle)'
                    }}
                  />
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                      <span className="badge badge-gold">{currentTeam.league || 'PWS'}</span>
                      <span className="badge badge-cyan">{currentTeam.region || 'KR'}</span>
                      {currentTeam.foundedYear && (
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                          창단: {currentTeam.foundedYear}년
                        </span>
                      )}
                    </div>
                    <h2 style={{ fontSize: '2rem', fontWeight: '900', color: '#fff', margin: '0 0 6px 0', letterSpacing: '0.5px' }}>
                      {currentTeam.name}
                    </h2>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', margin: 0, lineHeight: 1.5 }}>
                      {currentTeam.description}
                    </p>
                  </div>
                </div>

                {/* 코치 & 수상 내역 */}
                <div style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: '20px',
                  marginTop: '18px',
                  paddingTop: '16px',
                  borderTop: '1px solid rgba(255, 255, 255, 0.08)',
                  fontSize: '0.85rem'
                }}>
                  {currentTeam.coach && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-main)' }}>
                      <UserCheck size={16} color="var(--accent-cyan)" />
                      <span>감독/코치: <strong>{currentTeam.coach}</strong></span>
                    </div>
                  )}
                  {currentTeam.achievements && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-gold)' }}>
                      <Trophy size={16} color="var(--accent-gold)" />
                      <span>{currentTeam.achievements}</span>
                    </div>
                  )}
                </div>
              </div>

              {/* 팀 소속 선수 로스터 헤더 */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px' }}>
                <h3 style={{ fontSize: '1.25rem', color: '#fff', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Users size={20} color="var(--accent-gold)" />
                  <span>소속 선수 로스터 ({currentTeam.players ? currentTeam.players.length : 0}명)</span>
                </h3>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  선수 카드를 클릭하면 감도 & 15스텝 환산 세팅을 확인합니다
                </span>
              </div>

              {/* 선수 로스터 카드 그리드 */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
                gap: '16px'
              }}>
                {currentTeam.players && currentTeam.players.map((player) => {
                  const playerSteps = calculate15Steps(player.mouseDpi || 800, player.generalSens || 30);

                  return (
                    <div
                      key={player.id}
                      onClick={() => onSelectPlayer(player.id)}
                      className="glass-panel"
                      style={{
                        padding: '18px',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        position: 'relative',
                        overflow: 'hidden'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-4px)';
                        e.currentTarget.style.borderColor = 'var(--border-active)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'none';
                        e.currentTarget.style.borderColor = 'var(--border-subtle)';
                      }}
                    >
                      {/* 선수 프로필 헤더 */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '14px' }}>
                        <img
                          src={player.profileImageUrl || 'https://via.placeholder.com/80'}
                          alt={player.nickname}
                          style={{
                            width: '52px',
                            height: '52px',
                            borderRadius: '50%',
                            objectFit: 'cover',
                            border: '2px solid var(--border-subtle)'
                          }}
                        />
                        <div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                            <strong style={{ fontSize: '1.2rem', color: '#fff', fontFamily: 'var(--font-display)' }}>
                              {player.nickname}
                            </strong>
                          </div>
                          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                            {player.realName || '프로 선수'} • {player.role || 'Player'}
                          </span>
                        </div>
                      </div>

                      {/* 감도 요약 & 15스텝 동등 감도 칩 */}
                      <div style={{
                        background: 'rgba(11, 13, 19, 0.7)',
                        borderRadius: 'var(--radius-sm)',
                        padding: '12px',
                        marginBottom: '12px'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>기본 세팅:</span>
                          <span style={{ fontSize: '0.85rem', fontWeight: '800', color: 'var(--accent-gold)' }}>
                            {player.mouseDpi || 800} DPI / 감도 {player.generalSens || 30}
                          </span>
                        </div>

                        {/* 15스텝 법칙 미니 환산표 */}
                        <div style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          paddingTop: '6px',
                          borderTop: '1px solid rgba(255,255,255,0.06)',
                          fontSize: '0.75rem'
                        }}>
                          <span style={{ color: 'var(--text-muted)' }}>15스텝 환산:</span>
                          <span style={{ color: '#fff' }}>
                            400DPI(<strong style={{ color: 'var(--accent-gold)' }}>{playerSteps.sens400}</strong>) • 800DPI(<strong style={{ color: 'var(--accent-cyan)' }}>{playerSteps.sens800}</strong>) • 1600DPI(<strong style={{ color: 'var(--accent-green)' }}>{playerSteps.sens1600}</strong>)
                          </span>
                        </div>
                      </div>

                      {/* 마우스 장비 정보 */}
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        fontSize: '0.78rem',
                        color: 'var(--text-muted)'
                      }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          <Mouse size={14} color="var(--accent-cyan)" />
                          {player.mouseName || 'Logitech G PRO X SUPERLIGHT 2'}
                        </span>
                        <ChevronRight size={16} color="var(--accent-gold)" />
                      </div>
                    </div>
                  );
                })}
              </div>
            </>
          ) : (
            <div className="glass-panel" style={{ padding: '60px', textAlign: 'center' }}>
              <p style={{ color: 'var(--text-muted)', margin: 0 }}>선택된 팀이 없습니다.</p>
            </div>
          )}
        </div>

        {/* === 우측: 해당 권역의 팀 목록 박스 그리드 === */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '1.1rem', color: '#fff', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Shield size={18} color="var(--accent-cyan)" />
              <span>{selectedLeague} 리그 팀 목록 ({filteredTeams.length}팀)</span>
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {filteredTeams.map((team) => {
              const isSelected = team.id === (currentTeam?.id);

              return (
                <div
                  key={team.id}
                  onClick={() => setActiveTeamId(team.id)}
                  className="glass-panel"
                  style={{
                    padding: '14px 18px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    border: isSelected ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                    background: isSelected ? 'rgba(243, 166, 31, 0.12)' : 'rgba(22, 28, 41, 0.6)',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <img
                      src={team.logoUrl || 'https://via.placeholder.com/40'}
                      alt={team.name}
                      style={{ width: '36px', height: '36px', objectFit: 'contain' }}
                    />
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <strong style={{ color: '#fff', fontSize: '0.95rem' }}>{team.name}</strong>
                        <span className={`badge ${team.region === 'KR' ? 'badge-gold' : 'badge-cyan'}`} style={{ padding: '2px 6px', fontSize: '0.65rem' }}>
                          {team.league}
                        </span>
                      </div>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        로스터: {team.players ? team.players.map(p => p.nickname).join(', ') : '0명'}
                      </span>
                    </div>
                  </div>

                  <ChevronRight size={18} color={isSelected ? 'var(--accent-gold)' : 'var(--text-muted)'} />
                </div>
              );
            })}
          </div>
        </div>

      </div>
    </div>
  );
}
