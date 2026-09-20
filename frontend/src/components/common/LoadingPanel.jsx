import React from 'react';
import { RefreshCw } from 'lucide-react';

export default function LoadingPanel({ title = '불러오는 중입니다', detail }) {
  return (
    <div className="glass-panel" style={{
      padding: '60px 24px',
      borderRadius: 'var(--radius-md)',
      textAlign: 'center',
      border: '1px solid var(--border-subtle)'
    }}>
      <RefreshCw
        size={36}
        color="var(--accent-gold)"
        style={{ marginBottom: '16px', animation: 'pulseGlow 1.4s ease-in-out infinite' }}
      />
      <div style={{ fontWeight: '900', color: '#fff', fontSize: '1rem', marginBottom: '6px' }}>
        {title}
      </div>
      {detail && (
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{detail}</div>
      )}
    </div>
  );
}
