import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Crosshair, Plane, Skull, Target, Info, CircleDashed, Play, Pause } from 'lucide-react';
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
  // 처음 말한 "지형 중 어느 부분이 서클에 많이 걸치는가" 가 이것이다.
  // 마지막 한 점만 보는 '엔딩' 과 다른 질문이고, 페이즈를 넘기면 그대로
  // 서클이 줄어드는 모습이 된다.
  { key: 'zone', label: '자기장', icon: CircleDashed,
    hint: '그 칸이 자기장 안에 든 경기 비율. 페이즈를 넘기면 서클이 줄어드는 모습이 된다.',
    color: [0, 229, 255] },
];

const EMPTY = [];

/**
 * 무지개 색 띠. 보라 -> 파랑 -> 청록 -> 초록 -> 노랑 -> 빨강.
 *
 * **한 가지 색의 농도로는 3%와 30%가 구별되지 않는다.** 농도만 쓰면 눈이
 * 네댓 단계밖에 못 가르는데, 색이 바뀌면 그보다 훨씬 잘게 읽힌다. 지도 위에
 * 밀도를 얹는 자료가 대개 이 띠를 쓰는 이유다.
 *
 * 낮은 쪽은 투명에 가깝게 둬서 바닥이 통째로 덮이지 않게 한다.
 */
const RAMP = [
  [0.00, [40, 0, 90, 0.00]],
  [0.10, [90, 20, 160, 0.45]],
  [0.28, [40, 70, 230, 0.70]],
  [0.46, [0, 200, 220, 0.78]],
  [0.62, [60, 230, 90, 0.82]],
  [0.78, [240, 230, 40, 0.86]],
  [1.00, [250, 50, 30, 0.90]],
];

function rampAt(v) {
  const t = Math.max(0, Math.min(1, v));
  for (let i = 1; i < RAMP.length; i += 1) {
    if (t <= RAMP[i][0]) {
      const [p0, c0] = RAMP[i - 1];
      const [p1, c1] = RAMP[i];
      const f = (t - p0) / Math.max(1e-9, p1 - p0);
      return c0.map((c, k) => c + (c1[k] - c) * f);
    }
  }
  return RAMP[RAMP.length - 1][1];
}

export default function HitEndingTab() {
  const { data: maps, loading, error, reload } = useApi(fetchHeatMaps, [], EMPTY);
  const [map, setMap] = useState(null);
  const [layer, setLayer] = useState('zone');
  const [showPoints, setShowPoints] = useState(false);
  const [phase, setPhase] = useState(2);
  const [playing, setPlaying] = useState(false);

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
        {layer === 'zone' && (
          <PhasePicker heat={heat} phase={phase} setPhase={setPhase}
                       playing={playing} setPlaying={setPlaying} />
        )}
      </div>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', margin: '0 0 14px' }}>
        {spec.hint}
      </p>

      {heatLoading || !heat
        ? <LoadingPanel title="집계를 그리는 중입니다" detail="" />
        : <HeatView heat={heat} layer={layer} spec={spec} showPoints={showPoints}
                    phase={phase} />}

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
function HeatView({ heat, layer, spec, showPoints, phase }) {
  const canvasRef = useRef(null);
  // 자기장은 페이즈마다 따로 집계돼 있다. 나머지 셋은 한 장씩이다.
  const L = useMemo(() => {
    if (layer !== 'zone') return heat.layers?.[layer];
    const z = (heat.zones ?? []).find(x => x.phase === phase);
    // 목록·통계는 상위 칸만 쓰고, 그림은 counts 배열을 쓴다.
    return z && { ...z, cells: z.top ?? z.cells ?? [] };
  }, [heat, layer, phase]);

  const stats = useMemo(() => {
    if (!L?.cells?.length) return null;
    const g = heat.grid;
    // 비율의 뜻이 층마다 다르다. 낙하·사망·엔딩은 "전체 중 이 칸의 몫"이고,
    // 자기장은 "그 칸이 자기장 안에 든 경기 비율"이다. 분모를 가른다.
    const sum = L.cells.reduce((a, c) => a + c[2], 0);
    const denom = layer === 'zone' ? (L.matches || 1) : sum;
    // **붙어 있는 칸은 같은 자리다.** 그냥 앞에서 다섯 개를 집으면
    // "49%,37% · 47%,41% · 49%,39%" 처럼 한 덩어리가 다섯 줄로 나온다.
    // 이미 집은 자리에서 다섯 칸 안쪽이면 건너뛴다.
    const GAP = 5;
    const top = [];
    for (const [i, j, n] of L.cells) {
      if (top.length >= 5) break;
      if (top.some(t => Math.abs(t.i - i) < GAP && Math.abs(t.j - j) < GAP)) continue;
      top.push({ i, j, x: (i + 0.5) / g, y: (j + 0.5) / g, n, share: (n / denom) * 100 });
    }
    // 중심이 어디로 치우쳤는지. 치우치지 않았다는 것도 사실이라 그대로 적는다.
    let sx = 0, sy = 0;
    for (const [i, j, n] of L.cells) { sx += (i + 0.5) / g * n; sy += (j + 0.5) / g * n; }
    const peak = L.cells.length ? L.cells[0][2] : 0;
    return { top, cx: sx / sum, cy: sy / sum, peak, denom };
  }, [L, heat.grid, layer]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !L) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, SIZE, SIZE);
    const [r, g, b] = spec.color;

    // 자기장은 빽빽한 배열로 와서 그대로 격자가 된다. 해상도가 높아
    // 흐릴 필요도, 기준을 뽑을 필요도 없다 — 확률을 색 띠에 그대로 태운다.
    if (layer === 'zone' && L.counts) {
      const Z = heat.zoneGrid || heat.grid;
      const denom = L.max || 1;
      const small = document.createElement('canvas');
      small.width = Z; small.height = Z;
      const sctx = small.getContext('2d');
      const img = sctx.createImageData(Z, Z);
      for (let k = 0; k < L.counts.length; k += 1) {
        const [r, g, b, a] = rampAt(L.counts[k] / denom);
        img.data[k * 4] = r;
        img.data[k * 4 + 1] = g;
        img.data[k * 4 + 2] = b;
        img.data[k * 4 + 3] = a * 255;
      }
      sctx.putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(small, 0, 0, SIZE, SIZE);
      return;                       // 번호 표식은 얹지 않는다 — 지도가 어수선해진다
    }

    // **칸마다 그대로 칠하면 안 읽힌다.** 엔딩은 1,196개 점이 2,500칸에
    // 흩어져 대부분이 1~2 라, 낮은 값을 들어 올리면 지도 전체가 덮이고
    // 안 들어 올리면 한 칸만 보인다. 그래서 주변으로 번지게 한 뒤(상자
    // 흐리기 두 번 = 가우시안 근사) 그 밀도를 칠한다. 뭉친 곳이 드러난다.
    const G = heat.grid;
    let acc = new Float32Array(G * G);
    for (const [i, j, n] of L.cells) acc[j * G + i] = n;
    // 자기장은 원을 쌓은 값이라 이미 매끄럽다. 더 흐리면 가장자리만 뭉갠다.
    if (layer !== 'zone') acc = blur(blur(acc, G, 1), G, 1);

    // **자기장은 확률이라 절대값으로 칠한다.** "이 칸이 경기의 몇 %에서
    // 자기장 안이었나" 가 그 자체로 뜻을 가지므로, 분포에서 기준을 뽑으면
    // 오히려 맵마다 색이 다른 것을 뜻하게 된다. 0 을 투명, 최대를 가장
    // 진하게 둔다.
    //
    // 나머지 셋은 횟수라 절대값이 뜻을 갖지 않는다. 그쪽은 **분포에서**
    // 기준을 뽑는다 — 엔딩은 1,196개가 흩어져 거의 안 보이고 낙하는
    // 82,177개라 섬 전체가 덮이는데, 값이 있는 칸의 중앙값 언저리를 바닥으로
    // 잡으면 둘 다 "몰린 데"만 남는다.
    const nz = Array.from(acc).filter(v => v > 0).sort((a, b) => a - b);
    const max = nz.length ? nz[nz.length - 1] : 0;
    const floor = layer === 'zone'
      ? 0 : (nz.length ? nz[Math.floor(nz.length * 0.55)] : 0);
    const span = Math.max(1e-9, max - floor);

    const small = document.createElement('canvas');
    small.width = G; small.height = G;
    const sctx = small.getContext('2d');
    const img = sctx.createImageData(G, G);
    for (let k = 0; k < acc.length; k += 1) {
      const v = Math.max(0, (acc[k] - floor) / span);
      const a = v <= 0 ? 0 : Math.min(0.9, Math.pow(v, layer === 'zone' ? 2.4 : 0.65) * 0.9);
      const [cr, cg, cb, ca] = rampAt(v);
      img.data[k * 4] = cr;
      img.data[k * 4 + 1] = cg;
      img.data[k * 4 + 2] = cb;
      img.data[k * 4 + 3] = Math.min(ca, a) * 255;
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
            {/* **색이 무엇을 뜻하는지 적는다.** 가장 진한 곳이 50%인지 3%인지
                모르면 지도를 읽을 수가 없다. 층마다 단위가 다르다. */}
            <div style={{ marginTop: '12px', padding: '10px 12px',
                          borderRadius: 'var(--radius-sm)',
                          background: 'rgba(255,255,255,0.03)',
                          border: '1px solid var(--border-subtle)',
                          fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px',
                             marginBottom: '8px' }}>
                <span style={{ width: '84px', height: '10px', borderRadius: '3px',
                               background: 'linear-gradient(90deg, rgba(90,20,160,.5),'
                                 + ' rgba(40,70,230,.8), rgba(0,200,220,.85),'
                                 + ' rgba(60,230,90,.9), rgba(240,230,40,.95), rgb(250,50,30))',
                               flexShrink: 0 }} />
                가장 진한 곳 ={' '}
                <b style={{ color: '#fff' }}>
                  {layer === 'zone'
                    ? `경기의 ${((stats.peak / stats.denom) * 100).toFixed(1)}%`
                    : `${stats.peak.toLocaleString()}회`}
                </b>
              </span>
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

/**
 * 페이즈 고르개. 넘기면 그대로 **서클이 줄어드는 모습**이 된다.
 *
 * 페이즈마다 기여한 경기 수가 다르다 — 뒤로 갈수록 일찍 끝난 경기가 빠진다.
 * 그 수를 같이 보여 주지 않으면 뒤쪽 페이즈가 표본이 적다는 것이 숨는다.
 */
function PhasePicker({ heat, phase, setPhase, playing, setPlaying }) {
  const zones = heat?.zones ?? [];
  useEffect(() => {
    if (!playing || !zones.length) return;
    const id = setInterval(() => {
      setPhase(p => {
        const i = zones.findIndex(z => z.phase === p);
        const next = zones[(i + 1) % zones.length];
        return next ? next.phase : p;
      });
    }, 900);
    return () => clearInterval(id);
  }, [playing, zones, setPhase]);

  if (!zones.length) return null;
  const cur = zones.find(z => z.phase === phase);
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
      <button onClick={() => setPlaying(p => !p)} title="페이즈를 넘기며 재생"
        style={{ display: 'flex', alignItems: 'center', gap: '5px',
                 padding: '6px 11px', borderRadius: 'var(--radius-sm)',
                 background: 'rgba(255,255,255,0.05)', color: '#fff',
                 border: '1px solid var(--border-subtle)', cursor: 'pointer',
                 fontSize: '0.78rem', fontWeight: 800 }}>
        {playing ? <Pause size={13} /> : <Play size={13} />}
      </button>
      {zones.map(z => (
        <button key={z.phase} onClick={() => { setPlaying(false); setPhase(z.phase); }}
          style={{
            padding: '6px 10px', borderRadius: 'var(--radius-sm)',
            background: z.phase === phase ? 'var(--accent-gold)' : 'rgba(255,255,255,0.04)',
            color: z.phase === phase ? '#000' : 'var(--text-muted)',
            border: `1px solid ${z.phase === phase ? 'var(--accent-gold)' : 'var(--border-subtle)'}`,
            cursor: 'pointer', fontWeight: 900, fontSize: '0.76rem'
          }}>P{z.phase}</button>
      ))}
      {cur && (
        <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
          {cur.matches.toLocaleString()}경기
        </span>
      )}
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
