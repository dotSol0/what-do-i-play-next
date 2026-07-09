import React from 'react';

const COLS = '1fr 132px 88px 68px 220px';

export function ResultHeader() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: COLS, gap: 14, padding: '10px 26px', borderBottom: '1px solid var(--line)', font: '600 10px var(--mono)', letterSpacing: '.08em', textTransform: 'uppercase', color: 'var(--faint)' }}>
      <span>Piece</span><span>Instrumentation</span><span>Key</span><span>Length</span><span />
    </div>
  );
}

// One row in the Browse results table.
export default function ResultRow({ p, onSimilar }) {
  return (
    <div className="a-row" style={{ display: 'grid', gridTemplateColumns: COLS, gap: 14, padding: '15px 26px', alignItems: 'center', borderBottom: '1px solid var(--line2)' }}>
      <div>
        <div style={{ font: '500 14.5px var(--serif)', color: 'var(--ink)', marginBottom: 3 }}>{p.t}</div>
        <div style={{ display: 'flex', gap: 9, alignItems: 'center' }}>
          <span className={p.eraCls}>{p.eraLbl}</span>
          <span style={{ font: '400 11.5px var(--sans)', color: 'var(--muted)' }}>{p.c}</span>
          <span style={{ font: '400 11px var(--mono)', color: 'var(--faint)' }}>↓ {p.dl}</span>
        </div>
      </div>
      <span style={{ font: '400 12px var(--sans)', color: 'var(--ink2)' }}>{p.inst}</span>
      <span style={{ font: '400 12px var(--mono)', color: 'var(--ink2)' }}>{p.key}</span>
      <span style={{ font: '400 12px var(--mono)', color: 'var(--ink2)' }}>{p.dur}</span>
      <div style={{ display: 'flex', gap: 9, alignItems: 'center', justifyContent: 'flex-end' }}>
        <span className="simbtn" onClick={onSimilar}>≈ Similar</span>
        <a className="btn" href={p.permalink} target="_blank" rel="noopener noreferrer">View on IMSLP ↗</a>
      </div>
    </div>
  );
}
