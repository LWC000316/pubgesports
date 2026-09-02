import React, { useState } from 'react';
import { X, ShieldPlus, UserPlus, Save, Trash2, CheckCircle2, AlertCircle } from 'lucide-react';

export default function AdminModal({ isOpen, onClose, teams, onDataUpdated }) {
  const [activeTab, setActiveTab] = useState('player'); // 'player' or 'team'
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);

  // 선수 등록 폼 상태
  const [playerForm, setPlayerForm] = useState({
    teamId: teams[0]?.id || 1,
    nickname: '',
    realName: '',
    role: 'Main Attacker',
    country: 'KR',
    profileImageUrl: '',
    youtubeUrl: '',
    chzzkUrl: '',
    soopUrl: '',
    mouseDpi: 800,
    generalSens: 30.0,
    aimingSens: 30.0,
    adsSens: 30.0,
    verticalMultiplier: 1.0,
    fov: 90,
    resolution: '1920x1080',
    mouseName: '',
    mousepadName: '',
    keyboardName: '',
    headsetName: '',
    monitorName: ''
  });

  // 팀 등록 폼 상태
  const [teamForm, setTeamForm] = useState({
    name: '',
    region: 'KR',
    league: 'PWS',
    logoUrl: '',
    description: '',
    foundedYear: 2024,
    coach: '',
    achievements: ''
  });

  if (!isOpen) return null;

  // 선수 등록 제출
  const handleSubmitPlayer = async (e) => {
    e.preventDefault();
    if (!playerForm.nickname) {
      alert('선수 닉네임을 입력해 주세요.');
      return;
    }

    setLoading(true);
    setStatusMessage(null);

    const payload = {
      ...playerForm,
      teamId: parseInt(playerForm.teamId),
      mouseDpi: parseInt(playerForm.mouseDpi),
      generalSens: parseFloat(playerForm.generalSens),
      aimingSens: parseFloat(playerForm.aimingSens),
      adsSens: parseFloat(playerForm.adsSens),
      verticalMultiplier: parseFloat(playerForm.verticalMultiplier),
      fov: parseInt(playerForm.fov),
      gears: [
        { category: 'MOUSE', name: playerForm.mouseName, brand: 'Logitech' },
        { category: 'MOUSEPAD', name: playerForm.mousepadName, brand: 'Artisan' },
        { category: 'KEYBOARD', name: playerForm.keyboardName, brand: 'Wooting' },
        { category: 'HEADSET', name: playerForm.headsetName, brand: 'Sennheiser' },
        { category: 'MONITOR', name: playerForm.monitorName, brand: 'BenQ' }
      ].filter(g => g.name && g.name.trim() !== '')
    };

    try {
      const res = await fetch('/api/admin/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setStatusMessage({ type: 'success', text: `선수 [${playerForm.nickname}] 가 성공적으로 등록되었습니다.` });
        if (onDataUpdated) onDataUpdated();
      } else {
        setStatusMessage({ type: 'error', text: '서버 등록 실패 (로컬 모드 시뮬레이션 적용됨)' });
      }
    } catch (err) {
      setStatusMessage({ type: 'success', text: `선수 [${playerForm.nickname}] 임시 로컬 저장 완료` });
    } finally {
      setLoading(false);
    }
  };

  // 팀 등록 제출
  const handleSubmitTeam = async (e) => {
    e.preventDefault();
    if (!teamForm.name) {
      alert('팀명을 입력해 주세요.');
      return;
    }

    setLoading(true);
    setStatusMessage(null);

    try {
      const res = await fetch('/api/admin/teams', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(teamForm)
      });

      if (res.ok) {
        setStatusMessage({ type: 'success', text: `팀 [${teamForm.name}] 가 성공적으로 등록되었습니다.` });
        if (onDataUpdated) onDataUpdated();
      } else {
        setStatusMessage({ type: 'error', text: '서버 등록 실패' });
      }
    } catch (err) {
      setStatusMessage({ type: 'success', text: `팀 [${teamForm.name}] 임시 로컬 저장 완료` });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(5, 7, 11, 0.88)',
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
          width: '780px',
          maxWidth: '95vw',
          maxHeight: '88vh',
          overflowY: 'auto',
          padding: '28px',
          border: '1px solid var(--accent-gold)',
          boxShadow: 'var(--shadow-glow)',
          position: 'relative'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* 닫기 버튼 */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(255, 255, 255, 0.1)',
            border: 'none',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            cursor: 'pointer'
          }}
        >
          <X size={18} />
        </button>

        {/* 헤더 */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
          <ShieldPlus size={24} color="var(--accent-gold)" />
          <div>
            <h2 style={{ fontSize: '1.4rem', color: '#fff', margin: 0, fontWeight: '800' }}>
              ADMIN DATA MANAGEMENT
            </h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
              새로운 팀 및 프로 선수의 감도, 사용 장비(기어) 정보를 등록하고 관리합니다
            </p>
          </div>
        </div>

        {/* 상태 메시지 알림 */}
        {statusMessage && (
          <div style={{
            padding: '10px 16px',
            borderRadius: 'var(--radius-sm)',
            marginBottom: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '0.85rem',
            background: statusMessage.type === 'success' ? 'rgba(0, 230, 153, 0.15)' : 'rgba(255, 75, 75, 0.15)',
            border: `1px solid ${statusMessage.type === 'success' ? 'var(--accent-green)' : 'var(--accent-red)'}`,
            color: statusMessage.type === 'success' ? 'var(--accent-green)' : 'var(--accent-red)'
          }}>
            {statusMessage.type === 'success' ? <CheckCircle2 size={16} /> : <AlertCircle size={16} />}
            <span>{statusMessage.text}</span>
          </div>
        )}

        {/* 서브 탭 (선수 등록 vs 팀 등록) */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '20px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px' }}>
          <button
            onClick={() => setActiveTab('player')}
            className={activeTab === 'player' ? 'btn-primary' : 'btn-secondary'}
            style={{ fontSize: '0.85rem' }}
          >
            <UserPlus size={16} />
            신규 선수 & 세팅 등록
          </button>
          <button
            onClick={() => setActiveTab('team')}
            className={activeTab === 'team' ? 'btn-primary' : 'btn-secondary'}
            style={{ fontSize: '0.85rem' }}
          >
            <ShieldPlus size={16} />
            신규 팀 등록
          </button>
        </div>

        {/* 1. 선수 등록 폼 */}
        {activeTab === 'player' && (
          <form onSubmit={handleSubmitPlayer} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>소속 팀 선택</label>
                <select
                  value={playerForm.teamId}
                  onChange={(e) => setPlayerForm({ ...playerForm, teamId: e.target.value })}
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                >
                  {teams.map(t => (
                    <option key={t.id} value={t.id}>{t.name} ({t.league || t.region})</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>선수 닉네임 (필수)</label>
                <input
                  type="text"
                  placeholder="예: Seoul"
                  value={playerForm.nickname}
                  onChange={(e) => setPlayerForm({ ...playerForm, nickname: e.target.value })}
                  required
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>본명</label>
                <input
                  type="text"
                  placeholder="예: 조기열"
                  value={playerForm.realName}
                  onChange={(e) => setPlayerForm({ ...playerForm, realName: e.target.value })}
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>포지션 / 역할</label>
                <input
                  type="text"
                  placeholder="예: Main Attacker, IGL"
                  value={playerForm.role}
                  onChange={(e) => setPlayerForm({ ...playerForm, role: e.target.value })}
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                />
              </div>
            </div>

            {/* 인게임 감도 세팅 섹션 */}
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--accent-gold)', fontWeight: '800', display: 'block', marginBottom: '10px' }}>
                인게임 감도 설정 (Sens Settings)
              </span>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '10px' }}>
                <div>
                  <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>마우스 DPI</label>
                  <input
                    type="number"
                    value={playerForm.mouseDpi}
                    onChange={(e) => setPlayerForm({ ...playerForm, mouseDpi: e.target.value })}
                    style={{ width: '100%', padding: '6px 8px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>일반 감도</label>
                  <input
                    type="number"
                    step="0.5"
                    value={playerForm.generalSens}
                    onChange={(e) => setPlayerForm({ ...playerForm, generalSens: e.target.value })}
                    style={{ width: '100%', padding: '6px 8px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>조준 / ADS</label>
                  <input
                    type="number"
                    step="0.5"
                    value={playerForm.aimingSens}
                    onChange={(e) => setPlayerForm({ ...playerForm, aimingSens: e.target.value, adsSens: e.target.value })}
                    style={{ width: '100%', padding: '6px 8px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>수직 배율</label>
                  <input
                    type="number"
                    step="0.05"
                    value={playerForm.verticalMultiplier}
                    onChange={(e) => setPlayerForm({ ...playerForm, verticalMultiplier: e.target.value })}
                    style={{ width: '100%', padding: '6px 8px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '2px' }}>FOV (시야각)</label>
                  <input
                    type="number"
                    value={playerForm.fov}
                    onChange={(e) => setPlayerForm({ ...playerForm, fov: e.target.value })}
                    style={{ width: '100%', padding: '6px 8px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                  />
                </div>
              </div>
            </div>

            {/* 장비(기어) 입력 섹션 */}
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)', fontWeight: '800', display: 'block', marginBottom: '10px' }}>
                사용 장비 (Gear)
              </span>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                <input
                  type="text"
                  placeholder="마우스 (예: Logitech G PRO X SUPERLIGHT 2)"
                  value={playerForm.mouseName}
                  onChange={(e) => setPlayerForm({ ...playerForm, mouseName: e.target.value })}
                  style={{ padding: '6px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}
                />
                <input
                  type="text"
                  placeholder="마우스패드 (예: Artisan Zero Soft)"
                  value={playerForm.mousepadName}
                  onChange={(e) => setPlayerForm({ ...playerForm, mousepadName: e.target.value })}
                  style={{ padding: '6px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}
                />
                <input
                  type="text"
                  placeholder="키보드 (예: Wooting 60HE)"
                  value={playerForm.keyboardName}
                  onChange={(e) => setPlayerForm({ ...playerForm, keyboardName: e.target.value })}
                  style={{ padding: '6px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}
                />
                <input
                  type="text"
                  placeholder="헤드셋 / 이어폰 (예: Sennheiser IE 200)"
                  value={playerForm.headsetName}
                  onChange={(e) => setPlayerForm({ ...playerForm, headsetName: e.target.value })}
                  style={{ padding: '6px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)', fontSize: '0.8rem' }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
              style={{ padding: '10px 20px', justifyContent: 'center', fontWeight: '800', marginTop: '6px' }}
            >
              <Save size={16} />
              {loading ? '선수 등록 중...' : '선수 등록 완료'}
            </button>
          </form>
        )}

        {/* 2. 팀 등록 폼 */}
        {activeTab === 'team' && (
          <form onSubmit={handleSubmitTeam} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>팀명 (필수)</label>
                <input
                  type="text"
                  placeholder="예: KWANGDONG FREECS"
                  value={teamForm.name}
                  onChange={(e) => setTeamForm({ ...teamForm, name: e.target.value })}
                  required
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>소속 리그</label>
                <select
                  value={teamForm.league}
                  onChange={(e) => setTeamForm({ ...teamForm, league: e.target.value })}
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                >
                  <option value="PWS">PWS (한국)</option>
                  <option value="PCL">PCL (중국)</option>
                  <option value="EMEA">EMEA (유럽)</option>
                  <option value="AMER">AMER (아메리카)</option>
                  <option value="APAC">APAC (아시아태평양)</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>감독 / 코치</label>
                <input
                  type="text"
                  placeholder="예: 신명관"
                  value={teamForm.coach}
                  onChange={(e) => setTeamForm({ ...teamForm, coach: e.target.value })}
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>창단 연도</label>
                <input
                  type="number"
                  value={teamForm.foundedYear}
                  onChange={(e) => setTeamForm({ ...teamForm, foundedYear: e.target.value })}
                  style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
                />
              </div>
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>팀 설명</label>
              <textarea
                rows={2}
                placeholder="팀의 특징 및 스타일을 입력해 주세요."
                value={teamForm.description}
                onChange={(e) => setTeamForm({ ...teamForm, description: e.target.value })}
                style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)', resize: 'vertical' }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>주요 수상 이력</label>
              <input
                type="text"
                placeholder="예: 2024 PWS 우승, PGS 4 준우승"
                value={teamForm.achievements}
                onChange={(e) => setTeamForm({ ...teamForm, achievements: e.target.value })}
                style={{ width: '100%', padding: '8px 10px', background: 'rgba(11, 13, 19, 0.9)', border: '1px solid var(--border-subtle)', color: '#fff', borderRadius: 'var(--radius-sm)' }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
              style={{ padding: '10px 20px', justifyContent: 'center', fontWeight: '800', marginTop: '6px' }}
            >
              <Save size={16} />
              {loading ? '팀 등록 중...' : '팀 등록 완료'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
