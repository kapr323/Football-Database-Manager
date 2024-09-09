def calculate_team_statistics(data):
    teams_stats = {}
    matches = data.get('matches', [])
    tournament_type = data.get('tournament', {}).get('type', '')

    for match in matches:
        home_team = match['home_team']
        away_team = match['away_team']

        # Získání výsledků zápasu
        home_goals = match.get('home_goals', 0)
        away_goals = match.get('away_goals', 0)
        status = match.get('status', 'Finished')  # Získáme stav zápasu, výchozí je "Finished"

        # Inicializace statistik pro domácí a hostující tým, pokud ještě neexistují
        if home_team not in teams_stats:
            teams_stats[home_team] = {'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'goals_for': 0,
                                      'goals_against': 0, 'goal_difference': 0, 'points': 0}
        if away_team not in teams_stats:
            teams_stats[away_team] = {'played': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'goals_for': 0,
                                      'goals_against': 0, 'goal_difference': 0, 'points': 0}

        # Aktualizace statistik - počet zápasů a skóre
        teams_stats[home_team]['played'] += 1
        teams_stats[away_team]['played'] += 1
        teams_stats[home_team]['goals_for'] += home_goals
        teams_stats[home_team]['goals_against'] += away_goals
        teams_stats[away_team]['goals_for'] += away_goals
        teams_stats[away_team]['goals_against'] += home_goals
        teams_stats[home_team]['goal_difference'] = teams_stats[home_team]['goals_for'] - teams_stats[home_team]['goals_against']
        teams_stats[away_team]['goal_difference'] = teams_stats[away_team]['goals_for'] - teams_stats[away_team]['goals_against']

        # Zpracování stavu zápasu v závislosti na typu turnaje (Liga)
        if tournament_type == "League":
            if status == "Finished":
                # Standardní bodování - 3 body za výhru, 1 bod za remízu
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

            elif status == "After OT" or status == "After SO":
                # Zpracování zápasů po prodloužení nebo po nájezdech
                if home_goals > away_goals:
                    teams_stats[home_team]['won'] += 1
                    teams_stats[away_team]['lost'] += 1
                    teams_stats[home_team]['points'] += 2
                    teams_stats[away_team]['points'] += 1
                elif home_goals < away_goals:
                    teams_stats[away_team]['won'] += 1
                    teams_stats[home_team]['lost'] += 1
                    teams_stats[away_team]['points'] += 2
                    teams_stats[home_team]['points'] += 1

                # V případě "After SO" nepočítáme vítězný gól do skóre
                if status == "After SO":
                    # Upravíme skóre tak, aby se vítězný gól z nájezdů nepočítal
                    teams_stats[home_team]['goals_for'] -= 1
                    teams_stats[away_team]['goals_against'] -= 1
                    teams_stats[home_team]['goal_difference'] = teams_stats[home_team]['goals_for'] - teams_stats[home_team]['goals_against']
                    teams_stats[away_team]['goal_difference'] = teams_stats[away_team]['goals_for'] - teams_stats[away_team]['goals_against']

    return teams_stats
