const { useState, useEffect } = React;

const ChessGame = () => {
  const [gameState, setGameState] = useState(null);
  const [chat, setChat] = useState([]);

  useEffect(() => {
    const fetchGameState = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8008/gameState?gameId=UltimateBattle');
        if (response.ok) {
          const data = await response.json();
          setGameState(data);
        } else {
          console.error('Failed to fetch game state');
        }
      } catch (error) {
        console.error('Error fetching game state:', error);
      }
    };

    const fetchChat = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8008/chat?gameId=UltimateBattle');
        if (response.ok) {
          const data = await response.json();
          setChat(data);
        } else {
          console.error('Failed to fetch chat');
        }
      } catch (error) {
        console.error('Error fetching chat:', error);
      }
    };
    const intervalId = setInterval(() => {
      fetchGameState();
      fetchChat();
    }, 1000); // Fetch every second

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    var ruyLopez = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R'
    if (gameState) {
      // Render chessboard
      const board = Chessboard('board', {
        draggable: true,
        position: gameState.boardState,
        onDrop: (source, target) => {
          // Handle move logic here
        }
      });
    }
  }, [gameState]);
  const currMove = gameState && gameState[gameState.gameStatus.turn]
  return (
    <div>
      <div id="game-header">
        {gameState && (
          <div id="game-info">
            <p>White: {gameState.white}</p>
            <p>Black: {gameState.black}</p>
            <p>Game State: {gameState.gameStatus.state}</p>
            {currMove && <h2>{currMove} is making a move...</h2>}
          </div>
        )}
      </div>
    <div id="container">
      <div id="board"></div>
      <div id="chat-panel">
        <h2>Chat</h2>
        <ul>
          {chat.map((cht, index) => {
             const [name, message]= cht.split(':')
            return <div class="message" key={index}>
               <span class="name">{name} :</span>{message}
            </div>
}         )}
        </ul>
      </div>
    </div>
    </div>
  );
};

ReactDOM.render(<ChessGame />, document.getElementById('root'));
