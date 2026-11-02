import React, { useState } from 'react';
import { Flame, Shield, Trophy, Zap, Link2, Check } from 'lucide-react';
import { copyCurrentUrl } from '../hooks/useUrlState';

export default function Header({ activeTab, setActiveTab }) {
  const navTabs = [
    { id: 'pe', label: 'PE', icon: Shield },
    { id: 'tournaments', label: '대회', icon: Trophy },
    { id: 'hit_ending', label: '히트엔딩', icon: Zap }
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
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px', cursor: 'pointer' }} onClick={() => setActiveTab('pe')}>
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
            <span style={{ fontSize: '1.35rem', fontWeight: '900', color: '#fff', letterSpacing: '1px' }}>PUBG</span>
            <span style={{ fontSize: '1.35rem', fontWeight: '900', color: 'var(--accent-gold)' }}>ESPORTS</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0, fontWeight: '500' }}>
            Pro Analytics & Match Ending Archive
          </p>
        </div>
      </div>

      {/* 3대 네비게이션 탭: PE, 대회, 히트엔딩 */}
      <nav style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {navTabs.map((tab) => {
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
                padding: '10px 24px',
                borderRadius: 'var(--radius-sm)',
                background: isActive ? 'rgba(243, 166, 31, 0.16)' : 'transparent',
                border: isActive ? '1px solid var(--border-active)' : '1px solid transparent',
                color: isActive ? 'var(--accent-gold)' : 'var(--text-muted)',
                fontWeight: '800',
                fontSize: '0.95rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon size={18} color={isActive ? 'var(--accent-gold)' : 'var(--text-muted)'} />
              <span>{tab.label}</span>
            </button>
          );
        })}
        <ShareButton />
      </nav>
    </header>
  );
}

/**
 * 지금 보고 있는 화면의 링크를 복사한다.
 *
 * 고른 것이 주소에 적혀 있으므로(useUrlState) 이 링크 하나면 남이 같은
 * 대회·경기·맵을 연다. 복사됐는지 눈에 보여 줘야 해서 잠깐 표시를 바꾼다.
 */
function ShareButton() {
  const [done, setDone] = useState(false);
  return (
    <button
      onClick={async () => {
        const ok = await copyCurrentUrl();
        if (!ok) return;                 // 권한이 없으면 아무 말도 하지 않는다
        setDone(true);
        setTimeout(() => setDone(false), 1600);
      }}
      title="지금 화면의 링크 복사"
      style={{
        display: 'flex', alignItems: 'center', gap: '6px', marginLeft: '4px',
        padding: '8px 12px', borderRadius: 'var(--radius-sm)',
        background: done ? 'rgba(81, 207, 102, 0.15)' : 'rgba(255,255,255,0.04)',
        border: `1px solid ${done ? 'rgba(81,207,102,0.5)' : 'var(--border-subtle)'}`,
        color: done ? '#51cf66' : 'var(--text-muted)',
        cursor: 'pointer', fontSize: '0.82rem', fontWeight: 800
      }}>
      {done ? <Check size={16} /> : <Link2 size={16} />}
      <span>{done ? '복사됨' : '링크'}</span>
    </button>
  );
}
