import { ChessGame } from "https://deno.land/x/chess@0.6.0/mod.ts";
import { serve } from "https://deno.land/std/http/server.ts";

const games: Map<
  string,
  {
    chess: ChessGame;
    white: string;
    black: string;
    chat: string[];
    canPlay: boolean;
  }
> = new Map();

function handleCreateGame(gameId: string) {
  if (games.has(gameId)) {
    return new Response("Game already exists", { status: 400 });
  }
  games.set(gameId, {
    chess: ChessGame.NewStandardGame(),
    white: "",
    black: "",
    chat: [],
    canPlay: false,
  });
}

function handleJoinGame(userName: string, gameId: string): Promise<Response> {
  const game = games.get(gameId);
  if (!game) {
    return Promise.resolve(new Response("Game not found", { status: 404 }));
  }

  const color = game.white === "" ? "white" : "black";
  game[color] = userName;
  if (game.white !== "" && game.black !== "") {
    game.canPlay = true;
  }
  console.log(`${userName} joined as ${color}`)
  return Promise.resolve(
    new Response(JSON.stringify({ gameId, color }), { status: 200 }),
  );
}

function handleGetGameState(gameId: string): Promise<Response> {
  const game = games.get(gameId);
  if (!game) {
    return Promise.resolve(new Response("Game not found", { status: 404 }));
  }
  const { chess, white, black, canPlay } = game;
  console.log(chess.toString());
  return Promise.resolve(
    new Response(
      JSON.stringify({
        gameStatus: chess.getStatus(),
        boardState: chess.toString("fen"),
        white,
        black,
        canPlay,
      }),
      { status: 200 },
    ),
  );
}

function handleMakeMove(
  userName: string,
  gameId: string,
  move: string,
  message?: string,
): Promise<Response> {
  const game = games.get(gameId);
  if (!game) {
    return Promise.resolve(new Response(JSON.stringify({message: "Invalid game"}), { status: 404 }));
  }
  const { chess, white, black } = game;
  const gameState = chess.getStatus();
  if (
    (gameState.turn === "white" && userName !== white) ||
    (gameState.turn === "black" && userName !== black)
  ) {
    return Promise.resolve(new Response(JSON.stringify({message: "Not your turn"}), { status: 400 }));
  }
  const result = chess.move(move);
  if (!result) {
    return Promise.resolve(new Response(JSON.stringify({message:"Invalid move, check the board state and confirm you are making the right move?"}), { status: 400 }));
  }
  if (message) {
    game.chat.push(`${userName}: ${message}`);
  }
  return Promise.resolve(new Response(JSON.stringify({message: "Move processed successfully"}), { status: 200 }));
}

function handleGetCurrentTurn(gameId: string): Promise<Response> {
  const game = games.get(gameId);
  if (!game) {
    return Promise.resolve(new Response("Game not found", { status: 404 }));
  }
  const { chess } = game;
  return Promise.resolve(
    new Response(JSON.stringify({ turn: chess.getStatus().turn }), {
      status: 200,
    }),
  );
}

function handleGetChat(gameId: string): Promise<Response> {
  const game = games.get(gameId);
  if (!game) {
    return Promise.resolve(new Response("Game not found", { status: 404 }));
  }
  const { chat } = game;
  return Promise.resolve(new Response(JSON.stringify(chat), { status: 200 }));
}

function handleGetLatestMove(gameId: string): Promise<Response> {
  const game = games.get(gameId);
  if (!game) {
    return Promise.resolve(new Response("Game not found", { status: 404 }));
  }
  const { chess } = game;
  const previousMove = chess.history().slice(-1)[0];
  if (!previousMove) {
    return Promise.resolve(
      new Response("No moves played yet", { status: 200 }),
    );
  }
  const player = chess.getStatus().turn === "white" ? game.black : game.white;
  return Promise.resolve(
    new Response(JSON.stringify({ move: previousMove, player }), {
      status: 200,
    }),
  );
}
const handler = async (req: Request) => {
  const url = new URL(req.url);
  const gameId = url.searchParams.get("gameId");
  console.log(url.pathname, gameId);
  if (!gameId) {
    return Promise.resolve(
      new Response("gameId parameter is missing", { status: 400 }),
    );
  }
  switch (url.pathname) {
    case "/join": {
      const data = await req.json();
      console.log(data);
      return await handleJoinGame(data.userName, gameId);
    }
    case "/gameState": {
      return await handleGetGameState(gameId);
    }
    case "/makeMove": {
      const data = await req.json();
      console.log(data);
      return await handleMakeMove(
        data.userName,
        gameId,
        data.move,
        data.message,
      );
    }
    case "/currentTurn": {
      return await handleGetCurrentTurn(gameId);
    }
    case "/chat": {
      return await handleGetChat(gameId);
    }
    case "/latestMove": {
      return await handleGetLatestMove(gameId);
    }
    default: {
      console.log("404 req came in");
      return new Response("Not found", { status: 404 });
    }
  }
};
handleCreateGame("UltimateBattle");
serve(handler, { port: 8008 });

