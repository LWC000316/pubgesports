import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Play, Pause, SkipBack, Users, Crosshair, Car, Skull, ZoomIn } from 'lucide-react';

/**
 * 매치로그. 실제 맵 이미지 위에 선수 이동 경로와 자기장을 그린다.
 *
 * 좌표는 맵 한 변을 1 로 둔 비율이라(build_match_log.py) 캔버스 크기와 무관하게
 * 그대로 곱하면 된다. 캔버스 내부 해상도는 SIZE 로 고정하고 화면에서만 늘인다.
 *
 * 맵 이미지는 PUBG 가 API 사용자용으로 공개한 공식 api-assets 저장소에서 받았다
 * (frontend/public/maps/).
 */
const SIZE = 1000;

// 팀 구분용 색. 16팀까지 눈으로 구별되는 값으로 골랐다.
const TEAM_COLORS = [
  '#f3a61f', '#00e5ff', '#ff4d6d', '#51cf66', '#c084fc', '#ffd43b',
  '#4dabf7', '#ff922b', '#38d9a9', '#f783ac', '#a9e34b', '#748ffc',
  '#ffa94d', '#63e6be', '#e599f7', '#ff8787'
];

const SPEEDS = [1, 2, 4, 8];
const TICK_MS = 100;

const mmss = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.round(s) % 60).padStart(2, '0')}`;

export default function MatchLogMap({ log }) {
  const canvasRef = useRef(null);
  const [time, setTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(2);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [showKills, setShowKills] = useState(true);
  const [showTrails, setShowTrails] = useState(true);
  const [zoom, setZoom] = useState(1);

  const duration = log?.duration ?? 0;

  // 팀별로 선수를 묶는다. 경로를 팀 색으로 그리기 위해서다.
  const teams = useMemo(() => {
    const map = new Map();
    for (const t of log?.tracks ?? []) {
      const key = t.team || t.nickname;
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(t);
    }
    return [...map.entries()].sort((a, b) => a[0].localeCompare(b[0]));
  }, [log]);

  const colorOf = useMemo(() => {
    const m = new Map();
    teams.forEach(([name], i) => m.set(name, TEAM_COLORS[i % TEAM_COLORS.length]));
    return m;
  }, [teams]);

  // 선수가 언제 죽었는지. 킬 로그에 시각이 있으면 그걸 쓰고, 없으면 경로가
  // 끊긴 시점으로 본다. 둘 다 데이터에서 나온 값이라 지어내지 않는다.
  const deathAt = useMemo(() => {
    const m = new Map();
    for (const t of log?.tracks ?? []) {
      const pts = t.points;
      if (pts?.length) m.set(t.name, pts[pts.length - 1][0]);
    }
    for (const k of log?.kills ?? []) {
      if (k.t != null && k.victim) m.set(k.victim, k.t);
    }
    return m;
  }, [log]);

  // 지금 시각까지 일어난 킬. 오른쪽 킬 피드와 지도 표시에 함께 쓴다.
  const killsSoFar = useMemo(
    () => (log?.kills ?? []).filter(k => k.t == null || k.t <= time),
    [log, time]);

  useEffect(() => { setTime(0); setPlaying(false); setSelectedPlayer(null); }, [log]);

  useEffect(() => {
    if (!playing) return;
    const id = setInterval(() => {
      setTime(t => {
        const next = t + speed * (TICK_MS / 1000) * 10;
        if (next >= duration) { setPlaying(false); return duration; }
        return next;
      });
    }, TICK_MS);
    return () => clearInterval(id);
  }, [playing, duration, speed]);

  const circle = useMemo(
    () => [...(log?.circles ?? [])].reverse().find(c => c.t <= time),
    [log, time]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !log) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, SIZE, SIZE);
    const px = v => v * SIZE;

    // 1. 자기장. 바깥을 어둡게 해서 안전 구역이 드러나게 한다.
    if (circle && circle.r > 0) {
      ctx.save();
      ctx.fillStyle = 'rgba(0, 20, 40, 0.45)';
      ctx.beginPath();
      ctx.rect(0, 0, SIZE, SIZE);
      ctx.arc(px(circle.x), px(circle.y), px(circle.r), 0, Math.PI * 2, true);
      ctx.fill('evenodd');
      ctx.strokeStyle = '#00e5ff';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(px(circle.x), px(circle.y), px(circle.r), 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    // 2. 이동 경로
    for (const [teamName, members] of teams) {
      if (selectedTeam && selectedTeam !== teamName) continue;
      const color = colorOf.get(teamName);
      for (const track of members) {
        if (selectedPlayer && selectedPlayer !== track.name) continue;
        const focused = Boolean(selectedTeam || selectedPlayer);
        const pts = track.points.filter(p => p[0] <= time);
        if (!pts.length) continue;

        if (showTrails && pts.length > 1) {
          ctx.strokeStyle = color;
          ctx.globalAlpha = focused ? 0.9 : 0.45;
          ctx.lineWidth = focused ? 2.4 : 1.3;
          ctx.beginPath();
          pts.forEach((p, i) => {
            const x = px(p[1]), y = px(p[2]);
            if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
          });
          ctx.stroke();
        }

        // 낙하 지점 — 경로의 첫 점. 어디서 시작했는지가 전술을 읽는 출발점이다.
        if (focused) {
          const first = pts[0];
          ctx.globalAlpha = 0.8;
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.arc(px(first[1]), px(first[2]), 6, 0, Math.PI * 2);
          ctx.stroke();
        }

        // 현재 위치
        const last = pts[pts.length - 1];
        const dead = (deathAt.get(track.name) ?? Infinity) <= time;
        ctx.globalAlpha = dead ? 0.35 : 1;
        ctx.fillStyle = last[4] ? '#ff4d6d' : color;   // 기절 상태면 빨강
        ctx.beginPath();
        ctx.arc(px(last[1]), px(last[2]), focused ? 6 : 3.6, 0, Math.PI * 2);
        ctx.fill();

        if (last[3]) {                                  // 차량 탑승 중이면 테두리
          ctx.globalAlpha = dead ? 0.35 : 1;
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 1.6;
          ctx.beginPath();
          ctx.arc(px(last[1]), px(last[2]), focused ? 9 : 6, 0, Math.PI * 2);
          ctx.stroke();
        }
        if (focused) {
          ctx.globalAlpha = 1;
          ctx.fillStyle = dead ? 'rgba(255,255,255,0.45)' : '#fff';
          ctx.font = '600 13px sans-serif';
          ctx.fillText(track.nickname, px(last[1]) + 9, px(last[2]) + 4);
        }
      }
    }
    ctx.globalAlpha = 1;

    // 3. 킬 지점 — 지금까지 일어난 것만
    if (showKills) {
      ctx.strokeStyle = '#ff4d6d';
      ctx.lineWidth = 1.8;
      for (const k of killsSoFar) {
        const x = px(k.x), y = px(k.y);
        ctx.beginPath();
        ctx.moveTo(x - 5, y - 5); ctx.lineTo(x + 5, y + 5);
        ctx.moveTo(x + 5, y - 5); ctx.lineTo(x - 5, y + 5);
        ctx.stroke();
      }
    }
  }, [log, time, teams, colorOf, selectedTeam, selectedPlayer, showKills,
      showTrails, circle, killsSoFar, deathAt]);

  if (!log) return null;

  const aliveOf = track => (deathAt.get(track.name) ?? Infinity) > time;

  return (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{ flex: '1 1 520px', minWidth: 0, maxWidth: SIZE }}>
        <div style={{
          position: 'relative', width: '100%', borderRadius: 'var(--radius-sm)',
          overflow: 'hidden', border: '1px solid var(--border-subtle)', background: '#0a0e16'
        }}>
          <div style={{
            width: '100%', aspectRatio: '1 / 1', overflow: zoom > 1 ? 'auto' : 'hidden'
          }}>
            <div style={{
              position: 'relative', width: `${zoom * 100}%`, aspectRatio: '1 / 1'
            }}>
              <img
                src={`/maps/${log.map}.png`}
                alt={log.mapLabel}
                style={{ width: '100%', aspectRatio: '1 / 1', display: 'block', opacity: 0.85 }}
                onError={e => { e.currentTarget.style.visibility = 'hidden'; }}
              />
              <canvas
                ref={canvasRef}
                width={SIZE}
                height={SIZE}
                style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}
              />
            </div>
          </div>
        </div>

        {/* 재생 조작 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '12px', flexWrap: 'wrap' }}>
          <button onClick={() => { if (time >= duration) setTime(0); setPlaying(p => !p); }} style={ctrlBtn}>
            {playing ? <Pause size={15} /> : <Play size={15} />}{playing ? '정지' : '재생'}
          </button>
          <button onClick={() => { setPlaying(false); setTime(0); }} style={ctrlBtn}>
            <SkipBack size={15} /> 처음
          </button>
          <div style={{ display: 'flex', gap: '2px' }}>
            {SPEEDS.map(s => (
              <button key={s} onClick={() => setSpeed(s)} style={{
                ...ctrlBtn, padding: '7px 10px',
                background: speed === s ? 'var(--accent-gold)' : 'rgba(255,255,255,0.05)',
                color: speed === s ? '#000' : '#fff', fontWeight: '800'
              }}>{s}x</button>
            ))}
          </div>
          <span style={{ color: 'var(--accent-gold)', fontWeight: '900', fontVariantNumeric: 'tabular-nums' }}>
            {mmss(time)} / {mmss(duration)}
          </span>
        </div>

        <input
          type="range" min={0} max={duration} value={Math.round(time)}
          onChange={e => { setPlaying(false); setTime(Number(e.target.value)); }}
          style={{ width: '100%', marginTop: '10px', accentColor: 'var(--accent-gold)' }}
        />

        <div style={{ display: 'flex', gap: '14px', marginTop: '10px', fontSize: '0.8rem',
                      color: 'var(--text-muted)', flexWrap: 'wrap', alignItems: 'center' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Users size={14} /> 생존 {circle?.alive ?? '-'}명 / {circle?.aliveTeams ?? '-'}팀
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Skull size={14} /> 킬 {killsSoFar.length} / {log.kills?.length ?? 0}
          </span>
          <Toggle on={showKills} set={setShowKills} icon={Crosshair} label="킬 지점" />
          <Toggle on={showTrails} set={setShowTrails} icon={Car} label="이동 경로" />
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <ZoomIn size={14} />
            <input type="range" min={1} max={3} step={0.5} value={zoom}
                   onChange={e => setZoom(Number(e.target.value))}
                   style={{ width: '70px', accentColor: 'var(--accent-gold)' }} />
            {zoom}x
          </label>
        </div>
      </div>

      {/* 팀·선수 목록과 킬 피드 */}
      <div style={{ flex: '1 1 260px', minWidth: '240px', display: 'flex',
                    flexDirection: 'column', gap: '12px' }}>
        <div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
            팀을 누르면 그 팀만, 선수를 누르면 그 선수만 봅니다
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '3px',
                        maxHeight: '440px', overflowY: 'auto' }}>
            {teams.map(([name, members]) => {
              const on = selectedTeam === name;
              const alive = members.filter(aliveOf).length;
              return (
                <div key={name}>
                  <button
                    onClick={() => { setSelectedTeam(on ? null : name); setSelectedPlayer(null); }}
                    style={{
                      display: 'flex', alignItems: 'center', gap: '8px', width: '100%',
                      padding: '7px 10px', borderRadius: 'var(--radius-sm)',
                      background: on ? 'rgba(243,166,31,0.12)' : 'rgba(255,255,255,0.03)',
                      border: `1px solid ${on ? 'rgba(243,166,31,0.5)' : 'var(--border-subtle)'}`,
                      color: alive ? '#fff' : 'var(--text-muted)',
                      fontSize: '0.82rem', fontWeight: '700', cursor: 'pointer', textAlign: 'left'
                    }}>
                    <span style={{ width: '10px', height: '10px', borderRadius: '50%',
                                   background: colorOf.get(name), flexShrink: 0,
                                   opacity: alive ? 1 : 0.3 }} />
                    {name}
                    <span style={{ marginLeft: 'auto', fontSize: '0.74rem', opacity: 0.75 }}>
                      {alive}/{members.length}
                    </span>
                  </button>
                  {on && (
                    <div style={{ padding: '4px 0 4px 18px', display: 'flex',
                                  flexDirection: 'column', gap: '2px' }}>
                      {members.map(p => {
                        const live = aliveOf(p);
                        const picked = selectedPlayer === p.name;
                        return (
                          <button key={p.name}
                            onClick={() => setSelectedPlayer(picked ? null : p.name)}
                            style={{
                              display: 'flex', alignItems: 'center', gap: '6px',
                              padding: '4px 8px', borderRadius: 'var(--radius-sm)',
                              background: picked ? 'rgba(243,166,31,0.18)' : 'transparent',
                              border: 'none', cursor: 'pointer', textAlign: 'left',
                              color: live ? '#fff' : 'var(--text-muted)',
                              fontSize: '0.78rem', textDecoration: live ? 'none' : 'line-through'
                            }}>
                            {p.nickname}
                            {!live && <Skull size={11} style={{ marginLeft: 'auto' }} />}
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* 킬 피드 — 시각이 있는 로그만 시간순으로 쌓인다 */}
        {(log.kills ?? []).some(k => k.t != null) && (
          <div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
              킬 로그
            </div>
            <div style={{ display: 'flex', flexDirection: 'column-reverse', gap: '2px',
                          maxHeight: '200px', overflowY: 'auto' }}>
              {killsSoFar.map((k, i) => (
                <div key={i} style={{
                  display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 8px',
                  borderRadius: 'var(--radius-sm)', background: 'rgba(255,255,255,0.03)',
                  fontSize: '0.75rem', color: 'var(--text-muted)'
                }}>
                  <span style={{ fontVariantNumeric: 'tabular-nums', opacity: 0.7 }}>
                    {k.t != null ? mmss(k.t) : '--:--'}
                  </span>
                  <span style={{ color: '#fff' }}>{short(k.killer)}</span>
                  <Crosshair size={11} color="#ff4d6d" />
                  <span>{short(k.victim)}</span>
                  {k.weapon && <span style={{ marginLeft: 'auto', opacity: 0.6 }}>{k.weapon}</span>}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

/** 인게임 아이디에서 접두사를 떼어 닉네임만 보여준다. */
function short(name) {
  if (!name) return '—';
  const i = name.indexOf('_');
  return i > 0 ? name.slice(i + 1) : name;
}

function Toggle({ on, set, icon: Icon, label }) {
  return (
    <label style={{ display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
      <input type="checkbox" checked={on} onChange={e => set(e.target.checked)} />
      <Icon size={14} /> {label}
    </label>
  );
}

const ctrlBtn = {
  display: 'flex',
  alignItems: 'center',
  gap: '6px',
  padding: '7px 14px',
  borderRadius: 'var(--radius-sm)',
  background: 'rgba(255,255,255,0.05)',
  border: '1px solid var(--border-subtle)',
  color: '#fff',
  fontSize: '0.82rem',
  fontWeight: '700',
  cursor: 'pointer'
};
