import React from 'react';
import { byId } from '../data/catalog.js';
import { computeMatches } from '../lib/recommend.js';
import MatchCard from '../components/MatchCard.jsx';

export default function PlayNextScreen({ seedId, goRecommend }) {
  const seed = byId(seedId);
  const matches = computeMatches(seed);
  const seedTitle = seed.t.replace(/,.*$/, '');
  const seedShort = seed.c.split(',')[0] + ' — ' + seedTitle;

  return (
    <div style={{ flex: 1 }}>
      {/* hero */}
      <div style={{ padding: '34px 44px 26px', background: 'linear-gradient(180deg,var(--paper2),var(--paper))', borderBottom: '1px solid var(--line)' }}>
        <div style={{ maxWidth: 680 }}>
          <p style={{ font: '600 11px var(--mono)', letterSpacing: '.14em', textTransform: 'uppercase', color: 'var(--brass-d)', margin: '0 0 8px' }}>Find your next piece</p>
          <h1 style={{ font: '500 30px/1.2 var(--serif)', margin: '0 0 18px', color: 'var(--ink)' }}>What did you play last?</h1>
          <div style={{ minHeight: 52, border: '1.5px solid var(--wine)', borderRadius: 12, background: 'var(--paper)', display: 'flex', alignItems: 'center', gap: 11, padding: '7px 8px 7px 15px', boxShadow: '0 5px 20px -12px rgba(122,39,51,.55)', flexWrap: 'wrap' }}>
            <span style={{ color: 'var(--wine)', fontSize: 17 }}>⌕</span>
            <span className="chip on" style={{ padding: '5px 11px 5px 12px' }}>{seedShort} <span className="x">×</span></span>
            <span style={{ font: '400 12.5px var(--sans)', color: 'var(--faint)' }}>add another…</span>
            <button className="btn" style={{ marginLeft: 'auto' }}>Show me similar →</button>
          </div>
          <div style={{ display: 'flex', gap: 8, marginTop: 14, alignItems: 'center', flexWrap: 'wrap' }}>
            <span style={{ font: '400 12px var(--sans)', color: 'var(--muted)' }}>Prioritize:</span>
            <span className="chip on" style={{ padding: '5px 11px' }}>Same instrument</span>
            <span className="chip" style={{ padding: '5px 11px' }}>Same era</span>
            <span className="chip" style={{ padding: '5px 11px' }}>Similar length</span>
          </div>
        </div>
      </div>

      {/* results */}
      <div style={{ padding: '26px 44px 46px' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 9, marginBottom: 20, flexWrap: 'wrap' }}>
          <h2 style={{ font: '500 18px var(--serif)', margin: 0, color: 'var(--ink)' }}>Because you played <em>{seedTitle}</em></h2>
          <span style={{ font: '400 12px var(--mono)', color: 'var(--muted)' }}>— {matches.length} close matches</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 18 }}>
          {matches.map((m) => (
            <MatchCard key={m.id} m={m} onSimilar={() => goRecommend(m.id)} />
          ))}
        </div>
      </div>
    </div>
  );
}
