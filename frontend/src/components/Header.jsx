import React from 'react';
import { Shield, Trophy, RefreshCw, Flame, ShieldPlus } from 'lucide-react';

export default function Header({ activeTab, setActiveTab, onOpenCrawler, onOpenAdmin }) {
  const tabs = [
    { id: 'teams', label: 'PUBG ESPORTS', icon: Shield, desc: '권역별 프로팀 & 선수 로스터' },
    { id: 'tournaments', label: 'TOURNAMENTS', icon: Trophy, desc: '공식 세계 대회 및 권역 리그' }
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
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', cursor: 'pointer' }} onClick={() => setActiveTab('teams')}>
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
            <span className="badge badge-gold">Official API</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0, fontWeight: '500' }}>
            Official Tournaments, Regional Rosters & 15-Step Sensitivity System
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
                padding: '10px 20px',
                borderRadius: 'var(--radius-sm)',
                background: isActive ? 'rgba(243, 166, 31, 0.18)' : 'transparent',
                border: isActive ? '1px solid var(--border-active)' : '1px solid transparent',
                color: isActive ? 'var(--accent-gold)' : 'var(--text-muted)',
                fontWeight: '800',
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

      {/* Action Buttons (Admin & Sync) */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <button
          onClick={onOpenAdmin}
          className="btn-primary"
          style={{ fontSize: '0.8rem', padding: '7px 12px' }}
          title="관리자: 팀/선수 데이터 등록 및 편집"
        >
          <ShieldPlus size={15} />
          <span>ADMIN MANAGE</span>
        </button>

        <button
          onClick={onOpenCrawler}
          className="btn-secondary"
          style={{ fontSize: '0.8rem', padding: '7px 12px' }}
          title="공식 데이터 동기화 패널"
        >
          <RefreshCw size={14} color="var(--accent-cyan)" />
          <span>API SYNC</span>
        </button>
      </div>
    </header>
  );
}
