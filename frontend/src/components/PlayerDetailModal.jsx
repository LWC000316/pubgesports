import React, { useEffect, useState } from 'react';
import { X, Crosshair, Mouse, Monitor, Headphones, Keyboard, Video, ExternalLink, Calendar, CheckCircle2 } from 'lucide-react';
import { fetchPlayerDetail } from '../api/players';

const NOT_SET = '미등록';

const GEAR_CATEGORIES = ['MOUSE', 'MOUSEPAD', 'KEYBOARD', 'HEADSET', 'MONITOR'];

// 값이 없으면 null 을 돌려준다. 기본값을 지어내면 검증되지 않은 수치가
// 검증된 것처럼 보이므로 절대 대체값을 넣지 않는다.
const pick = (...values) => values.find(v => v !== undefined && v !== null && v !== '') ?? null;

function StatValue({ value, suffix = '', color = '#fff' }) {
  const missing = value === null;
  return (
    <div style={{
      fontSize: missing ? '0.95rem' : '1.1rem',
      fontWeight: '800',
      color: missing ? 'var(--text-muted)' : color,
      marginTop: '2px'
    }}>
      {missing ? NOT_SET : `${value}${suffix}`}
    </div>
  );
}

export default function PlayerDetailModal({ player, onClose }) {
  // 팀 카드가 넘겨주는 값은 dpi·sens·mouse 뿐이다. 나머지 감도와 장비는
  // /api/players/{id} 에만 있으므로 모달을 열 때 받아 와 덮어쓴다.
  // 실패하면 카드가 준 값만 그대로 쓴다 — 모달이 안 열리는 것보다 낫다.
  const [detail, setDetail] = useState(null);

  useEffect(() => {
    setDetail(null);
    if (!player?.id) return;
    let cancelled = false;
    fetchPlayerDetail(player.id)
      .then(d => { if (!cancelled) setDetail(d); })
      .catch(() => {});
    return () => { cancelled = true; };
  }, [player?.id]);

  if (!player) return null;

  const full = detail ?? player;
  const dpi = pick(full.setting?.mouseDpi, player.dpi);
  const generalSens = pick(full.setting?.generalSens, player.generalSens, player.sens);
  // 백엔드 SettingDto 는 aimingSens 로 내보낸다
  const aimSens = pick(full.setting?.aimingSens, full.setting?.aimSens, player.aimSens);
  const adsSens = pick(full.setting?.adsSens, player.adsSens);
  const verticalMultiplier = pick(full.setting?.verticalMultiplier, player.verticalMultiplier);
  const fov = pick(full.setting?.fov, player.fov);
  const resolution = pick(full.setting?.resolution, player.resolution);

  // 둘 다 있을 때만 합쳐 쓴다. 하나만 있으면 그 값만 보여주고 제목도 그에 맞춘다.
  // 예전에는 한쪽이 없으면 '? / 36' 처럼 물음표가 그대로 노출됐다.
  const aimAdsLabel = (aimSens !== null && adsSens !== null)
    ? '조준 / ADS 감도'
    : (aimSens !== null ? '조준 감도' : 'ADS 감도');
  const aimAds = (aimSens !== null && adsSens !== null)
    ? `${aimSens} / ${adsSens}`
    : (aimSens ?? adsSens);

  // 배율별 감도. 수집은 하는데 화면에 없으면 모은 값이 사라진 것과 같다.
  const scopes = [
    ['2배율', pick(full.setting?.scope2xSens)],
    ['3배율', pick(full.setting?.scope3xSens)],
    ['4배율', pick(full.setting?.scope4xSens)],
    ['6배율', pick(full.setting?.scope6xSens)],
    ['8배율', pick(full.setting?.scope8xSens)]
  ];
  const hasScopes = scopes.some(([, v]) => v !== null);

  // 5개 카테고리를 항상 노출한다. 비어 있는 항목이 보여야 무엇을 수집해야 하는지 드러난다.
  const gearByCategory = new Map(
    (full.gears ?? []).map(g => [g.category?.toUpperCase(), g.name])
  );
  const flatGear = {
    MOUSE: pick(player.mouseName, player.mouse),
    MOUSEPAD: pick(player.mousepad),
    KEYBOARD: pick(player.keyboard),
    HEADSET: pick(player.headset),
    MONITOR: pick(player.monitor)
  };
  const gears = GEAR_CATEGORIES.map(category => ({
    category,
    name: pick(gearByCategory.get(category), flatGear[category])
  }));

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
                <StatValue value={dpi} suffix=" DPI" />
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>일반 감도</div>
                <StatValue value={generalSens} color="var(--accent-cyan)" />
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{aimAdsLabel}</div>
                <StatValue value={aimAds} />
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>수직 배율 감도</div>
                <StatValue value={verticalMultiplier} />
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>시야각 (FOV)</div>
                <StatValue value={fov} />
              </div>

              <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>해상도</div>
                <StatValue value={resolution} />
              </div>
            </div>

            {hasScopes && (
              <div style={{ marginTop: '14px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
                  배율별 감도
                </div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '6px' }}>
                  {scopes.map(([label, value]) => (
                    <div key={label} style={{
                      background: 'rgba(255,255,255,0.03)',
                      padding: '10px 6px',
                      borderRadius: 'var(--radius-sm)',
                      textAlign: 'center'
                    }}>
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>{label}</div>
                      <div style={{
                        fontSize: value === null ? '0.75rem' : '0.95rem',
                        fontWeight: '800',
                        color: value === null ? 'var(--text-muted)' : '#fff',
                        marginTop: '2px'
                      }}>
                        {value === null ? NOT_SET : value}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
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
                    <div style={{
                      fontSize: '0.9rem',
                      color: g.name === null ? 'var(--text-muted)' : '#fff',
                      fontWeight: '700'
                    }}>
                      {g.name === null ? NOT_SET : g.name}
                    </div>
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
