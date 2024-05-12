# AI vs AI Chess
Making LLMs play competitve chess each other using agentic workflows
[Video]('./screeshots/Ai_vs_Ai_Chess.mp4')

## Tools used
- `Langchain` for creating tools and agents
- `Langsmith` for agent workflow analysis
- `Deno-Chess` for mainting headless chess server 
- `Chessboardjs` for spectating chess game

## Running locally

### Running the chess server
- Install deno `irm https://deno.land/install.ps1 | iex`
- `Deno run --allow-net .\GameServer\GameServer.ts`

### Running the Spectator
- `npx lite-server --baseDir="Spectate"`

### Running the Agents
- Rename the `.env.sample` file to `.env`
- Add in your secrets and api keys. You donot need to add all the API keys, just the ones that you plan to use.
- Run `poetry install`
- Run `poetry run python ./Agents/chess_agent.py <Player_Name> <agent_mode> <model_to_use>`
- Example: `poetry run python ./Agents/chess_agent.py Gpt-4 structured_chat gpt-4` will run a `structured chat` agent (preffered), with `gpt-4` as the model and `Gpt-4` as user name.
- Run two instances of the `chess_agent` and they will start playing with each other.
- Head over to `http://localhost:3000` to spectate the game


## Actively waiting for turn vs letting the LLM wait for their turn
- Currently, to optimize the RPs, I have set the logic to actively wait for the LLM's turn before executing the next run.
- If you would like to change that to let the `LLM` handle it by default, uncomment the following line (#92 as of now) 
- `agent_executor.invoke({"input": input_string})`

