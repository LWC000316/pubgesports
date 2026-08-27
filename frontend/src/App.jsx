import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import PlayerView from './components/PlayerView';
import PlayerDetailModal from './components/PlayerDetailModal';
import TournamentView from './components/TournamentView';
import StatsView from './components/StatsView';
import CrawlerPanel from './components/CrawlerPanel';

import {
  MOCK_PLAYERS,
  MOCK_PLAYER_DETAILS,
  MOCK_TOURNAMENTS,
  MOCK_PGS4_LEADERBOARD,
  MOCK_PGS4_STATS
} from './data/mockData';

export default function App() {
  const [activeTab, setActiveTab] = useState('players');
  const [players, setPlayers] = useState(MOCK_PLAYERS);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [tournaments, setTournaments] = useState(MOCK_TOURNAMENTS);
  const [leaderboards, setLeaderboards] = useState(MOCK_PGS4_LEADERBOARD);
  const [playerStats, setPlayerStats] = useState(MOCK_PGS4_STATS);
  const [isCrawlerOpen, setIsCrawlerOpen] = useState(false);

  // 백엔드 API에서 실제 데이터 가져오기 시도
  const fetchData = async () => {
    try {
      // 1. Players
      const resPlayers = await fetch('/api/players');
      if (resPlayers.ok) {
        const data = await resPlayers.json();
        if (data && data.length > 0) setPlayers(data);
      }

      // 2. Tournaments
      const resTournaments = await fetch('/api/tournaments');
      if (resTournaments.ok) {
        const data = await resTournaments.json();
        if (data && data.length > 0) setTournaments(data);
      }

      // 3. Tournament Leaderboard
      const resLeaderboard = await fetch('/api/tournaments/1/leaderboard');
      if (resLeaderboard.ok) {
        const data = await resLeaderboard.json();
        if (data && data.length > 0) setLeaderboards(data);
      }

      // 4. Tournament Stats
      const resStats = await fetch('/api/tournaments/1/stats');
      if (resStats.ok) {
        const data = await resStats.json();
        if (data && data.length > 0) setPlayerStats(data);
      }
    } catch (e) {
      console.log('Using local fallback mock data');
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 선수 클릭 시 상세 모달 열기
  const handleSelectPlayer = async (playerId) => {
    try {
      const res = await fetch(`/api/players/${playerId}`);
      if (res.ok) {
        const data = await res.json();
        setSelectedPlayer(data);
        return;
      }
    } catch (e) {}

    // Fallback Mock Detail
    const fallback = MOCK_PLAYER_DETAILS[playerId] || {
      ...players.find(p => p.id === playerId),
      setting: {
        mouseDpi: 800,
        generalSens: 30.0,
        aimingSens: 30.0,
        adsSens: 30.0,
        verticalMultiplier: 1.0,
        fov: 90,
        resolution: '1920x1080',
        screenMode: '전체 화면',
        renderScale: 100
      },
      gears: [
        { category: 'MOUSE', name: 'Logitech G PRO X SUPERLIGHT 2', brand: 'Logitech' },
        { category: 'MOUSEPAD', name: 'Artisan Ninja FX Zero Soft', brand: 'Artisan' },
        { category: 'KEYBOARD', name: 'Wooting 60HE', brand: 'Wooting' },
        { category: 'HEADSET', name: 'Sennheiser IE 200', brand: 'Sennheiser' },
        { category: 'MONITOR', name: 'BenQ ZOWIE XL2566K (360Hz)', brand: 'BenQ' }
      ],
      highlights: [
        { title: 'PGC 2023 매드무비', videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ' }
      ]
    };
    setSelectedPlayer(fallback);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Sticky Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenCrawler={() => setIsCrawlerOpen(true)}
      />

      {/* Main Content Area based on Tab */}
      <main style={{ flex: 1 }}>
        {activeTab === 'players' && (
          <PlayerView
            players={players}
            onSelectPlayer={handleSelectPlayer}
          />
        )}

        {activeTab === 'tournaments' && (
          <TournamentView
            tournaments={tournaments}
            leaderboards={leaderboards}
          />
        )}

        {activeTab === 'stats' && (
          <StatsView
            stats={playerStats}
          />
        )}
      </main>

      {/* Footer */}
      <footer style={{
        padding: '24px',
        textAlign: 'center',
        borderTop: '1px solid var(--border-subtle)',
        color: 'var(--text-dim)',
        fontSize: '0.8rem',
        marginTop: 'auto'
      }}>
        <p>PUBG PRO VAULT • eSports Analytics & Player Gear Archive • Inspired by Twire.gg</p>
        <p style={{ marginTop: '4px', fontSize: '0.75rem' }}>PLAYERUNKNOWN'S BATTLEGROUNDS is a registered trademark of KRAFTON, Inc.</p>
      </footer>

      {/* Player Detail Modal */}
      {selectedPlayer && (
        <PlayerDetailModal
          player={selectedPlayer}
          onClose={() => setSelectedPlayer(null)}
        />
      )}

      {/* Live Crawler Panel */}
      <CrawlerPanel
        isOpen={isCrawlerOpen}
        onClose={() => setIsCrawlerOpen(false)}
        onRefreshData={fetchData}
      />
    </div>
  );
}
