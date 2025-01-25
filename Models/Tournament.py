# Importation de la classe Round depuis le module models.round
from Models.Rounds import Round

class Tournament:
    # Initialisation du tournoi avec son nom, lieu, date, contrôle du temps, joueurs, etc.
    def __init__(self, name, place, date, time_control, players, nb_rounds=4, desc=""):
        self.name = name  # Nom du tournoi
        self.place = place  # Lieu du tournoi
        self.date = date  # Date du tournoi
        self.time_control = time_control  # Type de contrôle du temps
        self.players = players  # Liste des joueurs du tournoi
        self.nb_rounds = nb_rounds  # Nombre de rounds (par défaut 4)
        self.rounds = []  # Liste vide pour stocker les rounds créés
        self.desc = desc  # Description du tournoi (par défaut vide)

    # Méthode pour afficher les informations de base du tournoi
    def __str__(self):
        return f"Tournoi: {self.name}"

    # Méthode pour créer un round du tournoi
    def create_round(self, round_number):
        players_pairs = self.create_players_pairs(current_round=round_number)  # Créer les paires de joueurs pour ce round
        round = Round("Round " + str(round_number + 1), players_pairs)  # Création d'un objet Round avec ces paires
        self.rounds.append(round)  # Ajout du round à la liste des rounds du tournoi

    # Méthode pour créer les paires de joueurs pour un round donné
    def create_players_pairs(self, current_round):
        # Premier round, les joueurs sont triés par rang (du plus haut au plus bas)
        if current_round == 0:
            sorted_players = sorted(self.players, key=lambda x: x.rank, reverse=True)
        else:
            sorted_players = []  # Liste des joueurs triés
            score_sorted_players = sorted(self.players, key=lambda x: x.total_score, reverse=True)  # Tri des joueurs par score total

            # Si deux joueurs ont le même score, on les trie par leur rang
            for i, player in enumerate(score_sorted_players):
                try:
                    sorted_players.append(player)
                except player.total_score == score_sorted_players[i + 1].total_score:
                    if player.rank > score_sorted_players[i + 1].rank:  # Si le rang de player est plus élevé que celui du joueur suivant
                        hi_player = player
                        lo_player = score_sorted_players[i + 1]
                    else:
                        hi_player = score_sorted_players[i + 1]
                        lo_player = player
                    sorted_players.append(hi_player)  # Ajouter le joueur à plus haut rang
                    sorted_players.append(lo_player)  # Ajouter l'autre joueur
                except IndexError:  # Si on atteint la fin de la liste
                    sorted_players.append(player)

        # Diviser les joueurs en deux moitiés égales
        sup_part = sorted_players[len(sorted_players)//2:]  # Partie supérieure des joueurs
        inf_part = sorted_players[:len(sorted_players)//2]  # Partie inférieure des joueurs

        players_pairs = []  # Liste des paires de joueurs

        # Création des paires de joueurs
        for i, player in enumerate(sup_part):
            a = 0
            while True:
                try:
                    player2 = inf_part[i + a]  # Essayer de trouver le joueur dans la partie inférieure

                except IndexError:  # Si on dépasse la fin de la liste, on assigne le dernier joueur
                    player2 = inf_part[i]
                    players_pairs.append((player, player2))  # Ajouter la paire à la liste

                    # Ajouter les joueurs à leurs listes respectives de 'played_with' pour ne pas les appairer à nouveau
                    player.played_with.append(player2)
                    player2.played_with.append(player)
                    break

                # Si les deux joueurs ont déjà joué ensemble, on passe à la suivante
                if player in player2.played_with:
                    a += 1
                    continue

                # Si les joueurs n'ont pas joué ensemble, on les ajoute comme paire
                else:
                    players_pairs.append((player, player2))
                    player.played_with.append(player2)  # Ajouter le joueur2 à la liste 'played_with' de player
                    player2.played_with.append(player)  # Ajouter player à la liste 'played_with' de player2
                    break

        return players_pairs  # Retourner la liste des paires de joueurs

    # Méthode pour obtenir le classement des joueurs dans le tournoi
    def get_rankings(self, by_score=True):
        # Par défaut, on trie les joueurs par leur score total dans le tournoi
        if by_score:
            sorted_players = sorted(self.players, key=lambda x: x.tournament_score, reverse=True)
        else:
            sorted_players = sorted(self.players, key=lambda x: x.rank, reverse=True)

        return sorted_players  # Retourner la liste des joueurs triés

    # Méthode pour sérialiser les informations du tournoi
    def get_serialized_tournament(self, save_rounds=False):
        # Sérialisation de toutes les informations relatives au tournoi
        serialized_tournament = {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "time_control": self.time_control,
            "players": [player.get_serialized_player(save_turnament_score=True) for player in self.players],
            "nb_rounds": self.nb_rounds,
            "rounds": [round.get_serialized_round() for round in self.rounds],
            "desc": self.desc
        }

        # Si on doit inclure les rounds dans la sérialisation
        if save_rounds:
            serialized_tournament["rounds"] = [round.get_serialized_round() for round in self.rounds]

        return serialized_tournament  # Retourner le tournoi sérialisé
