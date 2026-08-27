import React from 'react';
import { Crosshair, Trophy, BarChart3, RefreshCw, Flame } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, onOpenCrawler }) {
  const tabs = [
    { id: 'players', label: 'PRO PLAYERS', icon: Crosshair, desc: '선수 세팅 & 장비' },
    { id: 'tournaments', label: 'TOURNAMENTS', icon: Trophy, desc: 'Twire 스타일 순위표' },
    { id: 'stats', label: 'LEADERBOARD', icon: BarChart3, desc: '선수 킬/딜 랭킹' },
  ];

  return (
    <header className="glass-panel" style={{
      margin: '20px 24px',
      padding: '16px 28px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottom: '1px solid var(--border-subtle)',
      position: 'sticky',
      top: '16px',
      zIndex: 100
    }}>
      {/* Brand Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', cursor: 'pointer' }} onClick={() => setActiveTab('players')}>
        <div style={{
          width: '42px',
          height: '42px',
          background: 'linear-gradient(135deg, #f3a61f 0%, #ff5200 100%)',
          borderRadius: 'var(--radius-sm)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: 'var(--shadow-glow)'
        }}>
          <Flame size={24} color="#0b0d13" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '1.4rem', fontWeight: '900', color: '#fff', letterSpacing: '1px' }}>PUBG PRO</span>
            <span style={{ fontSize: '1.4rem', fontWeight: '900', color: 'var(--accent-gold)' }}>VAULT</span>
            <span className="badge badge-gold">v1.0 eSports</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0, fontWeight: '500' }}>
            Pro Players Gear, In-Game Sens & Twire.gg Match Stats
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 18px',
                borderRadius: 'var(--radius-sm)',
                background: isActive ? 'rgba(243, 166, 31, 0.15)' : 'transparent',
                border: isActive ? '1px solid var(--border-active)' : '1px solid transparent',
                color: isActive ? 'var(--accent-gold)' : 'var(--text-muted)',
                fontWeight: '700',
                fontFamily: 'var(--font-display)',
                fontSize: '0.95rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              <Icon size={18} color={isActive ? 'var(--accent-gold)' : 'var(--text-muted)'} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Crawler & Sync Action Button */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button
          onClick={onOpenCrawler}
          className="btn-secondary"
          style={{ fontSize: '0.85rem', padding: '8px 14px' }}
          title="웹 크롤링 데이터 최신화 패널 열기"
        >
          <RefreshCw size={15} color="var(--accent-cyan)" />
          <span>DATA CRAWLER</span>
        </button>
      </div>
    </header>
  );
}
