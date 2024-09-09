def calculate_team_statistics(data):
    teams_stats = {}
    for match in data.get('matches', []):
        home_team = match['home_team']
        away_team = match['away_team']
        home_goals, away_goals = map(int, match['result'].split(':'))

        if home_team not in teams_stats:
            teams_stats[home_team] = {'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'goals_for': 0,
                                      'goals_against': 0, 'goal_difference': 0, 'points': 0}
        if away_team not in teams_stats:
            teams_stats[away_team] = {'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'goals_for': 0,
                                      'goals_against': 0, 'goal_difference': 0, 'points': 0}

        teams_stats[home_team]['played'] += 1
        teams_stats[away_team]['played'] += 1
        teams_stats[home_team]['goals_for'] += home_goals
        teams_stats[home_team]['goals_against'] += away_goals
        teams_stats[away_team]['goals_for'] += away_goals
        teams_stats[away_team]['goals_against'] += home_goals
        teams_stats[home_team]['goal_difference'] = teams_stats[home_team]['goals_for'] - teams_stats[home_team][
            'goals_against']
        teams_stats[away_team]['goal_difference'] = teams_stats[away_team]['goals_for'] - teams_stats[away_team][
            'goals_against']

        if home_goals > away_goals:
            teams_stats[home_team]['won'] += 1
            teams_stats[away_team]['lost'] += 1
            teams_stats[home_team]['points'] += 3
        elif home_goals < away_goals:
            teams_stats[away_team]['won'] += 1
            teams_stats[home_team]['lost'] += 1
            teams_stats[away_team]['points'] += 3
        else:
            teams_stats[home_team]['drawn'] += 1
            teams_stats[away_team]['drawn'] += 1
            teams_stats[home_team]['points'] += 1
            teams_stats[away_team]['points'] += 1

    return teams_stats
