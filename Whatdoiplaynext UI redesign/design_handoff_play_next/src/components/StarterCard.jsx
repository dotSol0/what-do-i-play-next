import React from 'react';

// Editor's-pick / default-starter card: shows downloads instead of a match score.
export default function StarterCard({ p, onSimilar }) {
  return (
    <div className="likecard" style={{ border: '1px solid var(--line)', borderRadius: 11, background: 'var(--paper)', padding: 16, display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span className={p.eraCls}>{p.eraLbl}</span>
        <span style={{ font: '400 11px var(--mono)', color: 'var(--faint)' }}>↓ {p.dl}</span>
      </div>
      <div>
        <div style={{ font: '500 15px/1.25 var(--serif)', color: 'var(--ink)', marginBottom: 3 }}>{p.t}</div>
        <div style={{ font: '400 11px var(--sans)', color: 'var(--muted)' }}>{p.c} · {p.instShort}</div>
      </div>
      <div style={{ display: 'flex', gap: 8, marginTop: 2 }}>
        <a className="btn" href={p.permalink} target="_blank" rel="noopener noreferrer" style={{ flex: 1, justifyContent: 'center', padding: '8px 10px', fontSize: 11.5 }}>View ↗</a>
        <span className="simbtn" onClick={onSimilar} style={{ padding: '8px 10px' }}>≈</span>
      </div>
    </div>
  );
}
