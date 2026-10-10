import React, { useMemo, useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

// 항목별로 오름차순·내림차순 정렬할 수 있다. 기본은 OVERALL 내림차순.
const COLUMNS = [
  { key: 'nickname', label: '선수', align: 'left', width: '1.4fr', text: true },
  { key: 'team', label: '팀', align: 'left', width: '1fr', text: true },
  { key: 'matches', label: '매치', width: '60px' },
  { key: 'overall', label: 'OVERALL', width: '92px', accent: true },
  { key: 'kills', label: '킬', width: '60px' },
  { key: 'avgDamage', label: '평균 데미지', width: '100px' },
  { key: 'avgSurvival', label: '평균 생존', width: '92px', time: true },
  { key: 'knocks', label: '기절', width: '60px' },
  { key: 'assists', label: '어시', width: '60px' },
  { key: 'headshots', label: '헤드샷', width: '70px' },
  { key: 'longestKill', label: '최장 킬', width: '80px', suffix: 'm' }
];

const GRID = COLUMNS.map(c => c.width).join(' ');

export default function PlayerStatsTable({ rows }) {
  // 배틀로얄이 아닌 단계(TDM·아레나 등)는 OVERALL 이 전부 비어 있다. 그걸로
  // 정렬하면 아무 순서도 나오지 않으므로 킬로 연다.
  const hasOverall = (rows ?? []).some(r => r.overall !== null && r.overall !== undefined);
  const [sort, setSort] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const active = sort ?? { key: hasOverall ? 'overall' : 'kills', dir: 'desc' };

  const sorted = useMemo(() => {
    const col = COLUMNS.find(c => c.key === active.key);
    const out = [...(rows ?? [])];
    out.sort((a, b) => {
      const av = a[active.key], bv = b[active.key];
      let cmp;
      if (col?.text) cmp = String(av ?? '').localeCompare(String(bv ?? ''));
      else cmp = (av ?? 0) - (bv ?? 0);
      return active.dir === 'asc' ? cmp : -cmp;
    });
    return out;
  }, [rows, active]);

  if (!rows || rows.length === 0) return null;
  const shown = expanded ? sorted : sorted.slice(0, 20);

  const toggle = key => setSort(
    active.key === key
      ? { key, dir: active.dir === 'desc' ? 'asc' : 'desc' }
      // 이름·팀은 가나다순부터, 숫자는 큰 값부터 보는 게 자연스럽다.
      : { key, dir: COLUMNS.find(c => c.key === key)?.text ? 'asc' : 'desc' });

  return (
    <div>
      <div className="glass-panel" style={{ borderRadius: 'var(--radius-sm)', overflowX: 'auto' }}>
        <div style={{ minWidth: '960px' }}>
          <div style={{
            display: 'grid',
            gridTemplateColumns: `48px ${GRID}`,
            padding: '10px 16px',
            background: 'rgba(255,255,255,0.03)',
            fontSize: '0.73rem',
            fontWeight: '800',
            color: 'var(--text-muted)',
            letterSpacing: '0.03em'
          }}>
            <span>#</span>
            {COLUMNS.map(c => {
              const on = active.key === c.key;
              return (
                <button
                  key={c.key}
                  onClick={() => toggle(c.key)}
                  title="눌러서 정렬 방향을 바꿉니다"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '3px',
                    justifyContent: c.align === 'left' ? 'flex-start' : 'flex-end',
                    background: 'none',
                    border: 'none',
                    padding: 0,
                    cursor: 'pointer',
                    color: on ? 'var(--accent-gold)' : 'var(--text-muted)',
                    fontSize: '0.73rem',
                    fontWeight: '800',
                    textTransform: 'uppercase',
                    letterSpacing: '0.03em'
                  }}
                >
                  {c.label}
                  {on && (active.dir === 'desc' ? <ChevronDown size={12} /> : <ChevronUp size={12} />)}
                </button>
              );
            })}
          </div>

          {shown.map((p, i) => (
            <div
              key={`${p.nickname}-${p.team}`}
              style={{
                display: 'grid',
                gridTemplateColumns: `48px ${GRID}`,
                padding: '10px 16px',
                borderTop: '1px solid rgba(255,255,255,0.04)',
                alignItems: 'center',
                fontSize: '0.85rem'
              }}
            >
              <span style={{ fontWeight: '900', color: i < 3 ? 'var(--accent-gold)' : 'var(--text-muted)' }}>
                {i + 1}
              </span>
              {COLUMNS.map(c => (
                <span
                  key={c.key}
                  style={{
                    textAlign: c.align === 'left' ? 'left' : 'right',
                    color: c.accent ? 'var(--accent-gold)'
                      : c.key === 'nickname' ? '#fff' : 'var(--text-muted)',
                    fontWeight: c.accent || c.key === 'nickname' ? '800' : '600'
                  }}
                >
                  {format(p[c.key], c)}
                </span>
              ))}
            </div>
          ))}
        </div>
      </div>

      {sorted.length > 20 && (
        <button
          onClick={() => setExpanded(v => !v)}
          style={{
            marginTop: '10px',
            padding: '8px 16px',
            borderRadius: 'var(--radius-sm)',
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-muted)',
            fontSize: '0.8rem',
            fontWeight: '700',
            cursor: 'pointer'
          }}
        >
          {expanded ? '접기' : `전체 ${sorted.length}명 보기`}
        </button>
      )}
    </div>
  );
}

function format(value, col) {
  if (value === null || value === undefined || value === '') return '-';
  if (col.time) {
    const m = Math.floor(value / 60), s = value % 60;
    return `${m}:${String(s).padStart(2, '0')}`;
  }
  if (typeof value === 'number' && !Number.isInteger(value)) {
    return Math.round(value) + (col.suffix ?? '');
  }
  return value + (col.suffix ?? '');
}
