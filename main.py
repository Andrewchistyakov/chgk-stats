import requests

def get_tournament_data(tournament_id):
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}.json?includeMasksAndControversials=1"
    response = requests.get(url)
    return response.json()

# getting tournament results for ypur team
def get_tournament_data_for_team(tournament_id, team_id):
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}results.json?includeMasksAndControversials=1"
    response = requests.get(url)
    for team_data in response.json():
        if team_data['team']['id'] == team_id:
            return team_data
    return None  # return None if team not found

def get()

def main():
    print(get_tournament_data(11908))


if __name__ == "__main__":
    main()
