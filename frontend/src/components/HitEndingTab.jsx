import React from 'react';
import { Crosshair, Map, Layers, Film } from 'lucide-react';

/**
 * 히트엔딩 탭 — 준비 중.
 *
 * 이전 구현은 실존 프로 선수(Xmpl, seoul, Salute, TGLTN)에 대한 출처 없는
 * 경기 서술을 컴포넌트에 하드코딩해 두고 있었다. 검증할 근거가 없는 내용이라
 * 제거했다.
 *
 * 만들 것: 매치 텔레메트리의 LogGameStatePeriodic(안전지대 좌표·반지름)을
 * 다수 경기에 걸쳐 집계해, 맵 이미지 위에 서클 축소 양상과 지형별 편향
 * (어느 지역이 서클에 자주 걸치는가)을 이미지·영상으로 보여준다.
 *
 * 선행 조건: 반복 실행 가능한 텔레메트리 수집 파이프라인.
 * 공식 텔레메트리 URL 은 primary_data/match_*.json 의 asset 항목에 들어 있다.
 */

const PLANNED = [
  {
    icon: Crosshair,
    title: '서클 축소 재생',
    detail: '매치별 안전지대 좌표와 반지름 변화를 단계별로 추적해 재생합니다.'
  },
  {
    icon: Layers,
    title: '지형 편향 분석',
    detail: '다수 경기를 집계해 어느 지역이 서클에 자주 포함되는지 히트맵으로 표시합니다.'
  },
  {
    icon: Map,
    title: '맵별 비교',
    detail: '에란겔·미라마·태고·론도 등 맵별로 서클 형성 경향을 비교합니다.'
  },
  {
    icon: Film,
    title: '이미지 · 영상 출력',
    detail: '분석 결과를 이미지와 영상으로 내보내 공유할 수 있게 합니다.'
  }
];

export default function HitEndingTab() {
  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      <div className="glass-panel" style={{
        padding: '40px 28px',
        borderRadius: 'var(--radius-md)',
        marginBottom: '24px',
        textAlign: 'center',
        border: '1px solid rgba(243, 166, 31, 0.25)',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.08) 0%, rgba(22, 26, 38, 0.95) 100%)'
      }}>
        <Crosshair size={40} color="var(--accent-gold)" style={{ marginBottom: '16px' }} />
        <h2 style={{ fontSize: '1.4rem', fontWeight: '900', color: '#fff', margin: '0 0 10px' }}>
          히트엔딩 · 준비 중
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem', maxWidth: '620px', margin: '0 auto', lineHeight: 1.6 }}>
          공식 매치 텔레메트리를 기반으로 서클이 어떻게 줄었고 어느 지형이 서클에
          많이 걸치는지 분석하는 기능입니다. 텔레메트리 수집 파이프라인 구축 후 공개됩니다.
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '16px'
      }}>
        {PLANNED.map(({ icon: Icon, title, detail }) => (
          <div
            key={title}
            className="glass-panel"
            style={{
              padding: '20px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
              opacity: 0.75
            }}
          >
            <Icon size={20} color="var(--accent-gold)" style={{ marginBottom: '12px' }} />
            <div style={{ fontWeight: '800', color: '#fff', fontSize: '0.98rem', marginBottom: '6px' }}>
              {title}
            </div>
            <div style={{ color: 'var(--text-muted)', fontSize: '0.84rem', lineHeight: 1.5 }}>
              {detail}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
