import requests
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import argparse

def get_tournament_data(tournament_id) -> dict:
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}.json?includeMasksAndControversials=1"
    response = requests.get(url)
    return response.json()

# getting tournament results for ypur team
def get_tournament_data_for_team(tournament_id, team_id) -> dict:
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

# makes a plot of results by tour 
def show_results_by_tour(tournament_data: dict, team_data: dict) -> None:
    if not tournament_data or not team_data:
        print("Error: Missing tournament or team data")
        return

    results_by_tour = []
    tours = sorted(tournament_data['questionQty'].keys(), key=int)
    max_questions = max(tournament_data['questionQty'].values())

    for tour in tours:
        tour_questions = tournament_data['questionQty'][tour]
        start_idx = (int(tour)-1)*tour_questions
        end_idx = start_idx + tour_questions
        results = team_data['mask'][start_idx:end_idx]
        correct = results.count('1')
        results_by_tour.append(correct)

    plt.figure(figsize=(10, 5))
    plt.plot(tours, results_by_tour, marker='o', linestyle='-', color='b')
    
    # Set Y-axis limits
    plt.ylim(bottom=1, top=max_questions)
    plt.yticks(np.arange(0, max_questions + 1, step=1))
    
    # Add labels and title
    plt.title(f"Взятые по турам - {team_data['team']['name']} на турнире {tournament_data['name']}")
    plt.xlabel("номер тура")
    plt.ylabel("взято")
    plt.grid(True)
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Анализ результатов турнира")
    parser.add_argument("tournament_id", help="tournament ID")
    parser.add_argument("team_id", help="team ID")
    args = parser.parse_args()
    show_results_by_tour(get_tournament_data(args.tournament_id), get_tournament_data_for_team(args.tournament_id,  args.team_id))


if __name__ == "__main__":
    main()
