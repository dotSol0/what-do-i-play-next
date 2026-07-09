import React from 'react';
import { catalog, byId } from '../data/catalog.js';
import { enrich, computeMatches } from '../lib/recommend.js';
import MatchCard from '../components/MatchCard.jsx';
import StarterCard from '../components/StarterCard.jsx';

const HISTORY = ['sarabande', 'solo cello', 'easy piano', 'D minor', 'Bach suites'];

export default function StartScreen({ goBrowse, goRecommend }) {
  const recent = [0, 8, 7].map(byId).map(enrich);
  const likeCards = computeMatches(byId(0)).slice(0, 4);
  const starters = [8, 7, 10, 6].map(byId).map(enrich);

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '70px 32px 60px' }}>
      {/* masthead + search */}
      <div style={{ width: '100%', maxWidth: 720, textAlign: 'center' }}>
        <p style={{ font: '600 11px var(--mono)', letterSpacing: '.16em', textTransform: 'uppercase', color: 'var(--brass-d)', margin: '0 0 12px' }}>A student's guide to public-domain repertoire</p>
        <h1 style={{ font: '400 42px/1.12 var(--serif)', margin: '0 0 14px', color: 'var(--ink)' }}>Repertoire worth your practice hours.</h1>
        <p style={{ font: '400 14px/1.6 var(--sans)', color: 'var(--muted)', maxWidth: 460, margin: '0 auto 30px' }}>Search 12,480 curated, freely-playable scores — or tell us what you played last and we'll find its neighbours.</p>

        <div className="field" onClick={goBrowse} style={{ height: 56, border: '1.5px solid var(--wine)', borderRadius: 13, cursor: 'text', boxShadow: '0 6px 22px -12px rgba(122,39,51,.55)', color: 'var(--muted)', fontSize: 14.5 }}>
          <span style={{ color: 'var(--wine)', fontSize: 18, marginRight: 11 }}>⌕</span>Search by title, composer, instrument, key…
          <span className="kbd" style={{ marginLeft: 'auto' }}>/</span>
        </div>

        <div style={{ display: 'flex', gap: 9, justifyContent: 'center', flexWrap: 'wrap', marginTop: 16 }}>
          <span style={{ font: '400 12.5px var(--sans)', color: 'var(--muted)', alignSelf: 'center' }}>Browse an era:</span>
          {['Baroque', 'Classical', 'Romantic'].map((e) => (
            <span key={e} className="chip" onClick={goBrowse}>{e}</span>
          ))}
        </div>
      </div>

      {/* pick up where you left off (compact) */}
      <div style={{ width: '100%', maxWidth: 1000, marginTop: 30, borderTop: '1px solid var(--line)', paddingTop: 20 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 9, marginBottom: 12, textAlign: 'left' }}>
          <span style={{ font: '600 10px var(--mono)', letterSpacing: '.12em', textTransform: 'uppercase', color: 'var(--muted)' }}>Pick up where you left off</span>
          <span style={{ font: '400 12px var(--sans)', color: 'var(--muted)' }}>— what did you play last?</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 12, textAlign: 'left' }}>
          {recent.map((p) => (
            <div key={p.id} onClick={() => goRecommend(p.id)} style={{ display: 'flex', alignItems: 'center', gap: 11, padding: '11px 14px', border: '1px solid var(--line)', borderRadius: 10, background: 'var(--paper)', cursor: 'pointer' }}>
              <span style={{ fontSize: 14, color: 'var(--brass)' }}>↻</span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ font: '500 13px/1.2 var(--serif)', color: 'var(--ink)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{p.t}</div>
                <div style={{ font: '400 11px var(--sans)', color: 'var(--muted)' }}>{p.c}</div>
              </div>
              <span style={{ font: '600 12px var(--sans)', color: 'var(--wine)', whiteSpace: 'nowrap' }}>Similar →</span>
            </div>
          ))}
        </div>

        {/* you may like */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, margin: '40px 0 18px', flexWrap: 'wrap', textAlign: 'left' }}>
          <h2 style={{ font: '500 20px var(--serif)', margin: 0, color: 'var(--ink)' }}>Because you've been exploring <em>solo cello</em></h2>
          <span style={{ font: '400 12px var(--mono)', color: 'var(--muted)' }}>— you may like</span>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 3, background: 'var(--paper)', border: '1px solid var(--line)', borderRadius: 9, padding: 3 }}>
            <span className="seg on">For you</span><span className="seg">Popular</span><span className="seg">New additions</span>
          </div>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 16, textAlign: 'left' }}>
          {likeCards.map((m) => (
            <MatchCard key={m.id} m={m} compact onSimilar={() => goRecommend(m.id)} />
          ))}
        </div>

        {/* starters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, margin: '40px 0 18px', flexWrap: 'wrap', textAlign: 'left' }}>
          <h2 style={{ font: '500 20px var(--serif)', margin: 0, color: 'var(--ink)' }}>New to the library? Start here</h2>
          <span style={{ font: '400 12px var(--mono)', color: 'var(--muted)' }}>— editor's picks</span>
          <span style={{ marginLeft: 'auto', font: '600 12px var(--sans)', color: 'var(--wine)', cursor: 'pointer' }} onClick={goBrowse}>Browse all 12,480 →</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 16, textAlign: 'left' }}>
          {starters.map((p) => (
            <StarterCard key={p.id} p={p} onSimilar={() => goRecommend(p.id)} />
          ))}
        </div>
      </div>
    </div>
  );
}
