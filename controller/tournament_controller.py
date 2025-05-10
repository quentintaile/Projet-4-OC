import json
import random
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match


class TournamentController:
    def __init__(self, view):
        self.view = view
        self.players = self.load_players()
        self.tournaments = self.load_tournaments()

    def save_players(self):
        with open("data/players.json", "w") as f:
            json.dump([p.to_dict() for p in self.players.values()], f, indent=4)

    def load_players(self):
        players = {}
        try:
            with open("data/players.json", "r") as f:
                data = json.load(f)
                for player_data in data:
                    player = Player.from_dict(player_data)
                    players[player.chess_id] = player
        except FileNotFoundError:
            pass
        return players

    def save_tournaments(self):
        with open("data/tournaments.json", "w") as f:
            json.dump([t.to_dict() for t in self.tournaments], f, indent=4)

    def load_tournaments(self):
        tournaments = []
        try:
            with open("data/tournaments.json", "r") as f:
                data = json.load(f)
                for t_data in data:
                    tournament = Tournament.from_dict(t_data, self.players)
                    tournaments.append(tournament)
        except FileNotFoundError:
            pass
        return tournaments

    def add_player(self):
        player_info = self.view.get_player_info()
        if player_info["chess_id"] not in self.players:
            player = Player(**player_info)
            self.players[player.chess_id] = player
            self.save_players()
            self.view.show_message("Joueur ajouté avec succès.")
        else:
            self.view.show_message("Ce joueur existe déjà.")

    def create_tournament(self):
        tournament_info = self.view.get_tournament_info()
        tournament = Tournament(**tournament_info)
        self.tournaments.append(tournament)
        self.save_tournaments()
        self.view.show_message("Tournoi créé avec succès.")

    def list_players(self):
        players = sorted(self.players.values(), key=lambda x: (x.last_name, x.first_name))
        self.view.display_players(players)

    def list_tournaments(self):
        self.view.display_tournaments(self.tournaments)

    def start_tournament(self):
        tournament = self.view.choose_tournament(self.tournaments)
        if not tournament:
            return

        if not tournament.players:
            self.view.show_message("Aucun joueur inscrit.")
            return

        while tournament.current_round < tournament.num_rounds:
            self.play_round(tournament)
            tournament.current_round += 1
            self.save_tournaments()
        self.view.show_message("Le tournoi est terminé.")

    def play_round(self, tournament):
        round_name = f"Round {tournament.current_round + 1}"
        new_round = Round(round_name)

        if tournament.current_round == 0:
            players_list = tournament.players[:]
            random.shuffle(players_list)
        else:
            players_list = sorted(
                tournament.players,
                key=lambda p: p.score,
                reverse=True
            )

        matches = []
        already_paired = set()
        while players_list:
            p1 = players_list.pop(0)
            for idx, p2 in enumerate(players_list):
                if (p1.chess_id, p2.chess_id) not in already_paired and \
                   (p2.chess_id, p1.chess_id) not in already_paired:
                    match = Match(p1, p2)
                    matches.append(match)
                    already_paired.add((p1.chess_id, p2.chess_id))
                    players_list.pop(idx)
                    break

        new_round.matches = matches
        self.view.display_round(new_round)

        for match in matches:
            scores = self.view.get_match_result(match)
            match.score1, match.score2 = scores
            match.player1.score += match.score1
            match.player2.score += match.score2

        new_round.close_round()
        tournament.rounds.append(new_round)
