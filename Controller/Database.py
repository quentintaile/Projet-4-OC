from pathlib import Path
from tinydb import TinyDB, Query, where
from Models.Player import Player
from Models.Tournament import Tournament
from Models.Rounds import Round
from Models.Match import Match


def save_db(db_name, serialized_data):
    """Sauvegarde des données dans TinyDB."""
    Path("data/").mkdir(exist_ok=True)

    db_path = Path(f"data/{db_name}.json")
    db = TinyDB(db_path)

    db.insert(serialized_data)
    print(f"{serialized_data['name']} sauvegardé avec succès.")


def update_db(db_name, serialized_data):
    """Mise à jour des données dans TinyDB."""
    db = TinyDB(f"data/{db_name}.json")
    db.update(serialized_data, where('name') == serialized_data['name'])
    print(f"{serialized_data['name']} mis à jour avec succès.")


def update_player_rank(db_name, serialized_data):
    """Mise à jour du classement et score total du joueur."""
    db = TinyDB(f"data/{db_name}.json")
    db.update(
        {'rank': serialized_data['rank'], 'total_score': serialized_data['total_score']},
        where('name') == serialized_data['name']
    )
    print(f"Classement de {serialized_data['name']} mis à jour avec succès.")


def load_db(db_name):
    """Charge toutes les données d'une base TinyDB."""
    db = TinyDB(f"data/{db_name}.json")
    return db.all()


def load_player(serialized_player, load_tournament_score=False):
    """Charge un joueur à partir des données sérialisées."""
    player = Player(
        serialized_player["name"],
        serialized_player["first_name"],
        serialized_player["sex"],
        serialized_player["total_score"],
        serialized_player["rank"]
    )
    if load_tournament_score:
        player.tournament_score = serialized_player.get("tournament_score", 0)
    return player


def load_tournament(serialized_tournament):
    """Charge un tournoi à partir des données sérialisées."""
    loaded_tournament = Tournament(
        serialized_tournament["name"],
        serialized_tournament["place"],
        serialized_tournament["date"],
        serialized_tournament["time_control"],
        [load_player(player, load_tournament_score=True) for player in serialized_tournament["players"]],
        serialized_tournament["nb_rounds"],
        serialized_tournament["desc"]
    )
    loaded_tournament.rounds = load_rounds(serialized_tournament, loaded_tournament)
    return loaded_tournament


def load_rounds(serialized_tournament, tournament):
    """Charge les rounds d'un tournoi."""
    loaded_rounds = []

    for round_data in serialized_tournament["rounds"]:
        players_pairs = []
        
        for pair in round_data["players_pairs"]:
            pair_p1 = next((player for player in tournament.players if player.name == pair[0]["name"]), None)
            pair_p2 = next((player for player in tournament.players if player.name == pair[1]["name"]), None)

            if pair_p1 is None or pair_p2 is None:
                raise ValueError(f"Erreur : Impossible de trouver les joueurs {pair[0]['name']} ou {pair[1]['name']}.")

            players_pairs.append((pair_p1, pair_p2))

        loaded_round = Round(
            round_data["name"],
            players_pairs,
            load_match=True
        )
        loaded_round.matchs = [load_match(match, tournament) for match in round_data["matchs"]]
        loaded_round.start_date = round_data["start_date"]
        loaded_round.end_date = round_data["end_date"]
        loaded_rounds.append(loaded_round)

    return loaded_rounds


def load_match(serialized_match, tournament):
    """Charge un match à partir des données sérialisées."""
    player1 = next((player for player in tournament.players if player.name == serialized_match["player1"]["name"]), None)
    player2 = next((player for player in tournament.players if player.name == serialized_match["player2"]["name"]), None)

    if player1 is None or player2 is None:
        raise ValueError(f"Erreur : Impossible de trouver les joueurs {serialized_match['player1']['name']} ou {serialized_match['player2']['name']}.")

    loaded_match = Match(
        players_pair=(player1, player2),
        name=serialized_match['name']
    )
    loaded_match.score_player1 = serialized_match["score_player1"]
    loaded_match.color_player1 = serialized_match["color_player1"]
    loaded_match.score_player2 = serialized_match["score_player2"]
    loaded_match.color_player2 = serialized_match["color_player2"]
    loaded_match.winner = serialized_match["winner"]

    return loaded_match
