import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Play, Pause, SkipBack, Users, Crosshair } from 'lucide-react';

/**
 * 매치로그. 실제 맵 이미지 위에 선수 이동 경로와 자기장을 그린다.
 *
 * 좌표는 맵 한 변을 1 로 둔 비율이라(build_match_log.py) 캔버스 크기와 무관하게
 * 그대로 곱하면 된다.
 *
 * 맵 이미지는 PUBG 가 API 사용자용으로 공개한 공식 api-assets 저장소에서 받았다
 * (frontend/public/maps/).
 */
const SIZE = 760;

// 팀 구분용 색. 16팀까지 눈으로 구별되는 값으로 골랐다.
const TEAM_COLORS = [
  '#f3a61f', '#00e5ff', '#ff4d6d', '#51cf66', '#c084fc', '#ffd43b',
  '#4dabf7', '#ff922b', '#38d9a9', '#f783ac', '#a9e34b', '#748ffc',
  '#ffa94d', '#63e6be', '#e599f7', '#ff8787'
];

export default function MatchLogMap({ log }) {
  const canvasRef = useRef(null);
  const [time, setTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [showKills, setShowKills] = useState(true);

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

  useEffect(() => {
    if (!playing) return;
    const id = setInterval(() => {
      setTime(t => {
        const next = t + 10;
        if (next >= duration) { setPlaying(false); return duration; }
        return next;
      });
    }, 100);
    return () => clearInterval(id);
  }, [playing, duration]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !log) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, SIZE, SIZE);

    const px = v => v * SIZE;

    // 1. 자기장. 지금 시각 이하의 마지막 상태를 쓴다.
    const circle = [...(log.circles ?? [])].reverse().find(c => c.t <= time);
    if (circle && circle.r > 0) {
      ctx.save();
      // 바깥을 어둡게 해서 안전 구역이 드러나게 한다.
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
        const pts = track.points.filter(p => p[0] <= time);
        if (pts.length < 2) continue;
        ctx.strokeStyle = color;
        ctx.globalAlpha = selectedTeam ? 0.9 : 0.5;
        ctx.lineWidth = selectedTeam ? 2 : 1.2;
        ctx.beginPath();
        pts.forEach((p, i) => {
          const x = px(p[1]), y = px(p[2]);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // 현재 위치
        const last = pts[pts.length - 1];
        ctx.globalAlpha = 1;
        ctx.fillStyle = last[4] ? '#ff4d6d' : color;   // 기절 상태면 빨강
        ctx.beginPath();
        ctx.arc(px(last[1]), px(last[2]), selectedTeam ? 5 : 3.2, 0, Math.PI * 2);
        ctx.fill();
        if (selectedTeam) {
          ctx.fillStyle = '#fff';
          ctx.font = '600 11px sans-serif';
          ctx.fillText(track.nickname, px(last[1]) + 8, px(last[2]) + 4);
        }
      }
    }
    ctx.globalAlpha = 1;

    // 3. 킬 지점
    if (showKills) {
      ctx.strokeStyle = '#ff4d6d';
      ctx.lineWidth = 1.6;
      for (const k of log.kills ?? []) {
        const x = px(k.x), y = px(k.y);
        ctx.beginPath();
        ctx.moveTo(x - 4, y - 4); ctx.lineTo(x + 4, y + 4);
        ctx.moveTo(x + 4, y - 4); ctx.lineTo(x - 4, y + 4);
        ctx.stroke();
      }
    }
  }, [log, time, teams, colorOf, selectedTeam, showKills]);

  if (!log) return null;

  const circle = [...(log.circles ?? [])].reverse().find(c => c.t <= time);
  const mm = String(Math.floor(time / 60)).padStart(2, '0');
  const ss = String(time % 60).padStart(2, '0');

  return (
    <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{ flex: '1 1 420px', minWidth: 0, maxWidth: SIZE }}>
        <div style={{
          position: 'relative',
          width: '100%',
          borderRadius: 'var(--radius-sm)',
          overflow: 'hidden',
          border: '1px solid var(--border-subtle)',
          background: '#0a0e16'
        }}>
          <img
            src={`/maps/${log.map}.png`}
            alt={log.mapLabel}
            style={{ width: '100%', aspectRatio: '1 / 1', display: 'block', opacity: 0.85 }}
            onError={e => { e.currentTarget.style.visibility = 'hidden'; }}
          />
          {/* 캔버스 해상도는 SIZE 로 고정하고 화면에서만 늘였다 줄인다 */}
          <canvas
            ref={canvasRef}
            width={SIZE}
            height={SIZE}
            style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '12px', flexWrap: 'wrap' }}>
          <button
            onClick={() => { if (time >= duration) setTime(0); setPlaying(p => !p); }}
            style={ctrlBtn}
          >
            {playing ? <Pause size={15} /> : <Play size={15} />}
            {playing ? '정지' : '재생'}
          </button>
          <button onClick={() => { setPlaying(false); setTime(0); }} style={ctrlBtn}>
            <SkipBack size={15} /> 처음
          </button>
          <input
            type="range"
            min={0}
            max={duration}
            value={time}
            onChange={e => { setPlaying(false); setTime(Number(e.target.value)); }}
            style={{ flex: 1, minWidth: '200px', accentColor: 'var(--accent-gold)' }}
          />
          <span style={{ color: 'var(--accent-gold)', fontWeight: '800', fontVariantNumeric: 'tabular-nums' }}>
            {mm}:{ss}
          </span>
        </div>

        <div style={{ display: 'flex', gap: '16px', marginTop: '10px', fontSize: '0.8rem', color: 'var(--text-muted)', flexWrap: 'wrap' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Users size={14} /> 생존 {circle?.alive ?? '-'}명 / {circle?.aliveTeams ?? '-'}팀
          </span>
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
            <input type="checkbox" checked={showKills} onChange={e => setShowKills(e.target.checked)} />
            <Crosshair size={14} /> 킬 지점 {log.kills?.length ?? 0}건
          </label>
        </div>
      </div>

      <div style={{ flex: '0 1 220px', minWidth: '180px' }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '8px' }}>
          팀을 누르면 그 팀만 봅니다
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', maxHeight: `${SIZE}px`, overflowY: 'auto' }}>
          {teams.map(([name, members]) => {
            const active = selectedTeam === name;
            return (
              <button
                key={name}
                onClick={() => setSelectedTeam(active ? null : name)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '7px 10px',
                  borderRadius: 'var(--radius-sm)',
                  background: active ? 'rgba(243,166,31,0.12)' : 'rgba(255,255,255,0.03)',
                  border: `1px solid ${active ? 'rgba(243,166,31,0.5)' : 'var(--border-subtle)'}`,
                  color: active ? '#fff' : 'var(--text-muted)',
                  fontSize: '0.82rem',
                  fontWeight: '700',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <span style={{
                  width: '10px', height: '10px', borderRadius: '50%',
                  background: colorOf.get(name), flexShrink: 0
                }} />
                {name}
                <span style={{ marginLeft: 'auto', fontSize: '0.74rem', opacity: 0.7 }}>
                  {members.length}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
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
