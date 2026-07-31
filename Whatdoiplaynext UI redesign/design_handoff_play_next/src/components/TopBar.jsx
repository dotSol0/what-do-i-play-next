import React from 'react';

export default function TopBar({ screen, goStart, goBrowse, goRecommend }) {
  return (
    <div className="topbar">
      <div className="brand" onClick={goStart}>
        <span className="logo">♪</span>What Do I Play Next
      </div>
      <div className="nav">
        <span className={'navlink' + (screen === 'browse' ? ' on' : '')} onClick={goBrowse}>Browse</span>
        <span className={'navlink' + (screen === 'recommend' ? ' on' : '')} onClick={() => goRecommend(0)}>Play Next</span>
      </div>
      <span className="avatar">MR</span>
    </div>
  );
}
