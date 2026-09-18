import React, { useState, useEffect, useCallback } from 'react';
import { Search, Shield, Mouse, ChevronRight, Flame, Trophy, Crown, Target, AlertTriangle, RefreshCw } from 'lucide-react';
import { HOT_PLAYERS_12, TOURNAMENT_LOGOS } from '../data/esportsData';

export default function PlayersTab({ onSelectPlayer }) {
  const [selectedTab, setSelectedTab] = useState('PWS');
  const [searchQuery, setSearchQuery] = useState('');

  // PWS 팀 목록은 백엔드에서 가져온다 (vite 프록시가 localhost:8080 으로 넘김)
  const [pwsTeams, setPwsTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadPwsTeams = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/teams/cards?league=PWS');
      if (!res.ok) {
        throw new Error(`서버가 ${res.status} ${res.statusText} 로 응답했습니다.`);
      }
      setPwsTeams(await res.json());
    } catch (e) {
      setError(e.message || '알 수 없는 오류');
      setPwsTeams([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPwsTeams();
  }, [loadPwsTeams]);

  const filterChips = [
    { id: 'HOT', label: 'HOT', icon: Flame, desc: '인기 스타 선수 TOP 12' },
    { id: 'PWS', label: 'PWS', logo: TOURNAMENT_LOGOS.PWS, desc: 'PUBG WEEKLY SERIES KOREA' },
    { id: 'PCL', label: 'PCL', logo: TOURNAMENT_LOGOS.PCL, desc: 'PUBG Champions League' },
    { id: 'EMEA', label: 'EMEA', logo: TOURNAMENT_LOGOS.EMEA, desc: 'PUBG EMEA Championship' },
    { id: 'AMER', label: 'AMER', logo: TOURNAMENT_LOGOS.AMER, desc: 'PUBG Americas Series' },
    { id: 'APAC', label: 'APAC', logo: TOURNAMENT_LOGOS.APAC, desc: 'PUBG Asia Pacific' }
  ];

  // PWS 탭: 검색어 필터링 (API 응답에는 누락 필드가 있을 수 있어 옵셔널 체이닝 필수)
  const filteredTeams = pwsTeams.filter(t => {
    const q = searchQuery.toLowerCase();
    const matchesTeamName =
      t.name?.toLowerCase().includes(q) || t.tag?.toLowerCase().includes(q);
    const matchesRoster = t.roster?.some(p => p.nickname?.toLowerCase().includes(q));
    return matchesTeamName || matchesRoster;
  });

  // 프로 시드와 퀄리파이어 시드 분리
  const proTeams = filteredTeams.filter(t => t.seedType === 'pro');
  const qualifierTeams = filteredTeams.filter(t => t.seedType === 'amateur');

  // HOT 탭: 선수 필터링
  const filteredHotPlayers = HOT_PLAYERS_12.filter(p => {
    const q = searchQuery.toLowerCase();
    return p.nickname?.toLowerCase().includes(q) || p.realName?.includes(q) || p.team?.toLowerCase().includes(q);
  });

  // 팀 카드 렌더러 함수
  const renderTeamCard = (team) => {
    const hasTrophies = team.trophies && team.trophies.length > 0;

    return (
      <div
        key={team.id}
        className="glass-panel"
        style={{
          padding: '20px',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          transition: 'all 0.2s ease',
          background: 'rgba(22, 26, 38, 0.75)'
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
        {/* 팀 헤더: 공식 로고 + 팀명 + 우승 트로피 뱃지 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          {/* 팀 로고 박스 */}
          <div style={{
            width: '54px',
            height: '54px',
            borderRadius: '10px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            overflow: 'hidden',
            flexShrink: 0,
            padding: '4px'
          }}>
            {team.logo ? (
              <img
                src={team.logo}
                alt={team.name}
                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                onError={(e) => {
                  e.target.style.display = 'none';
                  const fb = e.target.nextElementSibling;
                  if (fb) fb.style.display = 'flex';
                }}
              />
            ) : null}
            <div style={{
              display: team.logo ? 'none' : 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '100%',
              height: '100%',
              fontWeight: '900',
              fontSize: '1rem',
              color: 'var(--accent-gold)'
            }}>
              {team.tag}
            </div>
          </div>

          {/* 팀명 및 우승 트로피 목록 */}
          <div style={{ overflow: 'hidden', flex: 1 }}>
            <div style={{
              fontSize: '1.15rem',
              fontWeight: '900',
              color: '#fff',
              letterSpacing: '0.02em',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            }}>
              {team.name}
            </div>

            {/* 우승 트로피 라인 */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              flexWrap: 'wrap',
              marginTop: '4px'
            }}>
              {hasTrophies ? (
                team.trophies.map((trophy, tIdx) => (
                  <div
                    key={tIdx}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '3px',
                      background: 'rgba(243, 166, 31, 0.12)',
                      border: '1px solid rgba(243, 166, 31, 0.3)',
                      padding: '2px 7px',
                      borderRadius: '4px',
                      fontSize: '0.72rem',
                      fontWeight: '800',
                      color: 'var(--accent-gold)'
                    }}
                  >
                    <Trophy size={11} color="var(--accent-gold)" />
                    <span>{trophy.name}</span>
                    <span style={{ fontSize: '0.68rem', opacity: 0.9 }}>x{trophy.count}</span>
                  </div>
                ))
              ) : (
                <div style={{
                  fontSize: '0.72rem',
                  color: 'rgba(255, 255, 255, 0.3)',
                  fontWeight: '700',
                  letterSpacing: '0.05em'
                }}>
                  CHALLENGER
                </div>
              )}
            </div>
          </div>
        </div>

        {/* 공식 로스터 4인 카드 목록 */}
        <div style={{
          borderTop: '1px solid rgba(255, 255, 255, 0.06)',
          paddingTop: '14px'
        }}>
          <div style={{
            fontSize: '0.72rem',
            color: 'var(--text-muted)',
            marginBottom: '8px',
            fontWeight: '800',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
          }}>
            Official Roster
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
            {(team.roster ?? []).map((player) => (
              <div
                key={player.id ?? player.nickname}
                onClick={() => onSelectPlayer && onSelectPlayer({
                  ...player,
                  team: team.name,
                  league: team.league,
                  country: team.region,
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
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                  {player.role}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

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
        {/* 권역 탭 칩: HOT, PWS, PCL, EMEA, AMER, APAC */}
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
                  gap: '8px',
                  padding: '9px 18px',
                  borderRadius: 'var(--radius-sm)',
                  background: isActive ? 'var(--accent-gold)' : 'rgba(255, 255, 255, 0.04)',
                  color: isActive ? '#000' : 'var(--text-muted)',
                  border: isActive ? '1px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                  fontWeight: '900',
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                {Icon && <Icon size={16} color={isActive ? '#000' : 'var(--accent-gold)'} />}
                {chip.logo && (
                  <img
                    src={chip.logo}
                    alt={chip.label}
                    style={{
                      width: '20px',
                      height: '20px',
                      objectFit: 'contain'
                    }}
                  />
                )}
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
            placeholder={selectedTab === 'PWS' ? "Search team name or player..." : "Search star player..."}
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

      {/* PWS 로딩 중 */}
      {selectedTab === 'PWS' && loading && (
        <div className="glass-panel" style={{
          padding: '60px 24px',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center',
          border: '1px solid var(--border-subtle)'
        }}>
          <RefreshCw
            size={36}
            color="var(--accent-gold)"
            style={{ marginBottom: '16px', animation: 'pulseGlow 1.4s ease-in-out infinite' }}
          />
          <div style={{ fontWeight: '900', color: '#fff', fontSize: '1rem', marginBottom: '6px' }}>
            공식 로스터를 불러오는 중입니다
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            백엔드 서버에서 PWS 팀 데이터를 가져오고 있습니다.
          </div>
        </div>
      )}

      {/* PWS 로드 실패 */}
      {selectedTab === 'PWS' && !loading && error && (
        <div className="glass-panel" style={{
          padding: '60px 24px',
          borderRadius: 'var(--radius-md)',
          textAlign: 'center',
          border: '1px solid rgba(255, 51, 75, 0.35)',
          background: 'linear-gradient(135deg, rgba(255, 51, 75, 0.1) 0%, rgba(22, 26, 38, 0.95) 100%)'
        }}>
          <AlertTriangle size={36} color="#ff334b" style={{ marginBottom: '16px' }} />
          <div style={{ fontWeight: '900', color: '#fff', fontSize: '1rem', marginBottom: '8px' }}>
            팀 데이터를 불러오지 못했습니다
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
            {error}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '20px' }}>
            백엔드 서버(localhost:8080)와 PostgreSQL 컨테이너가 실행 중인지 확인해 주세요.
          </div>
          <button
            onClick={loadPwsTeams}
            style={{
              padding: '10px 22px',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--accent-gold)',
              color: '#000',
              border: 'none',
              fontWeight: '800',
              fontSize: '0.85rem',
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <RefreshCw size={15} />
            다시 시도
          </button>
        </div>
      )}

      {/* 1. PWS 선택 시: 공식 프로 시드와 퀄리파이어 시드 분리 뷰 */}
      {selectedTab === 'PWS' && !loading && !error && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '36px' }}>
          
          {/* 대회 공식 명칭 헤더 배너 */}
          <div className="glass-panel" style={{
            padding: '16px 22px',
            borderRadius: 'var(--radius-sm)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '12px',
            border: '1px solid rgba(243, 166, 31, 0.3)',
            background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.1) 0%, rgba(22, 26, 38, 0.95) 100%)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <img
                src={TOURNAMENT_LOGOS.PWS}
                alt="PWS"
                style={{ width: '28px', height: '28px', objectFit: 'contain' }}
              />
              <span style={{ fontWeight: '900', color: '#fff', fontSize: '1.1rem', letterSpacing: '0.02em' }}>
                2026 PUBG WEEKLY SERIES: KOREA Phase 2
              </span>
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <span className="badge badge-gold" style={{ fontSize: '0.75rem', fontWeight: '800' }}>
                {proTeams.length} PRO SEEDS
              </span>
              <span className="badge" style={{ fontSize: '0.75rem', fontWeight: '800', background: 'rgba(255,255,255,0.08)', color: '#fff' }}>
                {qualifierTeams.length} QUALIFIER SEEDS
              </span>
            </div>
          </div>

          {/* 1) 프로 시드 섹션 */}
          <div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              marginBottom: '16px',
              paddingBottom: '8px',
              borderBottom: '1px solid rgba(243, 166, 31, 0.3)'
            }}>
              <Crown size={20} color="var(--accent-gold)" />
              <h2 style={{
                fontSize: '1.1rem',
                fontWeight: '900',
                color: '#fff',
                margin: 0,
                letterSpacing: '0.05em',
                textTransform: 'uppercase'
              }}>
                Pro Seeds ({proTeams.length})
              </h2>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
              gap: '20px'
            }}>
              {proTeams.map(team => renderTeamCard(team))}
            </div>
          </div>

          {/* 2) 퀄리파이어 시드 섹션 */}
          <div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              marginBottom: '16px',
              paddingBottom: '8px',
              borderBottom: '1px solid rgba(255, 255, 255, 0.15)'
            }}>
              <Target size={20} color="#00e5ff" />
              <h2 style={{
                fontSize: '1.1rem',
                fontWeight: '900',
                color: '#fff',
                margin: 0,
                letterSpacing: '0.05em',
                textTransform: 'uppercase'
              }}>
                Qualifier Seeds ({qualifierTeams.length})
              </h2>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
              gap: '20px'
            }}>
              {qualifierTeams.map(team => renderTeamCard(team))}
            </div>
          </div>

        </div>
      )}

      {/* 2. HOT 선택 시: 스타 선수 12명 뷰 */}
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
              HOT STAR PLAYERS (TOP 12)
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
      )}

      {/* 3. 기타 권역 준비 중 안내 */}
      {selectedTab !== 'PWS' && selectedTab !== 'HOT' && (
        <div className="glass-panel" style={{ padding: '60px 20px', textAlign: 'center' }}>
          <Shield size={36} color="var(--accent-gold)" style={{ margin: '0 auto 16px auto' }} />
          <h3 style={{ fontSize: '1.2rem', color: '#fff', marginBottom: '8px' }}>
            {selectedTab} Official Roster Coming Soon
          </h3>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
            Official rosters and tournament metadata for {selectedTab} are currently being synchronized.
          </p>
        </div>
      )}
    </div>
  );
}
