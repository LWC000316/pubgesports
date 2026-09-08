import React from 'react';
import { X, Crosshair, Mouse, Monitor, Headphones, Keyboard, Video, ExternalLink, Calendar, CheckCircle2 } from 'lucide-react';

export default function PlayerDetailModal({ player, onClose }) {
  if (!player) return null;

  const dpi = player.setting?.mouseDpi || player.dpi || 800;
  const generalSens = player.setting?.generalSens || player.generalSens || 30;
  const aimSens = player.setting?.aimSens || player.aimSens || 30;
  const adsSens = player.setting?.adsSens || player.adsSens || 30;
  const verticalMultiplier = player.setting?.verticalMultiplier || player.verticalMultiplier || 1.0;
  const fov = player.setting?.fov || player.fov || 103;
  const resolution = player.setting?.resolution || player.resolution || '1920 x 1080';

  const gears = player.gears || [
    { category: 'MOUSE', name: player.mouseName || '로지텍 G PRO X Superlight', brand: 'Logitech' },
    { category: 'MOUSEPAD', name: player.mousepad || '아티산 제로 XSoft', brand: 'Artisan' },
    { category: 'KEYBOARD', name: player.keyboard || '우팅 60HE', brand: 'Wooting' },
    { category: 'HEADSET', name: player.headset || '보스 QC20', brand: 'Bose' },
    { category: 'MONITOR', name: player.monitor || '조위 XL2546K', brand: 'ZOWIE' }
  ];

  const getGearIcon = (category) => {
    switch (category.toUpperCase()) {
      case 'MOUSE': return <Mouse size={18} color="var(--accent-gold)" />;
      case 'MOUSEPAD': return <Crosshair size={18} color="var(--accent-cyan)" />;
      case 'KEYBOARD': return <Keyboard size={18} color="var(--accent-green)" />;
      case 'HEADSET':
      case 'EARPHONE': return <Headphones size={18} color="var(--accent-red)" />;
      case 'MONITOR': return <Monitor size={18} color="#c084fc" />;
      default: return <Mouse size={18} color="var(--accent-gold)" />;
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(5, 7, 11, 0.85)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }} onClick={onClose}>
      <div
        className="glass-panel animate-fade-in"
        style={{
          width: '840px',
          maxWidth: '95vw',
          maxHeight: '90vh',
          overflowY: 'auto',
          padding: '30px',
          border: '1px solid var(--border-active)',
          boxShadow: 'var(--shadow-glow)',
          position: 'relative',
          borderRadius: 'var(--radius-md)'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(255, 255, 255, 0.1)',
            border: 'none',
            borderRadius: '50%',
            width: '36px',
            height: '36px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            cursor: 'pointer',
            transition: 'all 0.2s'
          }}
        >
          <X size={20} />
        </button>

        {/* Player Header Banner */}
        <div style={{ display: 'flex', gap: '20px', alignItems: 'center', marginBottom: '24px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '20px' }}>
          <div style={{
            width: '72px',
            height: '72px',
            borderRadius: '50%',
            background: 'rgba(243, 166, 31, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.8rem',
            fontWeight: '900',
            color: 'var(--accent-gold)',
            flexShrink: 0
          }}>
            {player.nickname?.[0] || 'P'}
          </div>

          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
              <h2 style={{ fontSize: '1.8rem', color: '#fff', margin: 0, fontWeight: '900' }}>{player.nickname}</h2>
              <span className="badge badge-gold">{player.team?.name || player.team || '프로팀'}</span>
              <span className="badge badge-cyan">{player.role || 'PRO PLAYER'}</span>
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: '4px 0 0' }}>
              {player.realName} • {player.country} • {player.league}
            </p>
          </div>
        </div>

        {/* 2-Column Grid: Left (Settings) / Right (Gear) */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '20px' }}>
          {/* Left Column: In-Game Settings */}
          <div className="glass-panel" style={{ padding: '20px', background: 'rgba(15, 20, 30, 0.7)', borderRadius: 'var(--radius-sm)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <Crosshair size={18} color="var(--accent-gold)" />
              <h3 style={{ fontSize: '1.05rem', color: 'var(--accent-gold)', margin: 0 }}>인게임 감도 및 화면 설정</h3>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>마우스 DPI</div>
                <div style={{ fontSize: '1.2rem', fontWeight: '800', color: '#fff', marginTop: '2px' }}>{dpi} DPI</div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>일반 감도</div>
                <div style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-cyan)', marginTop: '2px' }}>{generalSens}</div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>조준 / ADS 감도</div>
                <div style={{ fontSize: '1.1rem', fontWeight: '800', color: '#fff', marginTop: '2px' }}>{aimSens} / {adsSens}</div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>수직 배율 감도</div>
                <div style={{ fontSize: '1.1rem', fontWeight: '800', color: '#fff', marginTop: '2px' }}>{verticalMultiplier}</div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>시야각 (FOV)</div>
                <div style={{ fontSize: '1.1rem', fontWeight: '800', color: '#fff', marginTop: '2px' }}>{fov}</div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>해상도</div>
                <div style={{ fontSize: '1rem', fontWeight: '800', color: '#fff', marginTop: '2px' }}>{resolution}</div>
              </div>
            </div>
          </div>

          {/* Right Column: Gear */}
          <div className="glass-panel" style={{ padding: '20px', background: 'rgba(15, 20, 30, 0.7)', borderRadius: 'var(--radius-sm)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <Mouse size={18} color="var(--accent-gold)" />
              <h3 style={{ fontSize: '1.05rem', color: 'var(--accent-gold)', margin: 0 }}>사용 장비 (Gear)</h3>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {gears.map((g, index) => (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px 14px',
                    background: 'rgba(255,255,255,0.02)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(255,255,255,0.04)'
                  }}
                >
                  <div style={{ width: '28px' }}>
                    {getGearIcon(g.category)}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{g.category}</div>
                    <div style={{ fontSize: '0.9rem', color: '#fff', fontWeight: '700' }}>{g.name}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
