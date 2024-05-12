# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

from typing import Optional, Type, Union, List, Dict
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
import asyncio
from .api import make_post_request, make_get_request, make_get_request_s

"""GetChessGameStateTool"""
class GetChessGameStateInput(BaseModel):
    game_id: str = Field(description="id of the game you want to get the state of")

class GetChessGameStateTool(BaseTool):
    """Tool that queries the chess server and gets the current state of a chess game."""
    """Sample response: {
    "gameStatus": {
        "state": "active",
        "turn": "white"
    },
    "boardState": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "white": "Gemini",
    "black": "Gpt",
    "canPlay": true
    }
    """
    name: str = "GetChessGameStateTool"
    description: str =(
        "A tool that helps to get the current state of a chess game from the chess server." 
        "Useful when you want to analyze the current state of a chess game to identiyfy what move to make next"
        "The boardState in the output is always returned as a Forsyth-Edwards Notation (FEN) string." 
        "Use the async call and Input should be the game id."
    )
    args_schema: Type[BaseModel] = GetChessGameStateInput

    def _run(
        self, 
        game_id: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            print("Calling sync run: GetChessGameStateTool", game_id)
            return asyncio.run(make_get_request(f'/gameState?gameId={game_id}', {}))
        except Exception as e:
            print("Error in sync run: GetChessGameStateTool", e)
            return repr(e)
    async def _arun(
        self, 
        game_id: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously."""
        try:
            print("Calling async run: GetChessGameStateTool")
            return await make_get_request(f'/gameState?gameId={game_id}', {})
        except Exception as e:
            print("Error in async run: GetChessGameStateTool", e)
            return repr(e)


""""MakeChessMoveTool"""
class MakeChessMoveInput(BaseModel):
    game_id: str = Field(description="the game id of the game you want to make a move in")
    user_name: str = Field(description="username of the player making the move")
    move: str = Field(description="move to make in the game in Universal Chess Interface (UCI) format")
    message: str = Field(description="a spicy message to send to the opponent to comment on the game state or the move made")

class MakeChessMoveTool(BaseTool):
    """Tool that queries the chess server and makes a move in a chess game."""
    name: str = "MakeChessMoveTool"
    description: str =(
        "A tool that helps to make a move in a chess game on the chess server." 
        "Useful when you want to make a move in a chess game." 
        "Use the async call and the Input should be the game id, username of the player, move in Universal Chess Interface (UCI) format and a message to send to the opponent"
    )
    args_schema: Type[BaseModel] = MakeChessMoveInput

    def _run(
        self, 
        game_id: str, 
        user_name: str,
        move: str,
        message: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            return asyncio.run(make_post_request(f'/makeMove?gameId={game_id}', {"userName": user_name, "move": move, "message": message,}))
        except Exception as e:
            return repr(e)
    async def _arun(
        self, 
        game_id: str, 
        user_name: str,
        move: str,
        message: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously."""
        try:
            return await make_post_request(f'/makeMove?gameId={game_id}', {"userName": user_name, "move": move, "message": message,})
        except Exception as e:
            return repr(e)


"""GetCurrentTurnTool"""
class GetCurrentTurnInput(BaseModel):
    game_id: str = Field(description="id of the game you want to check the turn of")

class GetCurrentTurnTool(BaseTool):
    """Tool that queries the chess server and gets the current state of a chess game."""
    name: str = "GetCurrentTurnTool"
    description: str =(
        "A tool that helps you check whose turn it is in a chess game from the chess server."
        "Useful when you want to know if it is your turn to make a move in a chess game." 
        "Use the async call and Input should be the game id."
    )
    args_schema: Type[BaseModel] = GetCurrentTurnInput

    def _run(
        self, 
        game_id: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Union[List[Dict], str]:
        """Use the tool."""
        try:
            return asyncio.run(make_get_request(f'/currentTurn?gameId={game_id}', {}))
        except Exception as e:
            return repr(e)
    async def _arun(
        self, 
        game_id: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously."""
        try:
            return await make_get_request(f'/currentTurn?gameId={game_id}', {})
        except Exception as e:
            return repr(e)