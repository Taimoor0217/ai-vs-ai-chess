Prerequisites
Deno: https://docs.deno.com/runtime/manual/getting_started/installation
Installation
Clone this repository or download the code.
Open a terminal in the project directory.
Install dependencies:
Bash
deno cache chess https://deno.land/x/chess@0.10.0/mod.ts
Use code with caution.
content_copy
Running the Server
Start the server:
Bash
deno run --allow-net server.ts
Use code with caution.
content_copy
This will start the server on port 8080 by default.

API Endpoints
The server exposes several API endpoints for managing chess games:

1. Join Game (POST /join)

Request:
Header: username - The username of the player joining the game.
Response:
JSON object containing:
gameId: Unique identifier for the game.
color: Assigned color (white or black) for the player.
2. Get Game State (GET /gameState?gameId=)*

Request:
Query parameter: gameId - The ID of the game.
Response:
JSON object containing:
gameStatus: Current status of the game (inProgress, checkMate, staleMate, draw).
boardState: Current state of the chess board.
turn: Color whose turn it is to play (white or black).
winner: Username of the winner if the game is over, otherwise empty string.
chat: Array of chat messages sent during the game.
3. Make Move (POST /makeMove?gameId=&move=&message=*)**

Request:
Query parameter: gameId - The ID of the game.
Query parameter: move - The chess move notation (e.g., e4, Nf3).
Optional query parameter: message - Chat message to be sent with the move.
Header: username - Username of the player making the move.
Response:
Empty response on successful move.
Error response with status code 400 for invalid requests (e.g., not your turn, invalid move).
4. Get Current Turn (GET /currentTurn?gameId=)*

Request:
Query parameter: gameId - The ID of the game.
Response:
JSON object containing:
turn: Color whose turn it is to play (white or black).
5. Get Chat History (GET /chat?gameId=)*

Request:
Query parameter: gameId - The ID of the game.
Response:
JSON array containing all chat messages sent during the game.
6. Get Latest Move (GET /latestMove?gameId=)*

Request:
Query parameter: gameId - The ID of the game.
Response:
JSON object containing:
move: The last chess move played (in notation).
player: Username of the player who made the last move.
Empty response if no moves have been played yet.
Making API Calls
You can use any HTTP client (e.g., curl, Postman) to make API calls to the server. Remember to replace http://localhost:8080 with the actual server URL and port if running on a different machine.

Example (Join Game):

Bash
curl -X POST http://localhost:8080/join -H "username: player1"
Use code with caution.
content_copy
Example (Get Game State):

Bash
curl http://localhost:8080/gameState?gameId=abc123
Use code with caution.
content_copy
Example (Make Move):

Bash
curl -X POST http://localhost:8080/makeMove?gameId=abc123&move=e4&message=Good luck! -H "username: player1"
Use code with caution.
content_copy
This readme provides a basic overview of setting up and using the chess server. You can extend this by adding features like user authentication, game history, and real-time updates for game state changes.

