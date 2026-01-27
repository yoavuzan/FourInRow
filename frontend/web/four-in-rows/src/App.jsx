import React, { useState, useEffect, useRef } from "react";
import "./App.css";

const App = () => {
  const [board, setBoard] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState("X");
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [myRole, setMyRole] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket("wss://four-in-row.onrender.com/ws/game");
    socketRef.current = socket;

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "role") {
          setMyRole(data.role);
          return;
        }

        if (data.type === "update") {
          // Safeguard: Only update state if data exists in the message
          if (data.board) setBoard(data.board);
          if (data.currentPlayer) setCurrentPlayer(data.currentPlayer);
          if (data.gameOver !== undefined) setGameOver(data.gameOver);
          if (data.winner !== undefined) setWinner(data.winner);
        }

        if (data.type === "error") {
          console.error("Game Error:", data.message);
          alert(data.message);
        }
      } catch (err) {
        console.error("Error parsing message:", err);
      }
    };
    socket.onopen = () => console.log("WebSocket connected");
    socket.onclose = () => console.log("WebSocket closed");
    socket.onerror = (error) => console.error("WebSocket error:", error);

    return () => {
      if (
        socket.readyState === WebSocket.OPEN ||
        socket.readyState === WebSocket.CONNECTING
      ) {
        socket.close();
        console.log("Cleanup: Closing WebSocket");
      }
    };
  }, []);

  const handleCellClick = (col) => {
    const isSocketReady = socketRef.current?.readyState === WebSocket.OPEN;

    if (gameOver || !isSocketReady || currentPlayer !== myRole) {
      console.log("Invalid move attempt or socket not ready");
      return;
    }

    socketRef.current.send(JSON.stringify({ action: "move", col }));
  };

  const handleReset = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ action: "reset" }));
    }
  };

  const getPlayerClass = (cell) => {
    if (cell === "X") return "player-1";
    if (cell === "O") return "player-2";
    return "";
  };

  return (
    <div className="app">
      <h1>Four in a Row</h1>
      <h3>Your Role: {myRole}</h3>
      <h3>Current Turn: {currentPlayer}</h3>

      <div className="board">
        {board.map((row, rowIndex) => (
          <div key={rowIndex} className="row">
            {row.map((cell, colIndex) => (
              <div
                key={colIndex}
                className={`cell ${
                  cell ? `filled ${getPlayerClass(cell)}` : ""
                }`}
                onClick={() => handleCellClick(colIndex)}
              />
            ))}
          </div>
        ))}
      </div>

      {gameOver && (
        <div className="game-over">
          <h2>
            {winner
              ? winner === "Draw"
                ? "It's a draw!"
                : `${winner} wins!`
              : ""}
          </h2>
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
