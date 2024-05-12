__package__ = 'Tools'

import sys 
import os
import asyncio
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_anthropic import ChatAnthropic

from Tools.chess_toolkit import GetChessGameStateTool, MakeChessMoveTool, GetCurrentTurnTool
from Tools.api import join_game, get_curent_turn

userName = sys.argv[1]
gameId = "UltimateBattle"
res = asyncio.run(join_game(gameId, userName))
color = res['color']
agent_type = sys.argv[2]
tools = [GetChessGameStateTool(), MakeChessMoveTool(), GetCurrentTurnTool()]


async def wait_for_turn(sec: int=2):
    while True:
        res = await get_curent_turn(gameId)
        if res['turn'] == color:
            print("My turn to make a move...")
            return
        else:
            print("Waiting for the opponent to make a move...")
        time.sleep(sec)

def initialize_llm():
    model_to_use = sys.argv[3]
    match model_to_use:
        case "hf_llama3":
            return HuggingFaceTextGenInference(
            inference_server_url=os.environ['HF_LLMA3_URL'],
            max_new_tokens=512,
            top_k=50,
            temperature=0.1,
            repetition_penalty=1.03,
            server_kwargs={
                "headers": {
                    "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
                    "Content-Type": "application/json",
                }
            })
        case "claude-3":
            return ChatAnthropic(model="claude-3-sonnet-20240229")
        case _:
            return ChatOpenAI(model="gpt-4")

llm = initialize_llm()    
prompt = prompt = hub.pull("hwchase17/structured-chat-agent") if agent_type == "structured_chat" else ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assitant who is good at playing chess
            Make sure to always use GetChessGameStateTool to get the current state of the game before making a move
            And use MakeChessMoveTool to make a move
            The board state is returned in Forsyth-Edwards Notation (FEN) format
            The moves should be in Universal Chess Interface (UCI) format
            Keep going until the game is over"""
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
) 

agent = create_structured_chat_agent(llm, tools=tools, prompt=prompt) if agent_type == "structured_chat" else create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=1000)


# Invoking the agent executor
input_string =  """
    "Your goal is to win this chess game. By checkmating the opponent's king.
     Your username is {userName}, the game id is {gameId} and you are playing as {color}.
     Carefully analyze the game state and make a move. You must eliminate maximum no of opponent's pieces.
     You should also send spicy and roasting messages to the opponent.
     The board state is returned in Forsyth-Edwards Notation (FEN) format
     The moves should be in Universal Chess Interface (UCI) format
     If it is other player's turn, donot exit keep on checking the game state.
     You must not finish util the game is over.
""".format(userName=userName, gameId=gameId, color=color)
# agent_executor.invoke({"input": input_string})
asyncio.run(wait_for_turn())
for step in agent_executor.iter({"input": input_string}):
    try: 
        loop = asyncio.get_running_loop()
        task = loop.create_task(wait_for_turn(1))
        loop.run_until_complete(task)
    except Exception as e:
        asyncio.run(wait_for_turn(1))