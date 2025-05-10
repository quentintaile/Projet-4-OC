from datetime import datetime


class Round:
    def __init__(self, name):
        self.name = name
        self.matches = []
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None

    def close_round(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "matches": [match.to_tuple() for match in self.matches],
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @staticmethod
    def from_dict(data, players_dict, Match):
        round_instance = Round(data["name"])
        round_instance.matches = [
            Match.from_tuple(match, players_dict)
            for match in data["matches"]
        ]
        round_instance.start_time = data["start_time"]
        round_instance.end_time = data["end_time"]
        return round_instance
