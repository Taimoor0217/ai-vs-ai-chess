import sys 
import os
import asyncio
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
__package__ = 'Tools'

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from Tools.chess_toolkit import GetChessGameStateTool, MakeChessMoveTool, GetCurrentTurnTool
from Tools.api import join_game, get_curent_turn

model = "gpt-4"
userName = sys.argv[1]
gameId = "UltimateBattle"
res = asyncio.run(join_game(gameId, userName))
color = res['color']


llm = ChatOpenAI(model=model)
tools = [GetChessGameStateTool(), MakeChessMoveTool(), GetCurrentTurnTool()]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f'You are great chess player who is playing with a very competitive player.  Your username is {userName}. You are playing as {color}. The game id is {gameId}. Make sure to always use GetChessGameStateTool to get the current state of the game before making a move. And use MakeChessMoveTool to make a move. You goal is to win the game. If the game is over, exit',
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

async def wait_for_turn(sec: int=2):
    while True:
        res = await get_curent_turn(gameId)
        if res['turn'] == color:
            print("My turn to make a move...")
            return
        else:
            print("Waiting for the opponent to make a move...")
        time.sleep(sec)
# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# agent_executor.invoke({"input": f'Lets win this chess game!, Use UCI format to make a move, the board state returned in FEN format, stop when the game is over. If it is not your turn, then wait for sometime to check again. If the server response mentions and incorrect input, make sure to remake the call with right input'})
asyncio.run(wait_for_turn())
for step in agent_executor.iter({"input": f'Lets win this chess game!, Use UCI format to make a move, the board state returned in FEN format, stop when the game is over. If it is not your turn, then wait for sometime to check again. If the server response mentions and incorrect input, make sure to remake the call with right input'}):
    try: 
        loop = asyncio.get_running_loop()
        task = loop.create_task(wait_for_turn())
        loop.run_until_complete(task)
    except Exception as e:
        asyncio.run(wait_for_turn())
    # if output := step.get("intermediate_step"):
    #     action, value = output[0]
    #     if action.tool == "GetPrime":
    #         print(f"Checking whether {value} is prime...")
    #         assert is_prime(int(value))
    #     # Ask user if they want to continue
    #     _continue = input("Should the agent continue (Y/n)?:\n") or "Y"
    #     if _continue.lower() != "y":
    #         break