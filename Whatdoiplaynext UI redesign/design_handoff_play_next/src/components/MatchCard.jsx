import React from 'react';

// Recommendation card with match score + reasons.
// Used in Play Next results and the homepage "you may like" shelf.
export default function MatchCard({ m, onSimilar, compact }) {
  return (
    <div className="likecard" style={{ border: '1px solid var(--line)', borderRadius: 12, background: 'var(--paper)', padding: compact ? 16 : 18, display: 'flex', flexDirection: 'column', gap: compact ? 11 : 12 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span className={m.eraCls}>{m.eraLbl}</span>
        {compact ? (
          <span style={{ font: '600 12px var(--mono)', color: 'var(--brass-d)' }}>{m.score} match</span>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 1 }}>
            <div style={{ font: '600 20px var(--mono)', color: 'var(--brass-d)', lineHeight: 1 }}>{m.score}</div>
            <div style={{ font: '500 8.5px var(--mono)', letterSpacing: '.12em', textTransform: 'uppercase', color: 'var(--faint)' }}>match</div>
          </div>
        )}
      </div>
      <div>
        <div style={{ font: `500 ${compact ? 15 : 15.5}px/1.25 var(--serif)`, color: 'var(--ink)', marginBottom: compact ? 3 : 4 }}>{m.t}</div>
        <div style={{ font: '400 11px var(--sans)', color: 'var(--muted)' }}>{m.c} · {m.instShort}</div>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginTop: 2, flex: 1 }}>
        {m.reasons.map((r, i) => (
          <div key={i} style={{ display: 'flex', gap: compact ? 7 : 8, alignItems: 'flex-start', font: '400 11.5px/1.35 var(--sans)', color: 'var(--ink2)' }}>
            <span style={{ color: 'var(--brass)', fontSize: 12, lineHeight: 1.2 }}>✦</span>{r}
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: compact ? 8 : 9, marginTop: 2 }}>
        <a className="btn" href={m.permalink} target="_blank" rel="noopener noreferrer" style={{ flex: 1, justifyContent: 'center', ...(compact ? { padding: '8px 10px', fontSize: 11.5 } : {}) }}>
          View on IMSLP ↗
        </a>
        <span className="simbtn" onClick={onSimilar} style={compact ? { padding: '8px 10px' } : {}}>≈</span>
      </div>
    </div>
  );
}
