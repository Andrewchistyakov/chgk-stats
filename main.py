import requests
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import argparse

def get_tournament_data(tournament_id):
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}.json?includeMasksAndControversials=1"
    response = requests.get(url)
    return response.json()

# getting tournament results for ypur team
def get_tournament_data_for_team(tournament_id, team_id):
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}/results.json?includeMasksAndControversials=1"
    response = requests.get(url)
    # Make sure the response is successful and parse JSON
    if response.status_code == 200:
        data = response.json()
        print(f"Looking for team {team_id} in {len(data)} teams")
        for team_data in data:
            if int(team_data['team']['id']) == int(team_id):
                print(f"Found team: {team_data['team']['name']}")
                return team_data
    print("Team not found")
    return None  # return None if team not found

# makes a bar-plot of results by tour 
def show_results_by_tour(tournament_data, team_data):
    results_by_tour = []

    for tour in tournament_data['questionQty']:
        tour_questions = tournament_data['questionQty'][tour]
        results = team_data['mask'][(int(tour)-1)*tour_questions:(int(tour)-1)*tour_questions+tour_questions]
        amount = 0
        for s in results:
            if s == '1':
                amount += 1
        results_by_tour.append(amount)        

    plt.plot(np.array(results_by_tour), marker='o')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Анализ результатов турнира")
    parser.add_argument("tournament_id", help="tournament ID")
    parser.add_argument("team_id", help="team ID")
    args = parser.parse_args()
    print(args)
    show_results_by_tour(get_tournament_data(args.tournament_id), get_tournament_data_for_team(args.tournament_id,  args.team_id))


if __name__ == "__main__":
    main()
