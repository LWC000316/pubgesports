import React from 'react';
import { X, Crosshair, Mouse, Monitor, Headphones, Keyboard, Video, ExternalLink, Calendar, CheckCircle2 } from 'lucide-react';

export default function PlayerDetailModal({ player, onClose }) {
  if (!player) return null;

  const setting = player.setting || {};
  const gears = player.gears || [];
  const highlights = player.highlights || [];

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
          width: '900px',
          maxWidth: '95vw',
          maxHeight: '90vh',
          overflowY: 'auto',
          padding: '32px',
          border: '1px solid var(--border-active)',
          boxShadow: 'var(--shadow-glow)',
          position: 'relative'
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
        <div style={{ display: 'flex', gap: '24px', alignItems: 'center', marginBottom: '28px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '24px' }}>
          <div style={{
            width: '100px',
            height: '100px',
            borderRadius: 'var(--radius-md)',
            overflow: 'hidden',
            border: '2px solid var(--accent-gold)',
            boxShadow: 'var(--shadow-glow)',
            flexShrink: 0
          }}>
            <img src={player.profileImageUrl} alt={player.nickname} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>

          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
              <h2 style={{ fontSize: '2rem', color: '#fff', margin: 0, fontWeight: '900' }}>{player.nickname}</h2>
              <span className="badge badge-gold">{player.team?.name || 'FREE AGENT'}</span>
              <span className="badge badge-cyan">{player.role || 'PRO PLAYER'}</span>
              {player.lastCrawledAt && (
                <span className="badge badge-green" style={{ fontSize: '0.65rem' }}>
                  <CheckCircle2 size={12} /> CRAWLED VERIFIED
                </span>
              )}
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', margin: '4px 0 12px' }}>{player.realName} • {player.country} 🇰🇷</p>

            {/* Social / Broadcast Links */}
            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
              {player.youtubeUrl && (
                <a href={player.youtubeUrl} target="_blank" rel="noreferrer" className="btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
                  유튜브 채널 <ExternalLink size={12} />
                </a>
              )}
              {player.chzzkUrl && (
                <a href={player.chzzkUrl} target="_blank" rel="noreferrer" className="btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem', borderColor: 'var(--accent-green)' }}>
                  치지직 방송 <ExternalLink size={12} />
                </a>
              )}
              {player.soopUrl && (
                <a href={player.soopUrl} target="_blank" rel="noreferrer" className="btn-secondary" style={{ padding: '4px 10px', fontSize: '0.75rem', borderColor: 'var(--accent-cyan)' }}>
                  SOOP 방송 <ExternalLink size={12} />
                </a>
              )}
            </div>
          </div>
        </div>

        {/* 2-Column Grid: Left (Settings) / Right (Gear & Highlights) */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px' }}>
          {/* Left Column: In-Game Settings */}
          <div className="glass-panel" style={{ padding: '20px', background: 'rgba(15, 20, 30, 0.7)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
              <Crosshair size={20} color="var(--accent-gold)" />
              <h3 style={{ fontSize: '1.1rem', color: 'var(--accent-gold)', margin: 0 }}>인게임 감도 & 디스플레이 설정</h3>
            </div>

            {/* Settings Table / Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>마우스 DPI</span>
                <p style={{ fontSize: '1.2rem', fontWeight: '800', color: '#fff', margin: '2px 0 0' }}>{setting.mouseDpi || 800} DPI</p>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>일반 감도</span>
                <p style={{ fontSize: '1.2rem', fontWeight: '800', color: 'var(--accent-gold)', margin: '2px 0 0' }}>{setting.generalSens || 30}</p>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>조준 / ADS 스코프 감도</span>
                <p style={{ fontSize: '1.1rem', fontWeight: '700', color: '#fff', margin: '2px 0 0' }}>{setting.aimingSens || 30} / {setting.adsSens || 30}</p>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>수직 감도 배율</span>
                <p style={{ fontSize: '1.1rem', fontWeight: '700', color: 'var(--accent-cyan)', margin: '2px 0 0' }}>{setting.verticalMultiplier || 1.0}x</p>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>1인칭 시야각 (FOV)</span>
                <p style={{ fontSize: '1.1rem', fontWeight: '700', color: '#fff', margin: '2px 0 0' }}>{setting.fov || 90}</p>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: 'var(--radius-sm)' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>인게임 해상도</span>
                <p style={{ fontSize: '1rem', fontWeight: '700', color: '#fff', margin: '2px 0 0' }}>{setting.resolution || '1920x1080'}</p>
              </div>
            </div>

            {/* PUBG 15-Step Equivalent Sens Banner */}
            <div style={{ background: 'rgba(243, 166, 31, 0.08)', border: '1px solid var(--border-active)', padding: '14px', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--accent-gold)', fontWeight: '800' }}>
                  PUBG 15스텝 동등 감도 환산
                </span>
                <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                  DPI 2배 증가 시 감도 15 감소
                </span>
              </div>

              {/* 400 / 800 / 1600 DPI 기준 감도 계산 */}
              {(() => {
                const currentDpi = setting.mouseDpi || 800;
                const gen = setting.generalSens || 30.0;
                
                let sens400 = gen;
                let sens800 = gen;
                let sens1600 = gen;

                if (currentDpi === 400) {
                  sens400 = gen;
                  sens800 = Math.max(0, gen - 15);
                  sens1600 = Math.max(0, gen - 30);
                } else if (currentDpi === 800) {
                  sens400 = gen + 15;
                  sens800 = gen;
                  sens1600 = Math.max(0, gen - 15);
                } else if (currentDpi === 1600) {
                  sens400 = gen + 30;
                  sens800 = gen + 15;
                  sens1600 = gen;
                } else {
                  // 임의 DPI일 때 800 기준 근사치
                  sens400 = Math.round(gen * (currentDpi / 400));
                  sens800 = Math.round(gen * (currentDpi / 800));
                  sens1600 = Math.round(gen * (currentDpi / 1600));
                }

                return (
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px', textAlign: 'center' }}>
                    <div style={{ background: currentDpi === 400 ? 'rgba(243, 166, 31, 0.2)' : 'rgba(255,255,255,0.03)', padding: '6px', borderRadius: '4px' }}>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>400 DPI</span>
                      <strong style={{ display: 'block', color: '#fff', fontSize: '0.95rem' }}>{sens400}</strong>
                    </div>
                    <div style={{ background: currentDpi === 800 ? 'rgba(243, 166, 31, 0.2)' : 'rgba(255,255,255,0.03)', padding: '6px', borderRadius: '4px' }}>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>800 DPI</span>
                      <strong style={{ display: 'block', color: 'var(--accent-gold)', fontSize: '0.95rem' }}>{sens800}</strong>
                    </div>
                    <div style={{ background: currentDpi === 1600 ? 'rgba(243, 166, 31, 0.2)' : 'rgba(255,255,255,0.03)', padding: '6px', borderRadius: '4px' }}>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>1600 DPI</span>
                      <strong style={{ display: 'block', color: '#fff', fontSize: '0.95rem' }}>{sens1600}</strong>
                    </div>
                  </div>
                );
              })()}
            </div>
          </div>

          {/* Right Column: Gear Rack & Highlights */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {/* Gear Rack */}
            <div className="glass-panel" style={{ padding: '20px', background: 'rgba(15, 20, 30, 0.7)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                <Mouse size={20} color="var(--accent-cyan)" />
                <h3 style={{ fontSize: '1.1rem', color: 'var(--accent-cyan)', margin: 0 }}>사용 장비 (GEAR)</h3>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {gears.map((gear) => (
                  <div key={gear.id || gear.name} style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border-subtle)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      {getGearIcon(gear.category)}
                      <div>
                        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', display: 'block' }}>{gear.category}</span>
                        <strong style={{ fontSize: '0.85rem', color: '#fff' }}>{gear.name}</strong>
                      </div>
                    </div>
                    {gear.brand && <span className="badge badge-gold" style={{ fontSize: '0.65rem' }}>{gear.brand}</span>}
                  </div>
                ))}
              </div>
            </div>

            {/* Highlights Video Embed */}
            {highlights.length > 0 && (
              <div className="glass-panel" style={{ padding: '20px', background: 'rgba(15, 20, 30, 0.7)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                  <Video size={20} color="var(--accent-red)" />
                  <h3 style={{ fontSize: '1.1rem', color: '#fff', margin: 0 }}>대회 하이라이트 영상</h3>
                </div>
                <div style={{ borderRadius: 'var(--radius-sm)', overflow: 'hidden', border: '1px solid var(--border-subtle)', aspectRatio: '16/9' }}>
                  <iframe
                    src={highlights[0].videoUrl}
                    title={highlights[0].title}
                    style={{ width: '100%', height: '100%', border: 'none' }}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
