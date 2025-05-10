import json


class Player:
    def __init__(self, last_name, first_name, birth_date, chess_id):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.score = 0

    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "score": self.score
        }

    @staticmethod
    def from_dict(data):
        player = Player(
            data["last_name"],
            data["first_name"],
            data["birth_date"],
            data["chess_id"]
        )
        player.score = data.get("score", 0)
        return player
