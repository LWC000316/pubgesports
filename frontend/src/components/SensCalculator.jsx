import React, { useState } from 'react';
import { Calculator, Crosshair, ArrowRightLeft, Sparkles, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function SensCalculator() {
  // PUBG 15스텝 변환 상태
  const [currentDpi, setCurrentDpi] = useState(800);
  const [generalSens, setGeneralSens] = useState(30);
  const [aimingSens, setAimingSens] = useState(30);
  const [adsSens, setAdsSens] = useState(30);
  const [verticalMultiplier, setVerticalMultiplier] = useState(1.0);

  // 타 FPS 변환 상태
  const [sourceGame, setSourceGame] = useState('VALORANT');
  const [sourceSens, setSourceSens] = useState(0.4);
  const [targetPubgDpi, setTargetPubgDpi] = useState(800);

  // 15스텝 변환 계산 함수
  // 400 DPI -> 800 DPI: -15
  // 800 DPI -> 1600 DPI: -15
  const calculate15Step = (baseDpi, sensVal, targetDpi) => {
    let diff = 0;
    if (baseDpi === 400) {
      if (targetDpi === 400) diff = 0;
      else if (targetDpi === 800) diff = -15;
      else if (targetDpi === 1600) diff = -30;
      else diff = -15 * Math.log2(targetDpi / 400);
    } else if (baseDpi === 800) {
      if (targetDpi === 400) diff = +15;
      else if (targetDpi === 800) diff = 0;
      else if (targetDpi === 1600) diff = -15;
      else diff = -15 * Math.log2(targetDpi / 800);
    } else if (baseDpi === 1600) {
      if (targetDpi === 400) diff = +30;
      else if (targetDpi === 800) diff = +15;
      else if (targetDpi === 1600) diff = 0;
      else diff = -15 * Math.log2(targetDpi / 1600);
    } else {
      diff = -15 * Math.log2(targetDpi / baseDpi);
    }

    const res = sensVal + diff;
    return Math.max(0, Math.round(res * 10) / 10);
  };

  // 프로 프리셋 불러오기
  const applyPreset = (nickname, dpi, gen, aim, ads, vert) => {
    setCurrentDpi(dpi);
    setGeneralSens(gen);
    setAimingSens(aim);
    setAdsSens(ads);
    setVerticalMultiplier(vert);
  };

  // 타 FPS 게임 -> PUBG 감도 변환 비율
  const convertGameToPubg = () => {
    let pubgSens = 30;
    const val = parseFloat(sourceSens) || 0;
    if (sourceGame === 'VALORANT') {
      // Valorant 0.4 @ 800DPI ~ PUBG 30 @ 800DPI
      pubgSens = Math.round((val * 75) * 10) / 10;
    } else if (sourceGame === 'OVERWATCH' || sourceGame === 'APEX') {
      // Overwatch/Apex 4.0 @ 800DPI ~ PUBG 30 @ 800DPI
      pubgSens = Math.round((val * 7.5) * 10) / 10;
    } else if (sourceGame === 'CS2') {
      // CS2 1.2 @ 800DPI ~ PUBG 30 @ 800DPI
      pubgSens = Math.round((val * 25) * 10) / 10;
    }
    return pubgSens;
  };

  return (
    <div className="animate-fade-in" style={{ padding: '0 24px 40px', maxWidth: '1100px', margin: '0 auto' }}>
      {/* 타이틀 배너 */}
      <div className="glass-panel gold-glow-border" style={{
        padding: '24px 28px',
        marginBottom: '28px',
        background: 'linear-gradient(135deg, rgba(243, 166, 31, 0.12) 0%, rgba(18, 24, 38, 0.95) 100%)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
          <Calculator size={24} color="var(--accent-gold)" />
          <h2 style={{ fontSize: '1.8rem', color: '#fff', margin: 0, fontWeight: '900' }}>
            PUBG SENSITIVITY CONVERTER
          </h2>
          <span className="badge badge-gold">15-STEP LAW</span>
        </div>
        <p style={{ color: 'var(--text-main)', fontSize: '0.9rem', margin: '4px 0 0' }}>
          배틀그라운드 프로들이 사용하는 <strong>DPI별 15스텝 실전 감도 환산 법칙 (400 DPI $\leftrightarrow$ 800 DPI $\leftrightarrow$ 1600 DPI)</strong>과 타 FPS 감도 변환을 지원합니다.
        </p>
      </div>

      {/* 2-Column 그리드: 좌측 입력 / 우측 15스텝 변환 결과 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '24px', marginBottom: '32px' }}>
        {/* 좌측: 내 감도 입력 패널 */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
            <Crosshair size={20} color="var(--accent-gold)" />
            <h3 style={{ fontSize: '1.2rem', color: '#fff', margin: 0, fontWeight: '800' }}>
              내 현재 감도 설정 입력
            </h3>
          </div>

          {/* DPI 선택 */}
          <div style={{ marginBottom: '18px' }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: '700', display: 'block', marginBottom: '8px' }}>
              마우스 DPI 선택
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px' }}>
              {[400, 800, 1600].map(dpi => (
                <button
                  key={dpi}
                  onClick={() => setCurrentDpi(dpi)}
                  className={currentDpi === dpi ? 'btn-primary' : 'btn-secondary'}
                  style={{ justifyContent: 'center', fontWeight: '800' }}
                >
                  {dpi} DPI
                </button>
              ))}
            </div>
          </div>

          {/* 일반 감도 슬라이더 & 인풋 */}
          <div style={{ marginBottom: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
              <span style={{ fontSize: '0.85rem', color: '#fff', fontWeight: '700' }}>일반 감도 (General)</span>
              <strong style={{ color: 'var(--accent-gold)', fontSize: '1.1rem' }}>{generalSens}</strong>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              step="1"
              value={generalSens}
              onChange={(e) => setGeneralSens(parseFloat(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-gold)' }}
            />
          </div>

          {/* 조준 & ADS 감도 */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>조준 감도 (Aim)</span>
                <strong style={{ color: '#fff' }}>{aimingSens}</strong>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="1"
                value={aimingSens}
                onChange={(e) => setAimingSens(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent-cyan)' }}
              />
            </div>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>ADS 감도</span>
                <strong style={{ color: '#fff' }}>{adsSens}</strong>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                step="1"
                value={adsSens}
                onChange={(e) => setAdsSens(parseFloat(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--accent-cyan)' }}
              />
            </div>
          </div>

          {/* 수직 감도 배율 */}
          <div style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span style={{ fontSize: '0.85rem', color: '#fff', fontWeight: '700' }}>수직 감도 배율 (Vertical Multiplier)</span>
              <strong style={{ color: 'var(--accent-cyan)', fontSize: '1rem' }}>{verticalMultiplier}x</strong>
            </div>
            <input
              type="range"
              min="0.7"
              max="2.0"
              step="0.05"
              value={verticalMultiplier}
              onChange={(e) => setVerticalMultiplier(parseFloat(e.target.value))}
              style={{ width: '100%', accentColor: 'var(--accent-cyan)' }}
            />
          </div>

          {/* 프로 선수 프리셋 빠른 로드 */}
          <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '16px' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: '700', display: 'block', marginBottom: '8px' }}>
              프로 선수 감도 프리셋 원클릭 적용:
            </span>
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              <button onClick={() => applyPreset('Seoul', 800, 28, 28, 28, 1.2)} className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }}>
                Seoul (800 / 28)
              </button>
              <button onClick={() => applyPreset('Salute', 800, 33, 33, 33, 1.0)} className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }}>
                Salute (800 / 33)
              </button>
              <button onClick={() => applyPreset('Inonix', 400, 50, 50, 48, 1.1)} className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }}>
                Inonix (400 / 50)
              </button>
              <button onClick={() => applyPreset('TGLTN', 800, 24, 24, 24, 1.0)} className="btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }}>
                TGLTN (800 / 24)
              </button>
            </div>
          </div>
        </div>

        {/* 우측: 15스텝 동등 감도 환산 결과 */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Sparkles size={20} color="var(--accent-cyan)" />
                <h3 style={{ fontSize: '1.2rem', color: '#fff', margin: 0, fontWeight: '800' }}>
                  15스텝 동등 감도 환산 결과
                </h3>
              </div>
              <span className="badge badge-green">동일 손목 이동량</span>
            </div>

            {/* 400 / 800 / 1600 DPI 카드 3개 */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {/* 400 DPI 환산 */}
              <div style={{
                padding: '16px',
                borderRadius: 'var(--radius-sm)',
                border: currentDpi === 400 ? '2px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                background: currentDpi === 400 ? 'rgba(243, 166, 31, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="badge badge-gold">400 DPI</span>
                    {currentDpi === 400 && <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', fontWeight: '700' }}>(현재 설정)</span>}
                  </div>
                  <div style={{ marginTop: '6px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    조준: {calculate15Step(currentDpi, aimingSens, 400)} • ADS: {calculate15Step(currentDpi, adsSens, 400)} • 수직 {verticalMultiplier}x
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>일반 감도</span>
                  <strong style={{ fontSize: '1.6rem', color: '#fff', display: 'block', fontWeight: '900' }}>
                    {calculate15Step(currentDpi, generalSens, 400)}
                  </strong>
                </div>
              </div>

              {/* 800 DPI 환산 */}
              <div style={{
                padding: '16px',
                borderRadius: 'var(--radius-sm)',
                border: currentDpi === 800 ? '2px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                background: currentDpi === 800 ? 'rgba(243, 166, 31, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="badge badge-cyan">800 DPI</span>
                    {currentDpi === 800 && <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', fontWeight: '700' }}>(현재 설정)</span>}
                  </div>
                  <div style={{ marginTop: '6px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    조준: {calculate15Step(currentDpi, aimingSens, 800)} • ADS: {calculate15Step(currentDpi, adsSens, 800)} • 수직 {verticalMultiplier}x
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>일반 감도</span>
                  <strong style={{ fontSize: '1.6rem', color: 'var(--accent-gold)', display: 'block', fontWeight: '900' }}>
                    {calculate15Step(currentDpi, generalSens, 800)}
                  </strong>
                </div>
              </div>

              {/* 1600 DPI 환산 */}
              <div style={{
                padding: '16px',
                borderRadius: 'var(--radius-sm)',
                border: currentDpi === 1600 ? '2px solid var(--accent-gold)' : '1px solid var(--border-subtle)',
                background: currentDpi === 1600 ? 'rgba(243, 166, 31, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="badge badge-green">1600 DPI</span>
                    {currentDpi === 1600 && <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', fontWeight: '700' }}>(현재 설정)</span>}
                  </div>
                  <div style={{ marginTop: '6px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    조준: {calculate15Step(currentDpi, aimingSens, 1600)} • ADS: {calculate15Step(currentDpi, adsSens, 1600)} • 수직 {verticalMultiplier}x
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>일반 감도</span>
                  <strong style={{ fontSize: '1.6rem', color: '#fff', display: 'block', fontWeight: '900' }}>
                    {calculate15Step(currentDpi, generalSens, 1600)}
                  </strong>
                </div>
              </div>
            </div>
          </div>

          {/* 팁 안내 */}
          <div style={{
            marginTop: '16px',
            padding: '12px',
            background: 'rgba(0, 229, 255, 0.05)',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-cyan)',
            fontSize: '0.8rem',
            color: 'var(--text-main)',
            lineHeight: 1.4
          }}>
            💡 <strong>PUBG 감도 15스텝 공식 가이드:</strong> 400 DPI에서 감도 35를 쓴다면, 800 DPI에서는 15를 뺀 <strong>20</strong>, 1600 DPI에서는 추가로 15를 뺀 <strong>5</strong>를 사용하면 실제 마우스 이동 체감이 완벽하게 일치합니다.
          </div>
        </div>
      </div>

      {/* 3. 하단 섹션: 타 FPS 게임 -> PUBG 감도 변환기 */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <ArrowRightLeft size={20} color="var(--accent-green)" />
          <h3 style={{ fontSize: '1.2rem', color: '#fff', margin: 0, fontWeight: '800' }}>
            타 FPS 게임 감도 $\rightarrow$ 배틀그라운드 감도 변환기
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px', alignItems: 'center' }}>
          {/* 게임 선택 */}
          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>원본 게임</label>
            <select
              value={sourceGame}
              onChange={(e) => setSourceGame(e.target.value)}
              style={{
                width: '100%',
                background: 'rgba(11, 13, 19, 0.9)',
                border: '1px solid var(--border-subtle)',
                color: '#fff',
                padding: '8px 12px',
                borderRadius: 'var(--radius-sm)',
                outline: 'none'
              }}
            >
              <option value="VALORANT">발로란트 (Valorant)</option>
              <option value="OVERWATCH">오버워치 2 (Overwatch 2)</option>
              <option value="APEX">에이펙스 레전드 (Apex Legends)</option>
              <option value="CS2">카운터 스트라이크 2 (CS2)</option>
            </select>
          </div>

          {/* 원본 감도 입력 */}
          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>원본 게임 인게임 감도</label>
            <input
              type="number"
              step="0.01"
              value={sourceSens}
              onChange={(e) => setSourceSens(e.target.value)}
              style={{
                width: '100%',
                background: 'rgba(11, 13, 19, 0.9)',
                border: '1px solid var(--border-subtle)',
                color: '#fff',
                padding: '8px 12px',
                borderRadius: 'var(--radius-sm)',
                outline: 'none'
              }}
            />
          </div>

          {/* 환산 결과 */}
          <div style={{
            background: 'rgba(243, 166, 31, 0.1)',
            padding: '14px 20px',
            borderRadius: 'var(--radius-sm)',
            border: '1px solid var(--border-active)',
            textAlign: 'center'
          }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>추천 PUBG 인게임 감도 (800 DPI 기준)</span>
            <strong style={{ fontSize: '1.6rem', color: 'var(--accent-gold)' }}>
              {convertGameToPubg()}
            </strong>
          </div>
        </div>
      </div>
    </div>
  );
}
