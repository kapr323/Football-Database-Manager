import json

class Player:
    def __init__(self, first_name, last_name, short_name, nationality, born_in_season, profile_picture=None):
        self.first_name = first_name
        self.last_name = last_name
        self.short_name = short_name
        self.nationality = nationality
        self.born_in_season = born_in_season
        self.profile_picture = profile_picture

def load_players(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        players = []
        for player_data in data['players']:
            player = Player(
                first_name=player_data['first_name'],
                last_name=player_data['last_name'],
                short_name=player_data['short_name'],
                nationality=player_data['nationality'],
                born_in_season=player_data['born_in_season'],
                profile_picture=player_data.get('profile_picture')
            )
            players.append(player)
        return players

# Usage example
players = load_players('Data/players.json')
for player in players:
    print(f"{player.first_name} {player.last_name} ({player.short_name}), {player.nationality}, Born in: {player.born_in_season}")
    if player.profile_picture:
        print(f"Profile picture: {player.profile_picture}")
