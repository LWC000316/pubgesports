import React, { useState } from 'react';
import Header from './components/Header';
import PlayersTab from './components/PlayersTab';
import TournamentsTab from './components/TournamentsTab';
import HitEndingTab from './components/HitEndingTab';
import PlayerDetailModal from './components/PlayerDetailModal';

export default function App() {
  const [activeTab, setActiveTab] = useState('pe');
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)', color: 'var(--text-main)' }}>
      {/* 상단 헤더: PE, 대회, 히트엔딩 탭 전환 */}
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* 메인 뷰 영역 */}
      <main style={{ maxWidth: '1440px', margin: '0 auto' }}>
        {activeTab === 'pe' && (
          <PlayersTab
            onSelectPlayer={(p) => setSelectedPlayer(p)}
          />
        )}

        {activeTab === 'tournaments' && (
          <TournamentsTab />
        )}

        {activeTab === 'hit_ending' && (
          <HitEndingTab />
        )}
      </main>

      {/* 선수 상세 프로필 모달 */}
      {selectedPlayer && (
        <PlayerDetailModal
          player={selectedPlayer}
          onClose={() => setSelectedPlayer(null)}
        />
      )}
    </div>
  );
}
