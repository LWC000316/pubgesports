import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Crosshair, Plane, Skull, Target, Info } from 'lucide-react';
import { fetchHeatMaps, fetchHeat } from '../api/tournaments';
import { useApi } from '../hooks/useApi';
import LoadingPanel from './common/LoadingPanel';
import ErrorPanel from './common/ErrorPanel';

/**
 * 히트엔딩 — **한 경기 복기가 아니라 여러 경기를 모아 본 것**이다.
 *
 * 매치로그는 한 경기를 되감는다. 여기서 보려는 것은 한 경기로는 절대 안 보이는
 * 것이다: 이 맵은 어디서 끝나는가, 어디로 내리는가, 어디서 죽는가.
 * 집계는 `ingest/build_heat.py` 가 맵마다 50x50 격자에 쌓아 둔다.
 *
 * **경기 수를 늘 같이 보여 준다.** 1,198경기짜리 에란겔과 표본이 적은 맵을
 * 같은 무게로 읽으면 거짓이 되기 때문이다. 표본이 20경기에 못 미치는 맵은
 * 집계 자체를 하지 않는다.
 */
const SIZE = 1000;

const LAYERS = [
  { key: 'ending', label: '엔딩', icon: Target,
    hint: '마지막 자기장의 중심. 이 맵이 어디서 끝나는가.',
    color: [243, 166, 31] },
  { key: 'landing', label: '낙하', icon: Plane,
    hint: '착지 지점. 어디로 내리는가.',
    color: [0, 229, 255] },
  { key: 'death', label: '사망', icon: Skull,
    hint: '죽은 자리. 어디서 싸우다 죽는가.',
    color: [255, 77, 109] },
];

const EMPTY = [];

export default function HitEndingTab() {
  const { data: maps, loading, error, reload } = useApi(fetchHeatMaps, [], EMPTY);
  const [map, setMap] = useState(null);
  const [layer, setLayer] = useState('ending');
  const [showPoints, setShowPoints] = useState(false);

  useEffect(() => { setMap(m => m ?? (maps ?? [])[0]?.map ?? null); }, [maps]);

  const heatFetcher = useCallback(
    () => (map ? fetchHeat(map) : Promise.resolve(null)), [map]);
  const { data: heat, loading: heatLoading } = useApi(heatFetcher, [map], null);

  if (loading) return <Pad><LoadingPanel title="히트엔딩을 불러오는 중입니다" detail="" /></Pad>;
  if (error) return <Pad><ErrorPanel title="히트엔딩을 불러오지 못했습니다" message={error} onRetry={reload} /></Pad>;
  if (!(maps ?? []).length) {
    return (
      <Pad>
        <Empty title="집계된 맵이 아직 없습니다"
               reason="매치로그를 모은 뒤 python ingest/build_heat.py 로 만듭니다." />
      </Pad>
    );
  }

  const current = maps.find(m => m.map === map);
  const spec = LAYERS.find(l => l.key === layer);

  return (
    <Pad>
      {/* 맵 고르기 — 경기 수를 같이 적는다 */}
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '14px' }}>
        {maps.map(m => (
          <button key={m.map} onClick={() => setMap(m.map)} style={{
            display: 'flex', flexDirection: 'column', gap: '2px', alignItems: 'flex-start',
            padding: '9px 16px', borderRadius: 'var(--radius-sm)',
            background: m.map === map ? 'var(--accent-gold)' : 'rgba(255,255,255,0.04)',
            color: m.map === map ? '#000' : 'var(--text-muted)',
            border: `1px solid ${m.map === map ? 'var(--accent-gold)' : 'var(--border-subtle)'}`,
            cursor: 'pointer', fontWeight: 900, fontSize: '0.86rem'
          }}>
            {m.mapLabel}
            <span style={{ fontSize: '0.7rem', opacity: 0.75, fontWeight: 700 }}>
              {m.matches.toLocaleString()}경기
            </span>
          </button>
        ))}
      </div>

      {/* 무엇을 볼지 */}
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '6px' }}>
        {LAYERS.map(({ key, label, icon: Icon }) => (
          <button key={key} onClick={() => setLayer(key)} style={{
            display: 'flex', alignItems: 'center', gap: '7px',
            padding: '8px 15px', borderRadius: 'var(--radius-sm)',
            background: key === layer ? 'rgba(243,166,31,0.15)' : 'rgba(255,255,255,0.04)',
            color: key === layer ? 'var(--accent-gold)' : 'var(--text-muted)',
            border: `1px solid ${key === layer ? 'rgba(243,166,31,0.5)' : 'var(--border-subtle)'}`,
            cursor: 'pointer', fontWeight: 800, fontSize: '0.83rem'
          }}>
            <Icon size={14} /> {label}
          </button>
        ))}
        {layer === 'ending' && (
          <label style={{ display: 'flex', alignItems: 'center', gap: '6px',
                          color: 'var(--text-muted)', fontSize: '0.8rem', cursor: 'pointer' }}>
            <input type="checkbox" checked={showPoints}
                   onChange={e => setShowPoints(e.target.checked)} />
            경기마다 점으로
          </label>
        )}
      </div>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0 0 14px' }}>
        {spec.hint}
      </p>

      {heatLoading || !heat
        ? <LoadingPanel title="집계를 그리는 중입니다" detail="" />
        : <HeatView heat={heat} layer={layer} spec={spec} showPoints={showPoints} />}

      <p style={{ color: 'var(--text-muted)', fontSize: '0.74rem', marginTop: '14px', lineHeight: 1.6 }}>
        <Info size={12} style={{ verticalAlign: '-2px' }} />{' '}
        {heat?.mapNote ? heat.mapNote + ' ' : ''}
        {current?.matches.toLocaleString()}경기 · {current?.stages}개 대회 단계를 모은 값입니다.
        {' '}우리가 뽑아 둔 매치로그만 센 것이라 전체 프로 경기가 아닙니다.
        {' '}출처: <a href="https://developer.pubg.com" target="_blank" rel="noopener noreferrer"
                  style={{ color: 'var(--text-muted)', textDecoration: 'underline' }}>PUBG 공식 API</a>
        {' '}· 맵 이미지: PUBG 공식 api-assets
      </p>
    </Pad>
  );
}

/** 맵 이미지 위에 격자 밀도를 덮는다. */
function HeatView({ heat, layer, spec, showPoints }) {
  const canvasRef = useRef(null);
  const L = heat.layers?.[layer];

  const stats = useMemo(() => {
    if (!L?.cells?.length) return null;
    const g = heat.grid;
    const top = L.cells.slice(0, 5).map(([i, j, n]) => ({
      x: (i + 0.5) / g, y: (j + 0.5) / g, n,
      share: (n / L.total) * 100,
    }));
    // 중심이 어디로 치우쳤는지. 치우치지 않았다는 것도 사실이라 그대로 적는다.
    let sx = 0, sy = 0;
    for (const [i, j, n] of L.cells) { sx += (i + 0.5) / g * n; sy += (j + 0.5) / g * n; }
    return { top, cx: sx / L.total, cy: sy / L.total };
  }, [L, heat.grid]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !L) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, SIZE, SIZE);
    const [r, g, b] = spec.color;

    // **칸마다 그대로 칠하면 안 읽힌다.** 엔딩은 1,196개 점이 2,500칸에
    // 흩어져 대부분이 1~2 라, 낮은 값을 들어 올리면 지도 전체가 덮이고
    // 안 들어 올리면 한 칸만 보인다. 그래서 주변으로 번지게 한 뒤(상자
    // 흐리기 두 번 = 가우시안 근사) 그 밀도를 칠한다. 뭉친 곳이 드러난다.
    const G = heat.grid;
    let acc = new Float32Array(G * G);
    for (const [i, j, n] of L.cells) acc[j * G + i] = n;
    acc = blur(blur(acc, G, 1), G, 1);

    // **자르는 기준을 층마다 분포에서 뽑는다.** 고정값을 쓰면 한쪽이 깨진다 —
    // 엔딩은 1,196개가 흩어져 거의 안 보이고, 낙하는 82,177개라 섬 전체가
    // 덮인다. 값이 있는 칸의 중앙값 언저리를 바닥으로 잡으면 둘 다 "몰린 데"
    // 만 남는다.
    const nz = Array.from(acc).filter(v => v > 0).sort((a, b) => a - b);
    const max = nz.length ? nz[nz.length - 1] : 0;
    const floor = nz.length ? nz[Math.floor(nz.length * 0.55)] : 0;
    const span = Math.max(1e-9, max - floor);

    const small = document.createElement('canvas');
    small.width = G; small.height = G;
    const sctx = small.getContext('2d');
    const img = sctx.createImageData(G, G);
    for (let k = 0; k < acc.length; k += 1) {
      const v = Math.max(0, (acc[k] - floor) / span);
      const a = v <= 0 ? 0 : Math.min(0.9, Math.pow(v, 0.65) * 0.9);
      const w = Math.pow(v, 1.6) * 110;          // 가장 진한 쪽만 흰빛을 섞는다
      img.data[k * 4] = Math.min(255, r + w);
      img.data[k * 4 + 1] = Math.min(255, g + w);
      img.data[k * 4 + 2] = Math.min(255, b + w);
      img.data[k * 4 + 3] = a * 255;
    }
    sctx.putImageData(img, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(small, 0, 0, SIZE, SIZE);

    // 엔딩은 경기마다 점 하나로도 볼 수 있다. 격자보다 실제 분포가 잘 보인다.
    if (showPoints && layer === 'ending') {
      ctx.clearRect(0, 0, SIZE, SIZE);
      ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.55)`;
      for (const [x, y] of heat.endPoints ?? []) {
        ctx.beginPath();
        ctx.arc(x * SIZE, y * SIZE, 3.2, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // 가장 잦은 다섯 칸에 번호를 붙여 오른쪽 목록과 잇는다.
    if (stats && !(showPoints && layer === 'ending')) {
      stats.top.forEach((t, k) => {
        const x = t.x * SIZE, y = t.y * SIZE;
        ctx.beginPath();
        ctx.arc(x, y, 13, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(8,12,20,0.8)';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1.6;
        ctx.stroke();
        ctx.fillStyle = '#fff';
        ctx.font = '900 14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(String(k + 1), x, y + 5);
        ctx.textAlign = 'left';
      });
    }
  }, [L, heat, layer, spec, showPoints, stats]);

  return (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{
        flex: '1 1 560px', minWidth: 0, maxWidth: SIZE, position: 'relative',
        borderRadius: 'var(--radius-sm)', overflow: 'hidden',
        border: '1px solid var(--border-subtle)', background: '#0a0e16'
      }}>
        <img src={`/maps/${heat.image || heat.map}.png`} alt={heat.mapLabel}
             style={{ width: '100%', aspectRatio: '1 / 1', display: 'block', opacity: 0.8 }}
             onError={e => { e.currentTarget.style.visibility = 'hidden'; }} />
        <canvas ref={canvasRef} width={SIZE} height={SIZE}
                style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />
      </div>

      <div style={{ flex: '1 1 260px', minWidth: '240px' }}>
        <div style={{ fontSize: '0.82rem', color: '#fff', fontWeight: 900, marginBottom: '8px' }}>
          가장 잦은 자리
        </div>
        {stats ? (
          <>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '3px' }}>
              {stats.top.map((t, k) => (
                <div key={k} style={{
                  display: 'flex', alignItems: 'center', gap: '9px', padding: '7px 10px',
                  borderRadius: 'var(--radius-sm)', background: 'rgba(255,255,255,0.03)',
                  border: '1px solid var(--border-subtle)', fontSize: '0.8rem'
                }}>
                  <span style={{
                    width: '20px', height: '20px', borderRadius: '50%', flexShrink: 0,
                    background: 'rgba(255,255,255,0.1)', color: '#fff', fontWeight: 900,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '0.72rem'
                  }}>{k + 1}</span>
                  <span style={{ color: 'var(--text-muted)', fontVariantNumeric: 'tabular-nums' }}>
                    {Math.round(t.x * 100)}%, {Math.round(t.y * 100)}%
                  </span>
                  <span style={{ marginLeft: 'auto', color: '#fff', fontWeight: 800 }}>
                    {t.n.toLocaleString()}
                  </span>
                  <span style={{ color: 'var(--text-muted)', width: '42px', textAlign: 'right' }}>
                    {t.share.toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
            <div style={{ marginTop: '12px', padding: '10px 12px',
                          borderRadius: 'var(--radius-sm)',
                          background: 'rgba(255,255,255,0.03)',
                          border: '1px solid var(--border-subtle)',
                          fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              무게중심 <b style={{ color: '#fff' }}>
                {Math.round(stats.cx * 100)}%, {Math.round(stats.cy * 100)}%
              </b>
              {' '}— 지도 한가운데가 50%, 50% 입니다.
              {' '}{describeBias(stats.cx, stats.cy)}
            </div>
            <div style={{ marginTop: '8px', fontSize: '0.74rem', color: 'var(--text-muted)' }}>
              좌표는 지도 왼쪽 위를 0%, 오른쪽 아래를 100% 로 본 값입니다.
              지명은 붙이지 않았습니다 — 우리에게 지명 데이터가 없습니다.
            </div>
          </>
        ) : <div style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>셀 데이터가 없습니다.</div>}
      </div>
    </div>
  );
}

/** 상자 흐리기 한 번. 가로·세로로 나눠 돌려 가우시안에 가깝게 만든다. */
function blur(src, G, radius) {
  const tmp = new Float32Array(G * G);
  const out = new Float32Array(G * G);
  const w = radius * 2 + 1;
  for (let y = 0; y < G; y += 1) {
    for (let x = 0; x < G; x += 1) {
      let sum = 0;
      for (let d = -radius; d <= radius; d += 1) {
        sum += src[y * G + Math.min(G - 1, Math.max(0, x + d))];
      }
      tmp[y * G + x] = sum / w;
    }
  }
  for (let x = 0; x < G; x += 1) {
    for (let y = 0; y < G; y += 1) {
      let sum = 0;
      for (let d = -radius; d <= radius; d += 1) {
        sum += tmp[Math.min(G - 1, Math.max(0, y + d)) * G + x];
      }
      out[y * G + x] = sum / w;
    }
  }
  return out;
}

/** 무게중심이 한가운데서 얼마나 벗어났는지 말로 적는다. 안 벗어난 것도 사실이다. */
function describeBias(cx, cy) {
  const dx = cx - 0.5, dy = cy - 0.5;
  const d = Math.hypot(dx, dy);
  if (d < 0.03) return '거의 한가운데라 쏠림이 없습니다.';
  const ns = dy < 0 ? '북' : '남';
  const ew = dx < 0 ? '서' : '동';
  const dir = Math.abs(dx) < 0.03 ? ns : Math.abs(dy) < 0.03 ? ew : ns + ew;
  return `${dir}쪽으로 ${Math.round(d * 100)}% 쏠려 있습니다.`;
}

function Pad({ children }) {
  return <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>{children}</div>;
}

function Empty({ title, reason }) {
  return (
    <div className="glass-panel" style={{
      padding: '40px 28px', borderRadius: 'var(--radius-md)', textAlign: 'center',
      border: '1px solid var(--border-subtle)'
    }}>
      <Crosshair size={34} color="var(--accent-gold)" style={{ marginBottom: '14px' }} />
      <h2 style={{ fontSize: '1.2rem', fontWeight: 900, color: '#fff', margin: '0 0 8px' }}>{title}</h2>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: 0 }}>{reason}</p>
    </div>
  );
}
