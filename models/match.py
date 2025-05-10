class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_tuple(self):
        return [
            [self.player1.chess_id, self.score1],
            [self.player2.chess_id, self.score2]
        ]

    @staticmethod
    def from_tuple(data, players_dict):
        p1 = players_dict[data[0][0]]
        p2 = players_dict[data[1][0]]
        return Match(p1, p2, data[0][1], data[1][1])
