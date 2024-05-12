import requests
import os
import asyncio
async def make_post_request(path: str, data: dict):
    url = os.environ['CHESS_SERVER_URL']+path
    print(url, data)
    response = requests.post(url, json=data)
    return response.json()

async def make_get_request(path: str, params: dict):
    url = os.environ['CHESS_SERVER_URL']+path
    print(url, params)
    response = requests.get(url, params)
    return response.json()

def make_get_request_s(path: str, params: dict):
    url = os.environ['CHESS_SERVER_URL']+path
    print(url, params)
    response = asyncio.run(requests.get(url, params))
    return asyncio.run(response.json())

async def join_game(game_id: str, user_name: str):
    return await make_post_request(f'/join?gameId={game_id}', {"userName": user_name})

async def get_curent_turn(game_id: str):
    return await make_get_request(f'/currentTurn?gameId={game_id}', {})