import React, { useState } from 'react';
import { Search, Flame } from 'lucide-react';
import { TOURNAMENT_LOGOS } from '../../data/esportsData';
import LeagueTeamGrid from './LeagueTeamGrid';
import HotPlayerGrid from './HotPlayerGrid';

// 리그를 추가할 때는 이 배열에만 항목을 넣으면 된다.
// bannerTitle 이 있는 리그는 팀 목록 위에 대회 공식 명칭 배너를 띄운다.
// sourceUrl 은 데이터를 대조한 리퀴피디아 문서. 출처 표기(CC-BY-SA)에 쓰인다.
//
// 팀 목록은 구획을 나누지 않고 한 줄기로 늘어놓는다. 프로로 볼 수 있는 구단이
// 앞에 오고 그 뒤로 아마추어 구단이 이어진다 — 순서는 seedType 이 정한다
// (LeagueTeamGrid 의 SEED_ORDER). 리그마다 '프로'의 근거가 달라서 구획 제목을
// 붙이면 어느 리그에서는 반드시 사실과 어긋나므로 제목 없이 순서로만 구분한다.
const LEAGUES = [
  {
    id: 'PWS',
    label: 'PWS',
    logo: TOURNAMENT_LOGOS.PWS,
    bannerTitle: '2026 PUBG WEEKLY SERIES: KOREA Phase 2',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_WEEKLY_SERIES/2026/Phase_2',
    // 상단 13팀: 위키가 text=Pro Seed 로 직접 표기한 팀.
  },
  {
    id: 'PCL',
    label: 'PCL',
    logo: TOURNAMENT_LOGOS.PCL,
    bannerTitle: 'PUBG CHAMPIONS LEAGUE 2026: Autumn — Stage S',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_Champions_League/2026/Autumn',
    // 상단 8팀: Stage S 직행 시드. 나머지 16팀은 Stage A 에서 올라왔다.
    // 위키에는 invite 가 없어 seed_types_pcl.json 에 사람이 확정한 값이다.
  },
  {
    id: 'EMEA',
    label: 'EMEA',
    logo: TOURNAMENT_LOGOS.EMEA,
    bannerTitle: 'PUBG EMEA CHAMPIONSHIP: 2026 Fall',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_EMEA_Championship/2026/Fall',
    // 상단 9팀: Global Partner 3 · Regional Partner 5 · PGS Attending 1.
  },
  {
    id: 'AMER',
    label: 'AMER',
    logo: TOURNAMENT_LOGOS.AMER,
    bannerTitle: 'PUBG AMERICAS SERIES 2 — 2026',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_Americas_Series/2026/2',
    // 상단 7팀: Global Partner 1 · Regional Partner 5 · PGS Attending 1.
  },
  // APAC 은 태국(PTS)·베트남(PVS) 으로 나눴다. 각각 독립된 권역 리그다.
  {
    id: 'PTS',
    label: 'PTS',
    logo: TOURNAMENT_LOGOS.PTS,
    bannerTitle: 'PUBG THAILAND SERIES 2026 — Phase 2',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_Thailand_Series/2026/Phase_2',
    // 위키가 {{Qualification|method=invite}} 로만 적어 프로/아마 근거가 원문에
    // 없다. 현재 순서는 invite 18팀이 앞, 예선 통과 6팀이 뒤일 뿐이다.
  },
  {
    id: 'PVS',
    label: 'PVS',
    logo: TOURNAMENT_LOGOS.PVS,
    bannerTitle: 'PUBG VIETNAM SERIES 2026 — Phase 2',
    sourceUrl: 'https://liquipedia.net/pubg/PUBG_Vietnam_Series/2026/Phase_2',
    // 상단 3팀: Phase 1 파이널 1~3위. 나머지는 PVS Cup 포인트 1~13위.
  }
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
