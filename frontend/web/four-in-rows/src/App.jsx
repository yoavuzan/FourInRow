import React from 'react';
import './App.css';

const NUM_ROWS = 6;
const NUM_COLS = 7;

const App = () => {
  // Placeholder board for rendering - actual state will come from backend
  const board = Array(NUM_ROWS).fill(Array(NUM_COLS).fill(null));

  const handleCellClick = (col) => {
    console.log(`Cell clicked in column: ${col}. This action will be sent to the backend.`);
    // In a real application, this would send an API request to the backend
    // e.g., fetch('/move', { method: 'POST', body: JSON.stringify({ col }) });
  };

  const handleReset = () => {
    console.log("Reset button clicked. This action will be sent to the backend.");
    // In a real application, this would send an API request to the backend to reset the game
  };

  return (
    <div className="app">
      <h1>Four in a Row</h1>
      <div className="board">
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={colIndex}
                className={`cell ${cell ? `filled ${cell.toLowerCase().replace(' ', '-')}` : ''}`}
                onClick={() => handleCellClick(colIndex)}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="status">
        <h2>Current Player: (Backend determines)</h2>
        <p>Game Status: (Backend determines)</p>
      </div>
       <button onClick={handleReset}>Reset Game</button>
    </div>
  );
};

export default App;