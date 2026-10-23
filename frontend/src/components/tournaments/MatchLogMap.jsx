import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Play, Pause, SkipBack, Users, Crosshair, Route, Skull, ZoomIn, Swords,
  Package, Tag, Grid3x3, Plane, Ruler, Camera, Maximize2, MessageSquare, Target,
  MousePointer2, Pencil, MoveUpRight, Pentagon, CircleDot, Eraser, Undo2, Redo2, Trash2
} from 'lucide-react';

/**
 * 매치로그. 실제 맵 이미지 위에 선수 이동 경로와 자기장을 그린다.
 *
 * 좌표는 맵 한 변을 1 로 둔 비율이라(build_match_log.py) 캔버스 크기와 무관하게
 * 그대로 곱하면 된다. 캔버스 내부 해상도는 SIZE 로 고정하고 화면에서만 늘인다.
 *
 * 맵 이미지는 PUBG 가 API 사용자용으로 공개한 공식 api-assets 저장소에서 받았다
 * (frontend/public/maps/).
 *
 * **화면에 나오는 것은 전부 텔레메트리에서 나온 값이다.** 유일한 예외가 비행
 * 항로인데, 공식 텔레메트리에 비행기 경로 이벤트가 없어서 이륙 직후 선수들의
 * 좌표로 직선을 맞춘 **추정값**이다. 그래서 화면에도 "추정"이라고 적는다.
 */
const SIZE = 1000;

// 팀 구분용 색. 16팀까지 눈으로 구별되는 값으로 골랐다.
const TEAM_COLORS = [
  '#f3a61f', '#00e5ff', '#ff4d6d', '#51cf66', '#c084fc', '#ffd43b',
  '#4dabf7', '#ff922b', '#38d9a9', '#f783ac', '#a9e34b', '#748ffc',
  '#ffa94d', '#63e6be', '#e599f7', '#ff8787'
];

const SPEEDS = [1, 2, 4, 8, 16];
const TICK_MS = 100;
// 경로를 "꼬리"로 그릴 때 남길 시간. 전체 경로는 지도를 덮어 버리고, 점만
// 찍으면 어디서 왔는지 안 보인다. 그 사이를 60초로 잡았다.
const TAIL_SECONDS = 60;

const mmss = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.round(s) % 60).padStart(2, '0')}`;

export default function MatchLogMap({ log, title }) {
  const canvasRef = useRef(null);
  const boxRef = useRef(null);
  const [time, setTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState(4);
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [zoom, setZoom] = useState(1);
  // 그리기 도구. wwcd 의 왼쪽 도구모음에 해당한다. 전부 화면에만 남고
  // 데이터에는 손대지 않는다 — 작전 설명용이다.
  const [tool, setTool] = useState(null);   // pen | arrow | poly | circle | erase | measure
  const [shapes, setShapes] = useState([]);
  const [undone, setUndone] = useState([]);
  const [draft, setDraft] = useState(null); // 그리는 중인 것
  const [phasePick, setPhasePick] = useState(2);   // 페이즈 원 크기

  const [view, setView] = useState({
    names: true,      // 닉네임
    tags: false,      // 이름 앞 팀태그
    centroid: false,  // 팀 무게중심 마커
    grid: false,      // 격자
    feed: true,       // 맵 위 킬 피드
    flight: true,     // 비행 항로(추정)
    trails: false,    // 이동 경로 — 고른 팀은 켜고 끄기와 무관하게 그린다
    kills: true,      // 킬 지점
    fights: true,     // 교전선
    drops: true,      // 보급 상자
  });
  const toggle = k => setView(v => ({ ...v, [k]: !v[k] }));

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

  const teamOf = useMemo(() => {
    const m = new Map();
    for (const t of log?.tracks ?? []) m.set(t.name, t.team || t.nickname);
    return m;
  }, [log]);

  const landingOf = useMemo(() => {
    const m = new Map();
    for (const l of log?.landings ?? []) m.set(l.name, l);
    return m;
  }, [log]);

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

  const phases = useMemo(() => derivePhases(log?.circles), [log]);
  // 페이즈 n 의 자기장 크기. "여기가 다음 자기장이면" 을 그려 보기 위한 것으로,
  // 지어낸 값이 아니라 그 경기에서 실제로 나온 반지름이다.
  const phaseRadii = useMemo(() => phases.map(t => {
    const c = [...(log?.circles ?? [])].reverse().find(x => x.t <= t);
    return c?.r ?? 0.1;
  }), [phases, log]);
  // 항로는 **실측이 있으면 실측**을 쓴다. 비행기에 타고 있던 좌표가 곧 항로이고
  // 오차 0.0m 로 한 직선에 놓인다 (build_match_log.py 의 flight_segment).
  // 그 항목이 없는 옛 로그에서만 좌표로 직선을 맞춘 추정값으로 돌아간다.
  const flight = useMemo(
    () => log?.flightPath ?? deriveFlightPath(log), [log]);
  const flightMeasured = Boolean(log?.flightPath);

  // 지금 벌어지고 있는 교전. 끝난 것은 그리지 않는다 — 쌓이면 지도가 덮인다.
  const fightsNow = useMemo(
    () => (log?.engagements ?? []).filter(e => e.t <= time && time <= e.end + 3),
    [log, time]);

  // 지금 시각까지 일어난 킬. 오른쪽 킬 피드와 지도 표시에 함께 쓴다.
  const killsSoFar = useMemo(
    () => (log?.kills ?? []).filter(k => k.t == null || k.t <= time),
    [log, time]);

  const circle = useMemo(
    () => [...(log?.circles ?? [])].reverse().find(c => c.t <= time),
    [log, time]);

  const phaseNo = useMemo(
    () => phases.filter(p => p <= time).length, [phases, time]);

  /**
   * 그 시각의 순위표. **공식 점수가 아니다** — 매치로그에는 대회 규정이 없다.
   * 살아 있는 팀을 킬 많은 순으로 먼저, 탈락한 팀을 나중에 죽은 순으로 뒤에
   * 놓는다. 배틀로얄에서 순위가 정해지는 방식 그대로라 지어낸 값이 없다.
   */
  const standings = useMemo(() => {
    const rows = teams.map(([name, members]) => {
      const alive = members.filter(p => (deathAt.get(p.name) ?? Infinity) > time).length;
      const out = alive === 0
        ? Math.max(...members.map(p => deathAt.get(p.name) ?? 0)) : null;
      return { name, members, alive, out, kills: 0 };
    });
    const byName = new Map(rows.map(r => [r.name, r]));
    for (const k of killsSoFar) {
      const t = teamOf.get(k.killer);
      if (t && byName.has(t)) byName.get(t).kills += 1;
    }
    rows.sort((a, b) => {
      if (!!a.alive !== !!b.alive) return a.alive ? -1 : 1;
      if (a.alive && b.alive) return b.kills - a.kills || a.name.localeCompare(b.name);
      return b.out - a.out;                       // 늦게 죽은 팀이 높은 순위
    });
    return rows;
  }, [teams, deathAt, killsSoFar, teamOf, time]);

  useEffect(() => {
    // 경기를 바꾸면 그려 둔 것도 치운다. 다른 경기 지도에 남아 있으면 거짓이 된다.
    setTime(0); setPlaying(false); setSelectedPlayer(null);
    setShapes([]); setDraft(null); setUndone([]);
  }, [log]);

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

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !log) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, SIZE, SIZE);
    const px = v => v * SIZE;
    const focusTeam = selectedTeam;
    const focusPlayer = selectedPlayer;
    const focused = Boolean(focusTeam || focusPlayer);

    // 1. 격자 — 1km 간격. mapSize 는 센티미터라 10만 = 1km 다.
    if (view.grid && log.mapSize) {
      const step = 100000 / log.mapSize;
      ctx.strokeStyle = 'rgba(255,255,255,0.13)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let g = step; g < 1; g += step) {
        ctx.moveTo(px(g), 0); ctx.lineTo(px(g), SIZE);
        ctx.moveTo(0, px(g)); ctx.lineTo(SIZE, px(g));
      }
      ctx.stroke();
    }

    // 2. 자기장. 바깥을 어둡게 해서 안전 구역이 드러나게 한다.
    if (circle && circle.r > 0) {
      ctx.save();
      ctx.fillStyle = 'rgba(0, 32, 72, 0.5)';
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
    // 다음 자기장(흰 원). 옛 로그에는 없는 필드라 있을 때만 그린다.
    const next = [...(log.nextCircles ?? [])].reverse().find(c => c.t <= time);
    if (next && next.r > 0) {
      ctx.strokeStyle = 'rgba(255,255,255,0.8)';
      ctx.lineWidth = 1.6;
      ctx.setLineDash([6, 5]);
      ctx.beginPath();
      ctx.arc(px(next.x), px(next.y), px(next.r), 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
    }
    // 레드존. 옛 로그에는 없는 필드라 있을 때만 그린다.
    const red = [...(log.redZones ?? [])].reverse().find(c => c.t <= time && c.t > time - 60);
    if (red && red.r > 0) {
      ctx.fillStyle = 'rgba(255, 60, 60, 0.18)';
      ctx.beginPath();
      ctx.arc(px(red.x), px(red.y), px(red.r), 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = 'rgba(255, 80, 80, 0.7)';
      ctx.lineWidth = 1.4;
      ctx.stroke();
    }

    // 3. 비행 항로(추정). 강하 전 좌표로 맞춘 직선이다.
    if (view.flight && flight) {
      ctx.strokeStyle = 'rgba(255, 90, 90, 0.75)';
      ctx.lineWidth = 2;
      ctx.setLineDash([10, 8]);
      ctx.beginPath();
      ctx.moveTo(px(flight.x1), px(flight.y1));
      ctx.lineTo(px(flight.x2), px(flight.y2));
      ctx.stroke();
      ctx.setLineDash([]);
      // 실측 항로는 비행기가 **실제로 지나간 구간**이라 양 끝이 뜻을 갖는다.
      // 어느 쪽에서 들어왔는지 보이도록 시작점에 표시를 둔다.
      if (flightMeasured) {
        ctx.fillStyle = 'rgba(255, 90, 90, 0.9)';
        ctx.beginPath();
        ctx.arc(px(flight.x1), px(flight.y1), 5, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // 4. 이동 경로와 선수
    for (const [teamName, members] of teams) {
      if (focusTeam && focusTeam !== teamName) continue;
      const color = colorOf.get(teamName);
      const live = [];
      for (const track of members) {
        if (focusPlayer && focusPlayer !== track.name) continue;
        const recorded = track.points.filter(p => p[0] <= time);
        if (!recorded.length) continue;
        // 경로 끝을 보간 지점까지 이어 둔다. 안 그러면 점만 앞서 나가고
        // 선은 최대 10초 뒤에 머문다.
        const here = interpolate(track.points, time);
        const pts = here && here[0] > recorded[recorded.length - 1][0]
          ? [...recorded, here] : recorded;

        // 경로는 **착지한 뒤부터** 긋는다. 위치 기록은 비행기에 타고 있을 때부터
        // 남으므로 그대로 이으면 64명분 항로가 지도를 가로지르는 평행선이 되어
        // 정작 교전 지역을 덮어 버린다. 착지 기록이 없으면 (옛 대회) 종전대로.
        const landedAt = landingOf.get(track.name)?.t;
        let trail = landedAt == null ? pts : pts.filter(p => p[0] >= landedAt);
        // 고른 팀은 전체 경로, 나머지는 최근 60초 꼬리만. 64명분 전체 경로는
        // 지도를 덮어 아무것도 안 보인다.
        if (!focused) trail = trail.filter(p => p[0] >= time - TAIL_SECONDS);

        if ((view.trails || focused) && trail.length > 1) {
          ctx.strokeStyle = color;
          ctx.globalAlpha = focused ? 0.9 : 0.5;
          ctx.lineWidth = focused ? 2.4 : 1.4;
          ctx.beginPath();
          trail.forEach((p, i) => {
            const x = px(p[1]), y = px(p[2]);
            if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
          });
          ctx.stroke();
        }

        // 낙하 지점. 텔레메트리의 착지 기록이 있으면 그걸 쓰고, 없으면 경로의
        // 첫 점으로 대신한다 (경로는 10초 간격이라 착지보다 뒤일 수 있다).
        if (focused) {
          const landed = landingOf.get(track.name);
          const first = landed ? [0, landed.x, landed.y] : pts[0];
          ctx.globalAlpha = 0.8;
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.arc(px(first[1]), px(first[2]), 6, 0, Math.PI * 2);
          ctx.stroke();
        }

        // 현재 위치. 위치 기록이 **10초 간격**이라 그대로 찍으면 점이 뚝뚝
        // 끊긴다. 다음 기록과 사이를 비례로 나눠 그 사이 지점을 그린다.
        const last = pts[pts.length - 1];
        const dead = (deathAt.get(track.name) ?? Infinity) <= time;
        if (!dead) live.push(last);
        ctx.globalAlpha = dead ? 0.3 : 1;
        ctx.fillStyle = last[4] ? '#ff4d6d' : color;   // 기절 상태면 빨강
        ctx.beginPath();
        ctx.arc(px(last[1]), px(last[2]), focused ? 6 : 4, 0, Math.PI * 2);
        ctx.fill();
        if (!dead) {
          ctx.strokeStyle = 'rgba(0,0,0,0.65)';
          ctx.lineWidth = 1.2;
          ctx.stroke();
        }

        if (last[3]) {                                  // 차량 탑승 중이면 테두리
          ctx.globalAlpha = dead ? 0.3 : 1;
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = 1.6;
          ctx.beginPath();
          ctx.arc(px(last[1]), px(last[2]), focused ? 9 : 7, 0, Math.PI * 2);
          ctx.stroke();
        }

        if (view.names && !dead) {
          const label = (view.tags && track.tag ? `[${track.tag}] ` : '') + track.nickname;
          drawLabel(ctx, label, px(last[1]) + 8, px(last[2]) + 4, color);
        }
      }

      // 팀 무게중심 — 팀이 지금 어디에 뭉쳐 있는지 한눈에 본다.
      if (view.centroid && live.length) {
        const cx = live.reduce((s, p) => s + p[1], 0) / live.length;
        const cy = live.reduce((s, p) => s + p[2], 0) / live.length;
        ctx.globalAlpha = 0.9;
        drawLabel(ctx, members[0].tag || teamName, px(cx), px(cy) - 12, color, true);
      }
    }
    ctx.globalAlpha = 1;

    // 5. 교전선 — 가해자에서 피해자로 선을 긋는다. 피해량이 클수록 굵다.
    if (view.fights) {
      for (const f of fightsNow) {
        if (focused) {
          const inFocus = [f.a, f.v].some(n =>
            (focusPlayer && n === focusPlayer) ||
            (focusTeam && teamOf.get(n) === focusTeam));
          if (!inFocus) continue;
        }
        ctx.strokeStyle = 'rgba(255, 77, 109, 0.75)';
        ctx.lineWidth = Math.min(4, 1 + f.dmg / 60);
        ctx.beginPath();
        ctx.moveTo(px(f.ax), px(f.ay));
        ctx.lineTo(px(f.vx), px(f.vy));
        ctx.stroke();
      }
    }

    // 6. 보급 상자 — 떨어진 뒤로는 계속 보인다
    for (const p of (view.drops ? log.packages ?? [] : [])) {
      if (p.t != null && p.t > time) continue;
      ctx.fillStyle = 'rgba(243, 166, 31, 0.9)';
      ctx.fillRect(px(p.x) - 4, px(p.y) - 4, 8, 8);
      ctx.strokeStyle = '#000';
      ctx.lineWidth = 1;
      ctx.strokeRect(px(p.x) - 4, px(p.y) - 4, 8, 8);
    }

    // 7. 킬 지점 — 지금까지 일어난 것만
    if (view.kills) {
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

    // 8. 그려 넣은 것들 — 가장 위에 올린다
    for (const sh of draft ? [...shapes, draft] : shapes) {
      drawShape(ctx, sh, px, log.mapSize);
    }
  }, [log, time, teams, colorOf, teamOf, selectedTeam, selectedPlayer, view,
      circle, killsSoFar, deathAt, fightsNow, landingOf, flight, flightMeasured,
      shapes, draft]);

  const at = e => {
    const r = e.currentTarget.getBoundingClientRect();
    return [(e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height];
  };
  const push = sh => { setShapes(v => [...v, sh]); setUndone([]); };

  const onDown = useCallback(e => {
    if (!tool) return;
    const [x, y] = at(e);
    if (tool === 'pen') { setDraft({ type: 'pen', pts: [[x, y]] }); return; }
    if (tool === 'arrow' || tool === 'measure') {
      setDraft({ type: tool, pts: [[x, y], [x, y]] }); return;
    }
    if (tool === 'circle') { push({ type: 'circle', pts: [[x, y]], r: phaseRadii[phasePick] ?? 0.1 }); return; }
    if (tool === 'poly') {
      // 점을 찍어 가며 만든다. 두 번 누르면 닫는다.
      setDraft(d => (d && d.type === 'poly'
        ? { ...d, pts: [...d.pts, [x, y]] } : { type: 'poly', pts: [[x, y]] }));
      return;
    }
    if (tool === 'erase') {
      setShapes(v => {
        const i = nearestShape(v, x, y);
        if (i < 0) return v;
        const out = v.slice(); out.splice(i, 1); return out;
      });
    }
  }, [tool, phasePick, phaseRadii]);

  const onMove = useCallback(e => {
    if (!draft) return;
    const [x, y] = at(e);
    if (draft.type === 'pen' && e.buttons) {
      setDraft(d => ({ ...d, pts: [...d.pts, [x, y]] }));
    } else if (draft.type === 'arrow' || draft.type === 'measure') {
      setDraft(d => ({ ...d, pts: [d.pts[0], [x, y]] }));
    }
  }, [draft]);

  const onUp = useCallback(() => {
    if (!draft || draft.type === 'poly') return;
    if (draft.pts.length > 1 || draft.type === 'pen') push(draft);
    setDraft(null);
  }, [draft]);

  const closePoly = useCallback(() => {
    if (draft?.type === 'poly' && draft.pts.length > 2) push({ ...draft, closed: true });
    setDraft(null);
  }, [draft]);

  const undo = useCallback(() => {
    setShapes(v => { if (!v.length) return v;
      setUndone(u => [...u, v[v.length - 1]]); return v.slice(0, -1); });
  }, []);
  const redo = useCallback(() => {
    setUndone(u => { if (!u.length) return u;
      setShapes(v => [...v, u[u.length - 1]]); return u.slice(0, -1); });
  }, []);

  // 단축키. wwcd 와 같은 글자를 쓴다 — 손이 기억하는 쪽이 낫다.
  useEffect(() => {
    const onKey = e => {
      if (e.target.tagName === 'INPUT') return;
      if (e.ctrlKey && e.key.toLowerCase() === 'z') { e.preventDefault(); undo(); return; }
      if (e.ctrlKey && e.key.toLowerCase() === 'y') { e.preventDefault(); redo(); return; }
      if (e.shiftKey && e.key === 'Backspace') { setShapes([]); setDraft(null); return; }
      if (e.key === 'Enter') { closePoly(); return; }
      if (e.key === 'Escape') { setDraft(null); setTool(null); return; }
      const k = { v: null, p: 'pen', a: 'arrow', c: 'circle', e: 'erase', m: 'measure' };
      if (e.key.toLowerCase() in k) setTool(k[e.key.toLowerCase()]);
      if (/^[1-9]$/.test(e.key)) setPhasePick(Number(e.key));
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [undo, redo, closePoly]);

  const saveImage = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const out = document.createElement('canvas');
    out.width = SIZE; out.height = SIZE;
    const g = out.getContext('2d');
    g.fillStyle = '#0a0e16';
    g.fillRect(0, 0, SIZE, SIZE);
    const img = boxRef.current?.querySelector('img');
    // 맵 이미지는 같은 출처라 캔버스가 오염되지 않는다.
    if (img && img.naturalWidth) g.drawImage(img, 0, 0, SIZE, SIZE);
    g.drawImage(canvas, 0, 0);
    const a = document.createElement('a');
    a.download = `${log.map}_${Math.round(time)}s.jpg`;
    a.href = out.toDataURL('image/jpeg', 0.92);
    a.click();
  }, [log, time]);

  const goFullscreen = useCallback(() => {
    const el = boxRef.current;
    if (!el) return;
    if (document.fullscreenElement) document.exitFullscreen();
    else el.requestFullscreen?.();
  }, []);

  if (!log) return null;

  const aliveOf = track => (deathAt.get(track.name) ?? Infinity) > time;
  const feedLines = view.feed ? killsSoFar.slice(-5).reverse() : [];

  return (
    <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap', alignItems: 'flex-start' }}>
      <div style={{ flex: '1 1 600px', minWidth: 0, maxWidth: SIZE }}>
        <div ref={boxRef} style={{
          position: 'relative', width: '100%', borderRadius: 'var(--radius-sm)',
          overflow: 'hidden', border: '1px solid var(--border-subtle)', background: '#0a0e16'
        }}>
          <div style={{
            width: '100%', aspectRatio: '1 / 1', overflow: zoom > 1 ? 'auto' : 'hidden'
          }}>
            <div style={{ position: 'relative', width: `${zoom * 100}%`, aspectRatio: '1 / 1' }}>
              <img
                src={`/maps/${log.map}.png`}
                alt={log.mapLabel}
                style={{ width: '100%', aspectRatio: '1 / 1', display: 'block', opacity: 0.9 }}
                onError={e => { e.currentTarget.style.visibility = 'hidden'; }}
              />
              <canvas
                ref={canvasRef}
                width={SIZE}
                height={SIZE}
                onMouseDown={onDown}
                onMouseMove={onMove}
                onMouseUp={onUp}
                onDoubleClick={closePoly}
                style={{ position: 'absolute', inset: 0, width: '100%', height: '100%',
                         cursor: tool ? 'crosshair' : 'default' }}
              />
            </div>
          </div>

          {/* 지도 위 머리말 */}
          <div style={{ position: 'absolute', top: 10, left: 10, display: 'flex',
                        gap: '8px', alignItems: 'center', pointerEvents: 'none' }}>
            <Badge accent>PHASE {phaseNo || 1}</Badge>
            <Badge>{title ? `${title} · ` : ''}{log.mapLabel}</Badge>
          </div>
          <div style={{ position: 'absolute', top: 10, right: 10, pointerEvents: 'none' }}>
            <Badge>생존 {circle?.alive ?? '-'}명 · {circle?.aliveTeams ?? '-'}팀</Badge>
          </div>

          {/* 지도 위 킬 피드 */}
          {feedLines.length > 0 && (
            <div style={{ position: 'absolute', top: 46, right: 10, display: 'flex',
                          flexDirection: 'column', gap: '3px', pointerEvents: 'none',
                          alignItems: 'flex-end' }}>
              {feedLines.map((k, i) => (
                <div key={i} style={{
                  background: 'rgba(8,12,20,0.78)', borderRadius: '4px',
                  padding: '3px 8px', fontSize: '0.72rem', color: 'var(--text-muted)',
                  display: 'flex', gap: '6px', alignItems: 'center',
                  opacity: 1 - i * 0.16
                }}>
                  <span style={{ color: '#fff', fontWeight: 700 }}>{short(k.killer)}</span>
                  <Crosshair size={10} color="#ff4d6d" />
                  <span>{short(k.victim)}</span>
                </div>
              ))}
            </div>
          )}

          {/* 보기 도구 — 지도 오른쪽에 붙인다 */}
          <div style={{ position: 'absolute', bottom: 10, right: 10, display: 'flex',
                        flexDirection: 'column', gap: '4px' }}>
            <IconBtn on={view.names} onClick={() => toggle('names')} icon={Users} title="닉네임 표시" />
            <IconBtn on={view.tags} onClick={() => toggle('tags')} icon={Tag} title="이름 앞 팀태그" />
            <IconBtn on={view.centroid} onClick={() => toggle('centroid')} icon={Target} title="팀 무게중심" />
            <IconBtn on={view.grid} onClick={() => toggle('grid')} icon={Grid3x3} title="격자 (1km)" />
            <IconBtn on={view.feed} onClick={() => toggle('feed')} icon={MessageSquare} title="맵 위 킬 피드" />
            <IconBtn on={view.flight} onClick={() => toggle('flight')} icon={Plane}
                     title={flightMeasured
                       ? '비행 항로 — 비행기에 타고 있던 좌표로 구한 실제 항로'
                       : '비행 항로 — 이 경기에는 비행기 기록이 없어 강하 전 좌표로 맞춘 추정값'} />
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
                ...ctrlBtn, padding: '7px 9px',
                background: speed === s ? 'var(--accent-gold)' : 'rgba(255,255,255,0.05)',
                color: speed === s ? '#000' : '#fff', fontWeight: '800'
              }}>{s}x</button>
            ))}
          </div>
          <span style={{ color: 'var(--accent-gold)', fontWeight: '900', fontVariantNumeric: 'tabular-nums' }}>
            {mmss(time)} / {mmss(duration)}
          </span>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '4px' }}>
            <IconBtn on={!tool} onClick={() => { setTool(null); setDraft(null); }}
                     icon={MousePointer2} title="선택/이동 (V)" />
            <IconBtn on={tool === 'pen'} onClick={() => setTool('pen')} icon={Pencil} title="펜 (P)" />
            <IconBtn on={tool === 'arrow'} onClick={() => setTool('arrow')}
                     icon={MoveUpRight} title="화살표 — 이동 경로를 그린다 (A)" />
            <IconBtn on={tool === 'poly'} onClick={() => setTool('poly')}
                     icon={Pentagon} title="영역 — 점을 찍고 Enter 나 더블클릭으로 닫는다" />
            <IconBtn on={tool === 'circle'} onClick={() => setTool('circle')}
                     icon={CircleDot} title={`페이즈 원 — 누른 곳에 P${phasePick} 크기 원 (C, 숫자로 페이즈 선택)`} />
            <IconBtn on={tool === 'erase'} onClick={() => setTool('erase')}
                     icon={Eraser} title="지우개 — 눌러서 지운다 (E)" />
            <IconBtn on={tool === 'measure'} onClick={() => setTool('measure')}
                     icon={Ruler} title="거리 측정 — 끌어서 잰다 (M)" />
            <IconBtn onClick={undo} icon={Undo2} title="되돌리기 (Ctrl+Z)" />
            <IconBtn onClick={redo} icon={Redo2} title="다시 실행 (Ctrl+Y)" />
            <IconBtn onClick={() => { setShapes([]); setDraft(null); }}
                     icon={Trash2} title="그림 전체 지우기 (Shift+Backspace)" />
            <IconBtn onClick={saveImage} icon={Camera} title="현재 화면 저장 (JPG)" />
            <IconBtn onClick={goFullscreen} icon={Maximize2} title="전체화면 (ESC 로 종료)" />
          </div>
        </div>

        {/* 진행 막대 — 자기장 페이즈가 어디서 시작하는지 눈금으로 보여준다 */}
        <div style={{ position: 'relative', marginTop: '10px' }}>
          <div style={{ position: 'relative', height: '12px' }}>
            {phases.map((t, i) => (
              <span key={i} title={`PHASE ${i + 1} · ${mmss(t)}`} style={{
                position: 'absolute', left: `${(t / duration) * 100}%`, top: 0,
                transform: 'translateX(-50%)', fontSize: '0.6rem',
                color: 'var(--text-muted)', fontWeight: 800
              }}>P{i + 1}</span>
            ))}
          </div>
          <input
            type="range" min={0} max={duration} value={Math.round(time)}
            onChange={e => { setPlaying(false); setTime(Number(e.target.value)); }}
            style={{ width: '100%', accentColor: 'var(--accent-gold)' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '14px', marginTop: '8px', fontSize: '0.8rem',
                      color: 'var(--text-muted)', flexWrap: 'wrap', alignItems: 'center' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <Skull size={14} /> 킬 {killsSoFar.length} / {log.kills?.length ?? 0}
          </span>
          <Toggle on={view.trails} set={() => toggle('trails')} icon={Route} label="이동 경로" />
          <Toggle on={view.kills} set={() => toggle('kills')} icon={Crosshair} label="킬 지점" />
          <Toggle on={view.fights} set={() => toggle('fights')} icon={Swords} label="교전" />
          <Toggle on={view.drops} set={() => toggle('drops')} icon={Package} label="보급" />
          <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <ZoomIn size={14} />
            <input type="range" min={1} max={4} step={0.5} value={zoom}
                   onChange={e => setZoom(Number(e.target.value))}
                   style={{ width: '70px', accentColor: 'var(--accent-gold)' }} />
            {zoom}x
          </label>
        </div>
      </div>

      {/* 순위·킬 로그 */}
      <div style={{ flex: '1 1 270px', minWidth: '250px', display: 'flex',
                    flexDirection: 'column', gap: '12px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.82rem', color: '#fff', fontWeight: 900 }}>순위</span>
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
              생존 팀이 먼저, 탈락 팀은 늦게 죽은 순 · 대회 점수는 아닙니다
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2px',
                        maxHeight: '460px', overflowY: 'auto' }}>
            {standings.map((row, i) => {
              const on = selectedTeam === row.name;
              return (
                <div key={row.name}>
                  <button
                    onClick={() => { setSelectedTeam(on ? null : row.name); setSelectedPlayer(null); }}
                    style={{
                      display: 'flex', alignItems: 'center', gap: '8px', width: '100%',
                      padding: '6px 9px', borderRadius: 'var(--radius-sm)',
                      background: on ? 'rgba(243,166,31,0.12)' : 'rgba(255,255,255,0.03)',
                      border: `1px solid ${on ? 'rgba(243,166,31,0.5)' : 'var(--border-subtle)'}`,
                      color: row.alive ? '#fff' : 'var(--text-muted)',
                      fontSize: '0.8rem', fontWeight: '700', cursor: 'pointer', textAlign: 'left',
                      opacity: row.alive ? 1 : 0.55
                    }}>
                    <span style={{ width: '18px', textAlign: 'right', opacity: 0.7,
                                   fontVariantNumeric: 'tabular-nums' }}>{i + 1}</span>
                    <span style={{ width: '9px', height: '9px', borderRadius: '50%',
                                   background: colorOf.get(row.name), flexShrink: 0 }} />
                    <span style={{ overflow: 'hidden', textOverflow: 'ellipsis',
                                   whiteSpace: 'nowrap' }}>{row.name}</span>
                    <span style={{ marginLeft: 'auto', fontSize: '0.74rem',
                                   color: row.alive ? 'var(--accent-gold)' : 'inherit' }}>
                      {row.alive}/{row.members.length}
                    </span>
                    <span style={{ width: '22px', textAlign: 'right', fontSize: '0.74rem',
                                   fontVariantNumeric: 'tabular-nums' }}>{row.kills}</span>
                  </button>
                  {on && (
                    <div style={{ padding: '4px 0 4px 18px', display: 'flex',
                                  flexDirection: 'column', gap: '2px' }}>
                      {row.members.map(p => {
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

/**
 * 자기장 페이즈가 시작하는 시각들.
 *
 * 공식 텔레메트리는 "지금 몇 페이즈"를 알려주지 않는다. 대신 안전 구역 반경이
 * **줄어들다 멈추는 순간**이 다음 구역이 예고된 때다. 그 지점을 세면 P1~P8 이
 * 나온다 (PGS 9 결승 1경기에서 9개, 위키의 페이즈 수와 같다).
 */
function derivePhases(circles) {
  if (!circles?.length) return [];
  const out = [circles[0].t];
  let shrinking = false;
  for (let i = 1; i < circles.length; i += 1) {
    if (circles[i].r < circles[i - 1].r - 1e-9) shrinking = true;
    else if (shrinking) { out.push(circles[i].t); shrinking = false; }
  }
  return out;
}

/**
 * 비행 항로 — **추정값이다.**
 *
 * 공식 텔레메트리에 비행기 경로 이벤트가 없다. 대신 아무도 뛰어내리기 전
 * (= 첫 착지 시각 이전) 선수 좌표는 전부 비행기 위에 있으므로 한 직선에
 * 놓인다. 그 점들에 주성분으로 직선을 맞추고, 많이 벗어난 30%를 버린 뒤 한 번
 * 더 맞춘다. 실측으로 중앙값 오차가 8km 맵에서 3~130m 였다.
 *
 * 착지 기록이 없는 옛 대회에서는 null 을 돌려주고 화면에도 그리지 않는다.
 */
function deriveFlightPath(log) {
  const landings = log?.landings ?? [];
  if (!landings.length || !log?.tracks?.length) return null;
  const until = Math.min(...landings.map(l => l.t));
  let pts = [];
  for (const tr of log.tracks) {
    for (const p of tr.points) {
      if (p[0] >= 1 && p[0] <= until) pts.push([p[1], p[2]]);
    }
  }
  if (pts.length < 20) return null;

  let line = fitLine(pts);
  if (!line) return null;
  // 일찍 뛴 선수는 벌써 비행기에서 떨어져 나와 있다. 많이 벗어난 점을 버린다.
  const scored = pts
    .map(p => [Math.abs(-(p[0] - line.mx) * line.dy + (p[1] - line.my) * line.dx), p])
    .sort((a, b) => a[0] - b[0]);
  pts = scored.slice(0, Math.max(20, Math.floor(scored.length * 0.7))).map(s => s[1]);
  line = fitLine(pts) || line;

  // 맵 끝까지 늘인다. 비행기는 맵을 가로지른다.
  const k = 2;
  return {
    x1: line.mx - line.dx * k, y1: line.my - line.dy * k,
    x2: line.mx + line.dx * k, y2: line.my + line.dy * k,
  };
}

function fitLine(pts) {
  const n = pts.length;
  if (!n) return null;
  const mx = pts.reduce((s, p) => s + p[0], 0) / n;
  const my = pts.reduce((s, p) => s + p[1], 0) / n;
  let sxx = 0, syy = 0, sxy = 0;
  for (const p of pts) {
    sxx += (p[0] - mx) ** 2; syy += (p[1] - my) ** 2;
    sxy += (p[0] - mx) * (p[1] - my);
  }
  const th = 0.5 * Math.atan2(2 * sxy / n, (sxx - syy) / n);
  return { mx, my, dx: Math.cos(th), dy: Math.sin(th) };
}

/** 그려 넣은 도형 하나. 전부 화면에만 있고 데이터에는 안 들어간다. */
function drawShape(ctx, sh, px, mapSize) {
  const C = '#ffd43b';
  ctx.strokeStyle = C;
  ctx.fillStyle = 'rgba(255, 212, 59, 0.16)';
  ctx.lineWidth = 2.5;
  ctx.setLineDash([]);
  const P = sh.pts;
  if (sh.type === 'pen' || sh.type === 'poly') {
    ctx.beginPath();
    P.forEach(([x, y], i) => (i ? ctx.lineTo(px(x), px(y)) : ctx.moveTo(px(x), px(y))));
    if (sh.closed) { ctx.closePath(); ctx.fill(); }
    ctx.stroke();
    if (sh.type === 'poly' && !sh.closed) {
      for (const [x, y] of P) {
        ctx.beginPath(); ctx.arc(px(x), px(y), 3, 0, Math.PI * 2); ctx.fillStyle = C; ctx.fill();
      }
    }
    return;
  }
  if (sh.type === 'circle') {
    ctx.beginPath();
    ctx.arc(px(P[0][0]), px(P[0][1]), px(sh.r), 0, Math.PI * 2);
    ctx.fill(); ctx.stroke();
    return;
  }
  // 화살표와 자
  const [a, b] = P;
  ctx.beginPath();
  if (sh.type === 'measure') ctx.setLineDash([6, 5]);
  ctx.moveTo(px(a[0]), px(a[1]));
  ctx.lineTo(px(b[0]), px(b[1]));
  ctx.stroke();
  ctx.setLineDash([]);
  if (sh.type === 'arrow') {
    const th = Math.atan2(b[1] - a[1], b[0] - a[0]);
    const h = 14;
    ctx.beginPath();
    ctx.moveTo(px(b[0]), px(b[1]));
    ctx.lineTo(px(b[0]) - h * Math.cos(th - 0.4), px(b[1]) - h * Math.sin(th - 0.4));
    ctx.lineTo(px(b[0]) - h * Math.cos(th + 0.4), px(b[1]) - h * Math.sin(th + 0.4));
    ctx.closePath(); ctx.fillStyle = C; ctx.fill();
  } else {
    const m = { ax: a[0], ay: a[1], bx: b[0], by: b[1] };
    drawLabel(ctx, `${distanceMeters(m, mapSize)}m`,
              px((a[0] + b[0]) / 2) + 8, px((a[1] + b[1]) / 2), C, true);
  }
}

/** 누른 자리에 가장 가까운 도형. 지우개가 쓴다. 없으면 -1. */
function nearestShape(shapes, x, y) {
  let best = -1, bestD = 0.02;            // 맵 한 변의 2% 안쪽만 집는다
  shapes.forEach((sh, i) => {
    for (const [px_, py] of sh.pts) {
      const d = Math.hypot(px_ - x, py - y);
      if (d < bestD) { bestD = d; best = i; }
    }
    if (sh.type === 'circle') {
      const d = Math.abs(Math.hypot(sh.pts[0][0] - x, sh.pts[0][1] - y) - sh.r);
      if (d < bestD) { bestD = d; best = i; }
    }
  });
  return best;
}

/** 두 점 사이 거리(미터). mapSize 는 센티미터다. */
function distanceMeters(m, mapSize) {
  if (!mapSize || m.bx == null) return 0;
  const dx = (m.bx - m.ax) * mapSize / 100;
  const dy = (m.by - m.ay) * mapSize / 100;
  return Math.round(Math.hypot(dx, dy));
}

/** 지도 위 글자는 배경 없이 두면 지형에 묻힌다. 테두리를 깔고 쓴다. */
function drawLabel(ctx, text, x, y, color, center) {
  ctx.font = '700 13px sans-serif';
  ctx.textAlign = center ? 'center' : 'left';
  ctx.lineWidth = 3;
  ctx.strokeStyle = 'rgba(0,0,0,0.85)';
  ctx.strokeText(text, x, y);
  ctx.fillStyle = color || '#fff';
  ctx.fillText(text, x, y);
  ctx.textAlign = 'left';
}

/**
 * 그 시각의 위치를 앞뒤 기록 사이에서 비례로 구한다.
 *
 * 텔레메트리의 위치 기록은 10초 간격이다 (PUBG 가 그렇게만 준다 — 우리가
 * 줄인 것이 아니다). 보간하지 않으면 재생할 때 10초마다 한 번씩 순간이동한다.
 */
function interpolate(points, t) {
  if (!points?.length) return null;
  if (t <= points[0][0]) return points[0];
  let lo = 0, hi = points.length - 1;
  if (t >= points[hi][0]) return points[hi];
  while (lo + 1 < hi) {                      // 이분 탐색 — 점이 180개라 선형도
    const mid = (lo + hi) >> 1;              // 되지만 64명 x 매 프레임이라 아낀다
    if (points[mid][0] <= t) lo = mid; else hi = mid;
  }
  const a = points[lo], b = points[hi];
  const span = b[0] - a[0];
  if (span <= 0) return a;
  const r = (t - a[0]) / span;
  // 차량·기절 여부는 섞지 않고 앞 기록의 값을 쓴다. 중간값이 없는 상태값이다.
  return [t, a[1] + (b[1] - a[1]) * r, a[2] + (b[2] - a[2]) * r, a[3], a[4]];
}

/** 인게임 아이디에서 접두사를 떼어 닉네임만 보여준다. */
function short(name) {
  if (!name) return '—';
  const i = name.indexOf('_');
  return i > 0 ? name.slice(i + 1) : name;
}

function Badge({ children, accent }) {
  return (
    <span style={{
      background: accent ? 'rgba(243,166,31,0.9)' : 'rgba(8,12,20,0.8)',
      color: accent ? '#000' : '#fff',
      padding: '3px 9px', borderRadius: '4px',
      fontSize: '0.72rem', fontWeight: 900, letterSpacing: '0.02em'
    }}>{children}</span>
  );
}

function IconBtn({ on, onClick, icon: Icon, title }) {
  return (
    <button onClick={onClick} title={title} style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      width: '30px', height: '30px', borderRadius: 'var(--radius-sm)',
      background: on ? 'rgba(243,166,31,0.2)' : 'rgba(8,12,20,0.75)',
      border: `1px solid ${on ? 'rgba(243,166,31,0.6)' : 'var(--border-subtle)'}`,
      color: on ? 'var(--accent-gold)' : 'var(--text-muted)', cursor: 'pointer'
    }}>
      <Icon size={15} />
    </button>
  );
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
