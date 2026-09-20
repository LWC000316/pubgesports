import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

export default function ErrorPanel({ title = '데이터를 불러오지 못했습니다', message, hint, onRetry }) {
  return (
    <div className="glass-panel" style={{
      padding: '60px 24px',
      borderRadius: 'var(--radius-md)',
      textAlign: 'center',
      border: '1px solid rgba(255, 51, 75, 0.35)',
      background: 'linear-gradient(135deg, rgba(255, 51, 75, 0.1) 0%, rgba(22, 26, 38, 0.95) 100%)'
    }}>
      <AlertTriangle size={36} color="#ff334b" style={{ marginBottom: '16px' }} />
      <div style={{ fontWeight: '900', color: '#fff', fontSize: '1rem', marginBottom: '8px' }}>
        {title}
      </div>
      {message && (
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
          {message}
        </div>
      )}
      {hint && (
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '20px' }}>
          {hint}
        </div>
      )}
      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            padding: '10px 22px',
            borderRadius: 'var(--radius-sm)',
            background: 'var(--accent-gold)',
            color: '#000',
            border: 'none',
            fontWeight: '800',
            fontSize: '0.85rem',
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <RefreshCw size={15} />
          다시 시도
        </button>
      )}
    </div>
  );
}
