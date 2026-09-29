import React, { useState } from 'react';
import { Search, Flame } from 'lucide-react';
import { TOURNAMENT_LOGOS } from '../../data/esportsData';
import LeagueTeamGrid from './LeagueTeamGrid';
import HotPlayerGrid from './HotPlayerGrid';

// 리그를 추가할 때는 이 배열에만 항목을 넣으면 된다.
// bannerTitle 이 있는 리그는 팀 목록 위에 대회 공식 명칭 배너를 띄운다.
// sourceUrl 은 데이터를 대조한 리퀴피디아 문서. 출처 표기(CC-BY-SA)에 쓰인다.
const LEAGUES = [
  {
    id: 'PWS',
    label: 'PWS',
    logo: TOURNAMENT_LOGOS.PWS,
    bannerTitle: '2026 PUBG WEEKLY SERIES: KOREA Phase 2',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_WEEKLY_SERIES/2026/Phase_2'
  },
  {
    id: 'PCL',
    label: 'PCL',
    logo: TOURNAMENT_LOGOS.PCL,
    bannerTitle: 'PUBG CHAMPIONS LEAGUE 2026: Autumn — Stage S',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_Champions_League/2026/Autumn'
  },
  {
    id: 'EMEA',
    label: 'EMEA',
    logo: TOURNAMENT_LOGOS.EMEA,
    bannerTitle: 'PUBG EMEA CHAMPIONSHIP: 2026 Fall',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_EMEA_Championship/2026/Fall'
  },
  {
    id: 'AMER',
    label: 'AMER',
    logo: TOURNAMENT_LOGOS.AMER,
    bannerTitle: 'PUBG AMERICAS SERIES 2 — 2026',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_Americas_Series/2026/2'
  },
  // APAC 은 태국(PTS)·베트남(PVS) 으로 나눴다. 각각 독립된 권역 리그다.
  { id: 'PTS', label: 'PTS', logo: TOURNAMENT_LOGOS.PTS },
  { id: 'PVS', label: 'PVS', logo: TOURNAMENT_LOGOS.PVS }
];

const HOT_CHIP = { id: 'HOT', label: 'HOT', icon: Flame };

export default function PlayersTab({ onSelectPlayer }) {
  const [selectedTab, setSelectedTab] = useState('PWS');
  const [searchQuery, setSearchQuery] = useState('');

  const chips = [HOT_CHIP, ...LEAGUES];
  const activeLeague = LEAGUES.find(l => l.id === selectedTab);

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
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {chips.map(chip => {
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
                    style={{ width: '20px', height: '20px', objectFit: 'contain' }}
                  />
                )}
                <span>{chip.label}</span>
              </button>
            );
          })}
        </div>

        <div style={{ position: 'relative', minWidth: '300px' }}>
          <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            placeholder={selectedTab === 'HOT' ? 'Search star player...' : 'Search team name or player...'}
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

      {selectedTab === 'HOT' ? (
        <HotPlayerGrid searchQuery={searchQuery} onSelectPlayer={onSelectPlayer} />
      ) : (
        <LeagueTeamGrid
          league={activeLeague.id}
          searchQuery={searchQuery}
          bannerLogo={activeLeague.logo}
          bannerTitle={activeLeague.bannerTitle}
          sourceUrl={activeLeague.sourceUrl}
          onSelectPlayer={onSelectPlayer}
        />
      )}
    </div>
  );
}
