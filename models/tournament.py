import json
from models.round import Round
from models.match import Match
from models.player import Player


class Tournament:
    def __init__(self, name, place, start_date, end_date, description, num_rounds=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.num_rounds = num_rounds
        self.current_round = 0
        self.rounds = []
        self.players = []

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "num_rounds": self.num_rounds,
            "current_round": self.current_round,
            "players": [player.chess_id for player in self.players],
            "rounds": [round_.to_dict() for round_ in self.rounds]
        }

    @staticmethod
    def from_dict(data, players_dict):
        tournament = Tournament(
            data["name"],
            data["place"],
            data["start_date"],
            data["end_date"],
            data["description"],
            data.get("num_rounds", 4)
        )
        tournament.current_round = data["current_round"]
        tournament.players = [players_dict[chess_id] for chess_id in data["players"]]
        tournament.rounds = [
            Round.from_dict(round_data, players_dict, Match)
            for round_data in data["rounds"]
        ]
        return tournament
