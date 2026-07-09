import React, { useState } from 'react';
import TopBar from './components/TopBar.jsx';
import StartScreen from './screens/StartScreen.jsx';
import BrowseScreen from './screens/BrowseScreen.jsx';
import PlayNextScreen from './screens/PlayNextScreen.jsx';

// Simple screen router. Swap for react-router in a real app.
export default function App() {
  const [screen, setScreen] = useState('start'); // 'start' | 'browse' | 'recommend'
  const [seedId, setSeedId] = useState(0);

  const go = (s) => { setScreen(s); window.scrollTo(0, 0); };
  const goRecommend = (id) => { setSeedId(id); setScreen('recommend'); window.scrollTo(0, 0); };

  return (
    <div className="app">
      <TopBar screen={screen} goStart={() => go('start')} goBrowse={() => go('browse')} goRecommend={goRecommend} />
      {screen === 'start' && <StartScreen goBrowse={() => go('browse')} goRecommend={goRecommend} />}
      {screen === 'browse' && <BrowseScreen goRecommend={goRecommend} />}
      {screen === 'recommend' && <PlayNextScreen seedId={seedId} goRecommend={goRecommend} />}
    </div>
  );
}
