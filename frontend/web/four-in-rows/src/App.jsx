import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'https://fourinrow.onrender.com';

const App = () => {
  const [board, setBoard] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('');
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);

  const fetchGameState = async () => {
    try {
      const response = await fetch(`${API_URL}/game`);
      const data = await response.json();
      setBoard(data.board);
      setCurrentPlayer(data.currentPlayer);
      setGameOver(data.gameOver);
      setWinner(data.winner);
    } catch (error) {
      console.error("Error fetching game state:", error);
    }
  };

  useEffect(() => {
    fetchGameState();
  }, []);

  const handleCellClick = async (col) => {
    if (gameOver) return;

    try {
      const response = await fetch(`${API_URL}/game/move`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ col }),
      });
      const data = await response.json();
      if (data.success) {
        setBoard(data.board);
        setCurrentPlayer(data.currentPlayer);
        setGameOver(data.gameOver);
        setWinner(data.winner);
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error("Error making move:", error);
    }
  };

  const handleReset = async () => {
    try {
      const response = await fetch(`${API_URL}/game/reset`, { method: 'POST' });
      const data = await response.json();
      setBoard(data.board);
      setCurrentPlayer(data.currentPlayer);
      setGameOver(data.gameOver);
      setWinner(data.winner);
    } catch (error) {
      console.error("Error resetting game:", error);
    }
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

