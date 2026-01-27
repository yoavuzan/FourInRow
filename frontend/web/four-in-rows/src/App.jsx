import React, { useState, useEffect } from 'react';
import './App.css';


const socket = new WebSocket("wss://four-in-row-pi.vercel.app/ws/game");

const App = () => {
  const [board, setBoard] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('');
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);

  useEffect(() => {
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setBoard(data.board);
      setCurrentPlayer(data.currentPlayer);
      setGameOver(data.gameOver);
      setWinner(data.winner);
    };

    socket.onopen = () => {
      console.log("WebSocket connection established");
      // You might want to send a message to get the initial game state
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }, []);

  const handleCellClick = (col) => {
    if (gameOver) return;
    socket.send(JSON.stringify({ action: 'move', col }));
  };

  const handleReset = () => {
    socket.send(JSON.stringify({ action: 'reset' }));
  };

  const getPlayerClass = (cell) => {
    if (cell === 'X') return 'player-1';
    if (cell === 'O') return 'player-2';
    return '';
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
                className={`cell ${cell ? `filled ${getPlayerClass(cell)}` : ''}`}
                onClick={() => handleCellClick(colIndex)}
              />
            ))}
          </div>
        ))}
      </div>
      {gameOver && (
        <div className="game-over">
          <h2>{winner ? (winner === 'Draw' ? "It's a draw!" : `${winner} wins!`) : ''}</h2>
          <button onClick={handleReset}>Play Again</button>
        </div>
      )}
      {!gameOver && (
        <div className="status">
          <h2>Current Player: {currentPlayer}</h2>
        </div>
      )}
      <button onClick={handleReset}>Reset Game</button>
    </div>
  );
};

export default App;



