from views.view import View


class Match:
    def __init__(self, name, players_pair):
        # Initialise un match avec deux joueurs.
        # name : Le nom ou identifiant du match.
        # players_pair : Une liste contenant deux joueurs.
        self.player1 = players_pair[0]  # Joueur 1.
        self.score_player1 = 0  # Score initial du joueur 1.
        self.player2 = players_pair[1]  # Joueur 2.
        self.score_player2 = 0  # Score initial du joueur 2.
        self.winner = ""  # Gagnant du match (initialement vide).
        self.name = name  # Nom ou identifiant du match.

    def __repr__(self):
        # Renvoie une représentation lisible du match.
        # Exemple : ([player1, score_player1], [player2, score_player2])
        return ([self.player1, self.score_player1],
                [self.player2, self.score_player2])

    def play_match(self):
        # Joue le match en :
        # 1. Enregistrant le gagnant ou une égalité via l'interaction utilisateur.
        # 2. Met à jour les scores des joueurs.

        # Étape 1 : Interaction utilisateur pour enregistrer le résultat.
        print()  # Ligne vide pour la mise en page.
        winner = View().get_user_entry(
            msg_display=f"{self.player1.first_name} VS {self.player2.first_name}\n"
                        f"Gagnant ?\n"
                        f"0 - {self.player1.first_name}\n"
                        f"1 - {self.player2.first_name}\n"
                        f"2 - Égalité\n> ",
            msg_error="Veuillez entrer 0, 1 ou 2.",  # Message en cas d'entrée incorrecte.
            value_type="selection",  # Type de valeur attendue (choix parmi plusieurs options).
            assertions=["0", "1", "2"]  # Valeurs valides.
        )

        # Étape 2 : Mise à jour des scores et attribution du gagnant.
        if winner == "0":  # Joueur 1 est le gagnant.
            self.winner = self.player1.first_name
            self.score_player1 += 1  # Joueur 1 reçoit 1 point.
        elif winner == "1":  # Joueur 2 est le gagnant.
            self.winner = self.player2.first_name
            self.score_player2 += 1  # Joueur 2 reçoit 1 point.
        elif winner == "2":  # Match nul.
            self.winner = "Égalité"
            self.score_player1 += 0.5  # Les deux joueurs reçoivent 0,5 point.
            self.score_player2 += 0.5

        # Mise à jour des scores totaux des joueurs dans le tournoi.
        self.player1.tournament_score += self.score_player1
        self.player2.tournament_score += self.score_player2

    def get_serialized_match(self):
        # Sérialise les données du match pour une sauvegarde ou un export.
        return {
            "player1": self.player1.get_serialized_player(save_turnament_score=True),  # Données du joueur 1.
            "score_player1": self.score_player1,  # Score du joueur 1.
            "player2": self.player2.get_serialized_player(save_turnament_score=True),  # Données du joueur 2.
            "score_player2": self.score_player2,  # Score du joueur 2.
            "winner": self.winner,  # Gagnant du match.
            "name": self.name  # Nom du match.
        }
