import requests
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
import argparse


def get_tournament_data(tournament_id) -> dict:
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}.json?includeMasksAndControversials=1"
    response = requests.get(url)
    return response.json()


def get_tournament_results(tournament_id) -> dict:
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}/results.json?includeMasksAndControversials=1"
    response = requests.get(url)
    return response.json()


# getting tournament results for ypur team
def get_tournament_data_for_team(tournament_id, team_id) -> dict:
    url = f"https://api.rating.chgk.info/tournaments/{tournament_id}/results.json?includeMasksAndControversials=1"
    response = requests.get(url)
    # make sure the response is successful and parse JSON
    if response.status_code == 200:
        data = response.json()
        print(f"Looking for team {team_id} in {len(data)} teams")
        for team_data in data:
            if int(team_data['team']['id']) == int(team_id):
                print(f"Found team: {team_data['team']['name']}")
                return team_data
    print("Team not found :(")
    return {}  # return None if team not found


def show_relative_results_by_tour(tournament_results: dict, team_data: dict, tournament_tours_q: dict, tournament_name: str) -> None:
    # error handling
    if not tournament_results or not team_data:
        print("tournament results or team data or tours amount not found while counting avg by tour")
        return

    # array of 1s
    sum_by_tour = np.zeros(len(tournament_tours_q))
    print(sum_by_tour)

    # getting results of each team
    for team in tournament_results:
        results_by_tour = []
        tours = tournament_tours_q.keys()
        max_questions = max(tournament_tours_q.values())

        # counting answered questions for each tour
        for tour in tours:
            tour_questions = tournament_tours_q[tour]
            start_idx = (int(tour) - 1) * tour_questions
            end_idx = start_idx + tour_questions
            results = team['mask'][start_idx:end_idx]
            correct = results.count('1')
            results_by_tour.append(correct)

        print(results_by_tour)
        # updating avg score
        for i in range(len(results_by_tour)):
            sum_by_tour[i] += results_by_tour[i]

        print(sum_by_tour)

    team_amount = len(tournament_results)

    avg_by_tour = sum_by_tour
    for i in range(len(sum_by_tour)):
        avg_by_tour[i] = sum_by_tour[i] / team_amount

    print(avg_by_tour)

    # counting user's team results
    results_by_tour = []
    tours = tournament_tours_q.keys()
    max_questions = max(tournament_tours_q.values())

    # counting answered questions for each tour
    for tour in tours:
        tour_questions = tournament_tours_q[tour]
        start_idx = (int(tour) - 1) * tour_questions
        end_idx = start_idx + tour_questions
        results = team_data['mask'][start_idx:end_idx]
        correct = results.count('1')
        results_by_tour.append(correct)

    # making a plot
    plt.figure(figsize=(10, 5))

    # plot of user's team results
    plt.plot(tours, results_by_tour, marker='o', linestyle='-', color='r', label='результат команды')

    # plot of avg results
    plt.plot(tours, avg_by_tour, marker='o', linestyle=':', color='b', label='средний результат на турнире')
    # plot of differences
    diffs = [results_by_tour[i] - avg_by_tour[i] for i in range(len(avg_by_tour))]
    plt.plot(tours, diffs, marker='o', linestyle='-.', color='g', label='выигрыш команды относительно среднего')

    # add value labels near each marker
    avg_values = []
    for i, (x, y) in enumerate(zip(tours, avg_by_tour)):
        avg_values.append(y)
        plt.text(x, y + 0.2, str(y),  # x, y+offset, text
                 ha='center',  # horizontal alignment
                 va='bottom',  # vertical alignment
                 fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    for i, (x, y) in enumerate(zip(tours, results_by_tour)):
        plt.text(x, y + 0.2, str(y),  # x, y+offset, text
                 ha='center',  # horizontal alignment
                 va='bottom',  # vertical alignment
                 fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    for i, (x, y) in enumerate(zip(tours, diffs)):
        plt.text(x, y + 0.2, f'+{str(round(y, 2))}' if y >= 0 else f'-{str(y)}',  # x, y+offset, text
                 ha='center',  # horizontal alignment
                 va='bottom',  # vertical alignment
                 fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))

    # format the plot
    plt.ylim(bottom=1, top=max_questions)
    plt.yticks(np.arange(0, max_questions + 1, step=1))

    plt.title(f"Взятые по турам - {team_data['team']['name']} - {tournament_name}")
    plt.xlabel("номер тура")
    plt.ylabel("взято")
    plt.grid(True)
    plt.legend(loc='best', fontsize='small')
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Анализ результатов турнира")
    parser.add_argument("tournament_id", help="tournament ID")
    parser.add_argument("team_id", help="team ID")
    args = parser.parse_args()
    show_relative_results_by_tour(get_tournament_results(args.tournament_id),
                                  get_tournament_data_for_team(args.tournament_id, args.team_id),
                                  get_tournament_data(args.tournament_id)['questionQty'],
                                  get_tournament_data(args.tournament_id)['name'])


if __name__ == "__main__":
    main()
