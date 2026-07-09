import React from 'react';
import { catalog, byId } from '../data/catalog.js';
import { enrich } from '../lib/recommend.js';
import ResultRow, { ResultHeader } from '../components/ResultRow.jsx';

// NOTE: filter rail + query are visual placeholders in this prototype.
// Wire them to real state + your search/filter service in production.
export default function BrowseScreen({ goRecommend }) {
  const rows = [0, 1, 2, 3, 10, 5].map(byId).map(enrich);

  return (
    <div style={{ flex: 1 }}>
      {/* search bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 18, padding: '18px 34px', borderBottom: '1px solid var(--line)', background: 'var(--paper)' }}>
        <div className="field" style={{ flex: 1, maxWidth: 620, height: 44, color: 'var(--ink)', fontWeight: 500 }}>
          <span style={{ color: 'var(--wine)', fontSize: 16, marginRight: 10 }}>⌕</span>sarabande
          <span style={{ width: 1.5, height: 18, background: 'var(--wine)', marginLeft: 1 }} />
          <span style={{ marginLeft: 'auto', font: '400 12px var(--mono)', color: 'var(--faint)' }}>3,102 results</span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '236px 1fr' }}>
        {/* filter rail */}
        <div style={{ borderRight: '1px solid var(--line)', padding: '22px 20px', background: 'var(--paper2)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 18 }}>
            <span style={{ font: '600 11px var(--mono)', letterSpacing: '.1em', textTransform: 'uppercase', color: 'var(--muted)' }}>Filters</span>
            <span style={{ font: '500 11.5px var(--sans)', color: 'var(--wine)', cursor: 'pointer' }}>Clear</span>
          </div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ font: '600 12.5px var(--sans)', color: 'var(--ink)', marginBottom: 10 }}>Era</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 9, font: '400 12.5px var(--sans)', color: 'var(--ink2)' }}>
              {[['Baroque', '3,102', true], ['Classical', '4,417', false], ['Romantic', '4,961', false]].map(([label, n, on]) => (
                <label key={label} style={{ display: 'flex', gap: 9, alignItems: 'center', cursor: 'pointer' }}>
                  <span style={on
                    ? { width: 16, height: 16, borderRadius: 4, background: 'var(--wine)', display: 'grid', placeItems: 'center', color: '#fff', fontSize: 10 }
                    : { width: 16, height: 16, borderRadius: 4, border: '1.5px solid var(--line)' }}>{on ? '✓' : ''}</span>
                  {label}<span style={{ marginLeft: 'auto', color: 'var(--faint)', font: '400 11px var(--mono)' }}>{n}</span>
                </label>
              ))}
            </div>
          </div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ font: '600 12.5px var(--sans)', color: 'var(--ink)', marginBottom: 10 }}>Instrument</div>
            <div className="field" style={{ height: 36 }}>Piano, cello…</div>
          </div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', font: '600 12.5px var(--sans)', color: 'var(--ink)', marginBottom: 14 }}>Duration <span style={{ font: '400 11px var(--mono)', color: 'var(--muted)' }}>0–30m</span></div>
            <div style={{ height: 4, borderRadius: 2, background: 'var(--line)', position: 'relative' }}>
              <span style={{ position: 'absolute', left: '12%', right: '34%', top: 0, bottom: 0, background: 'var(--wine)', borderRadius: 2 }} />
              <span style={{ position: 'absolute', left: '12%', top: -5, width: 13, height: 13, borderRadius: '50%', background: 'var(--paper)', border: '2px solid var(--wine)' }} />
              <span style={{ position: 'absolute', right: '34%', top: -5, width: 13, height: 13, borderRadius: '50%', background: 'var(--paper)', border: '2px solid var(--wine)' }} />
            </div>
          </div>
          <div>
            <div style={{ font: '600 12.5px var(--sans)', color: 'var(--ink)', marginBottom: 10 }}>Key</div>
            <div className="field" style={{ height: 36 }}>Any key</div>
          </div>
        </div>

        {/* results */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '15px 26px', borderBottom: '1px solid var(--line)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 9, flexWrap: 'wrap' }}>
              <span style={{ font: '400 12.5px var(--sans)', color: 'var(--muted)' }}>Showing</span>
              <span className="chip on" style={{ padding: '4px 11px' }}>Baroque <span className="x">×</span></span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 9, font: '400 12px var(--sans)', color: 'var(--muted)' }}>Sort <b style={{ color: 'var(--ink)', fontWeight: 600 }}>Most downloaded ▾</b></div>
          </div>
          <ResultHeader />
          {rows.map((p) => (
            <ResultRow key={p.id} p={p} onSimilar={() => goRecommend(p.id)} />
          ))}
        </div>
      </div>
    </div>
  );
}
