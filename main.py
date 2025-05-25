import requests
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore

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
        for team_data in data:
            if team_data['team']['id'] == team_id:
                return team_data
    return None  # return None if team not found

# makes a bar-plot of results by tour 
def show_results_by_tour(tournament_data, team_data):
    results_by_tour = []

    for tour in tournament_data['questionQty']:
        results = team_data['mask'][(int(tour)-1)*12:(int(tour)-1)*12+12]
        amount = 0
        for s in results:
            if s == '1':
                amount += 1
        results_by_tour.append(amount)        

    plt.plot(np.array(results_by_tour), marker='o')
    plt.show()

def main():
    show_results_by_tour(get_tournament_data(11908), get_tournament_data_for_team(11908,  93928))


if __name__ == "__main__":
    main()
