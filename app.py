from quart import Quart, request
from quart_schema import QuartSchema
from leagueSchema import LeagueAccountSchema, LeagueAccountPUUID
from leagueApiService import get_account_details_by_puuid, get_account_details_by_username, get_free_champions_in_rotation, get_users_TFT_account
app = Quart(__name__)
QuartSchema(app)


@app.get("/get_league_user_account_details_by_username")
async def get_league_user_details():
    schema = LeagueAccountSchema()
    result = schema.load(await request.get_json())
    content = get_account_details_by_username(
        result["username"], result["tagLine"])
    return content, 200


@app.get("/get_league_user_account_details_by_puuid")
async def get_champion_masteries():
    schema = LeagueAccountPUUID()
    result = schema.load(await request.get_json())
    content = get_account_details_by_puuid(result["puuid"])
    return content, 200


@app.get("/get_champions_in_rotation")
def get_champions_in_rotation():
    content = get_free_champions_in_rotation()
    return content, 200


@app.get("/get_users_tft_account")
async def get_users_tft_account():
    schema = LeagueAccountPUUID()
    result = schema.load(await request.get_json())
    content = get_users_TFT_account(result["puuid"])
    return content, 200


if __name__ == "__main__":
    app.run()
