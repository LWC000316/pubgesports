import React, { useState } from 'react';
import { Zap, Trophy, Crosshair, Flame, Play, Shield, Target, Award } from 'lucide-react';

export default function HitEndingTab() {
  const [selectedTournament, setSelectedTournament] = useState('pgs4');

  const HIT_ENDINGS_DATA = [
    {
      id: 'm18',
      matchNumber: '그랜드 파이널 매치 18 (최종 피날레)',
      map: 'Erangel (에란겔)',
      winnerTeam: 'Twisted Minds',
      runnerUpTeam: 'CERBERUS Esports',
      endingKiller: 'Xmpl',
      endingWeapon: 'Beryl M762',
      endingZone: 'Phase 9 (야스나야 남쪽 능선)',
      clutchType: '2 vs 3 진영 역전 치킨',
      description: '마지막 자기장 수축 순간, Xmpl 선수가 연막 속에서 침착하게 헤드샷 2킬을 꽂아 넣으며 우승을 확정 지은 결정적 히트엔딩 장면입니다.'
    },
    {
      id: 'm12',
      matchNumber: '그랜드 파이널 매치 12',
      map: 'Miramar (미라마)',
      winnerTeam: 'Danawa e-sports',
      runnerUpTeam: 'Soniqs',
      endingKiller: 'seoul',
      endingWeapon: 'Mini14 & M416',
      endingZone: 'Phase 8 (추마세라 언덕 바위)',
      clutchType: '1 vs 2 솔로 클러치 엔딩',
      description: '적의 양각 포위 상황에서 단독 생존한 seoul 선수가 완벽한 바위 핑퐁 샷으로 상대 2명을 차례로 제압하며 기적적인 치킨을 가져왔습니다.'
    },
    {
      id: 'm7',
      matchNumber: '그랜드 파이널 매치 7',
      map: 'Rondo (론도)',
      winnerTeam: 'Kwangdong Freecs',
      runnerUpTeam: '17Gaming',
      endingKiller: 'Salute',
      endingWeapon: 'ACE32',
      endingZone: 'Phase 9 (중앙 대나무 숲)',
      clutchType: '4 vs 4 풀 스쿼드 정면 힘싸움',
      description: '투척 무기 세례 속에서 Salute 선수가 기절 위기를 뚫고 상대 주력 딜러를 먼저 끊어내며 수적 우위를 점한 교전 엔딩입니다.'
    },
    {
      id: 'm3',
      matchNumber: '그랜드 파이널 매치 3',
      map: 'Taego (태고)',
      winnerTeam: 'Soniqs',
      runnerUpTeam: 'Four Angry Men',
      endingKiller: 'TGLTN',
      endingWeapon: 'Aug',
      endingZone: 'Phase 8 (평원 해바라기 밭)',
      clutchType: '3 vs 2 포위 섬멸 엔딩',
      description: '고지대 이점을 쥐고 있던 TGLTN 선수의 정밀한 장거리 스프레이로 적의 진입로를 완벽 봉쇄하며 승리를 확정 지었습니다.'
    }
  ];

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px' }}>
      
      {/* 상단 소개 배너 */}
      <div className="glass-panel" style={{
        padding: '24px 28px',
        borderRadius: 'var(--radius-md)',
        marginBottom: '28px',
        background: 'linear-gradient(135deg, rgba(255, 51, 75, 0.12) 0%, rgba(22, 26, 38, 0.95) 100%)',
        border: '1px solid rgba(255, 51, 75, 0.3)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '10px',
            background: 'rgba(255, 51, 75, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <Zap size={26} color="var(--accent-red)" />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h2 style={{ fontSize: '1.45rem', fontWeight: '900', color: '#fff', margin: 0 }}>
                HIT ENDING (히트엔딩 아카이브)
              </h2>
              <span className="badge badge-red" style={{ fontSize: '0.72rem' }}>FINAL CIRCLE & CLUTCH</span>
            </div>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', margin: '4px 0 0 0' }}>
              매치의 승패를 결정지은 마지막 자기장 페이즈 8, 9의 치킨 결정 순간 및 슈퍼 플레이 클러치 로그
            </p>
          </div>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          padding: '10px 18px',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(0, 0, 0, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.08)'
        }}>
          <Trophy size={18} color="var(--accent-gold)" />
          <span style={{ fontSize: '0.9rem', color: '#fff', fontWeight: '800' }}>PGS 4 그랜드 파이널</span>
        </div>
      </div>

      {/* 히트엔딩 매치 피날레 카드 목록 */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {HIT_ENDINGS_DATA.map((ending) => (
          <div
            key={ending.id}
            className="glass-panel"
            style={{
              padding: '24px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
              transition: 'all 0.2s ease',
              display: 'flex',
              flexDirection: 'column',
              gap: '18px'
            }}
            onMouseEnter={e => e.currentTarget.style.borderColor = 'rgba(255, 51, 75, 0.4)'}
            onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--border-subtle)'}
          >
            {/* 상단 매치 정보 헤더 */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderBottom: '1px solid rgba(255, 255, 255, 0.06)',
              paddingBottom: '14px',
              flexWrap: 'wrap',
              gap: '10px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{
                  padding: '4px 10px',
                  borderRadius: '4px',
                  background: 'rgba(243, 166, 31, 0.15)',
                  color: 'var(--accent-gold)',
                  fontWeight: '800',
                  fontSize: '0.82rem'
                }}>
                  {ending.map}
                </span>
                <span style={{ fontSize: '1.15rem', fontWeight: '900', color: '#fff' }}>
                  {ending.matchNumber}
                </span>
              </div>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '4px 12px',
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(255, 51, 75, 0.15)',
                color: 'var(--accent-red)',
                fontSize: '0.8rem',
                fontWeight: '800'
              }}>
                <Crosshair size={14} />
                <span>{ending.clutchType}</span>
              </div>
            </div>

            {/* 본문: 치킨 팀 vs 준우승 팀 & 결정타 */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
              gap: '16px',
              alignItems: 'center'
            }}>
              {/* 치킨 승리팀 */}
              <div style={{
                padding: '16px',
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(243, 166, 31, 0.06)',
                border: '1px solid rgba(243, 166, 31, 0.2)'
              }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', fontWeight: '800', marginBottom: '4px' }}>
                  WINNER 치킨 획득 (WWCD) 🍗
                </div>
                <div style={{ fontSize: '1.3rem', fontWeight: '900', color: '#fff' }}>
                  {ending.winnerTeam}
                </div>
              </div>

              {/* 엔딩 킬러 & 무기 */}
              <div style={{
                padding: '16px',
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(0, 229, 255, 0.05)',
                border: '1px solid rgba(0, 229, 255, 0.2)'
              }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--accent-cyan)', fontWeight: '800', marginBottom: '4px' }}>
                  엔딩 결정타 (KILLER & WEAPON)
                </div>
                <div style={{ fontSize: '1.2rem', fontWeight: '900', color: '#fff' }}>
                  {ending.endingKiller} <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: '500' }}>({ending.endingWeapon})</span>
                </div>
              </div>

              {/* 엔딩 서클 위치 */}
              <div style={{
                padding: '16px',
                borderRadius: 'var(--radius-sm)',
                background: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid rgba(255, 255, 255, 0.05)'
              }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '800', marginBottom: '4px' }}>
                  최종 자기장 위치
                </div>
                <div style={{ fontSize: '0.95rem', fontWeight: '700', color: '#eee' }}>
                  {ending.endingZone}
                </div>
              </div>
            </div>

            {/* 교전 서술 */}
            <div style={{
              fontSize: '0.88rem',
              color: 'var(--text-muted)',
              lineHeight: '1.6',
              padding: '12px 16px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(0, 0, 0, 0.2)'
            }}>
              {ending.description}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
