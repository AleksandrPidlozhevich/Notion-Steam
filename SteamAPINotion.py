import requests
from notion_client import Client

# Replace "YOUR_STEAM_API_KEY" with your Steam Web API Key
STEAM_API_KEY = ""
STEAM_ID = ""

# Get the Notion API Integration Token and Database ID
notion = Client(auth="")
database_id = ""

# Get list of game id from Steam account
response = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json")
game_ids = [game["appid"] for game in response.json()["response"]["games"]]

# Get information about games from the Steam API
new_games = []
for game_id in game_ids:
    response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game_id}")
    game_data = response.json()
    if game_data[str(game_id)]["success"]:
        game_name = game_data[str(game_id)]["data"]["name"]
        new_game = {"Name": {"title": [{"text": {"content": game_name}}]}, "Game ID": {"number": game_id}, "Platform's": {"multi_select": [{"name": "Steam"}]}}
        # Checking for the uniqueness of the game
        existing_game = notion.databases.query(database_id, filter={"property": "Game ID", "number": {"equals": game_id}}).get("results")
        if len(existing_game) == 0:
            new_games.append(new_game)

# For each new game, create a new page in the database
for new_game in new_games:
    notion.pages.create(parent={"database_id": database_id}, properties=new_game)