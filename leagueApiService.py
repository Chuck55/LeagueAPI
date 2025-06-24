import string
import requests
from secrets import api_key

headers = {
    "X-Riot-Token": api_key
}


def get_account_details_by_username(username: string, tagLine: string):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tagLine}"
    response = requests.get(
        url, headers=headers, timeout=10)
    return response.json()


def get_account_details_by_puuid(puuid: string):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    response = requests.get(url, headers=headers, timeout=10)
    return response.json()


def get_free_champions_in_rotation():
    url = "https://na1.api.riotgames.com/lol/platform/v3/champion-rotations"
    response = requests.get(url, headers=headers, timeout=10)
    champion_id_list = get_champion_id_map(version="14.12.1")

    champion_ids = response.json()["freeChampionIds"]
    champions_names_for_all_players = list(
        map(champion_id_list.get, champion_ids))

    new_player_champion_ids = response.json()["freeChampionIdsForNewPlayers"]
    champions_names_for_new_players = list(
        map(champion_id_list.get, new_player_champion_ids))
    return {
        "free_champions": champions_names_for_all_players,
        "free_champions_for_new_players": champions_names_for_new_players
    }


def get_champion_masteries(puuid: str):
    url = f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
    response = requests.get(url, headers=headers, timeout=10)
    champion_list_map = get_champion_id_map(version="14.12.1")
    high_mastery_champions = [champion for champion in response.json()
                              if champion["championLevel"] > 10]
    consise_list = list(map(lambda champion: {
        "champion_Id": champion["championId"],
        "champion_name": champion_list_map.get(champion["championId"]),
        "champion_points": champion["championPoints"],
        "champion_level": champion["championLevel"]
    },
        high_mastery_champions))
    return consise_list


def get_users_TFT_account(puuid: string):
    url = f"https://na1.api.riotgames.com/tft/league/v1/by-puuid/{puuid}"
    response = requests.get(url, headers=headers, timeout=10)
    return response.json()


def get_champion_id_map(version="14.12.1"):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.get(url, timeout=10)
    data = response.json()["data"]

    # Create a dict: {champion_id: champion_name}
    id_map = {}
    for champ in data.values():
        id_map[int(champ["key"])] = champ["name"]
    return id_map
