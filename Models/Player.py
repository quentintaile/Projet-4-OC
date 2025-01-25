class Player:
    # Le constructeur de la classe Player initialise les attributs du joueur.
    def __init__(self, name, first_name, sex, total_score, rank=0):
        self.name = name  # Nom du joueur
        self.first_name = first_name  # Prénom du joueur
        self.sex = sex  # Sexe du joueur
        self.total_score = total_score  # Score total du joueur (souvent utilisé pour le classement)
        self.tournament_score = 0  # Score du tournoi (initialisé à 0)
        self.rank = rank  # Rang du joueur (par défaut, il est 0)
        self.played_with = []  # Liste des joueurs contre lesquels le joueur a joué

    # La méthode __str__ permet de définir la manière dont un objet Player est affiché en tant que chaîne de caractères.
    def __str__(self):
        return f"{self.first_name} {self.name} [{self.tournament_score} pts]"  # Format du nom et du score du joueur

    # La méthode get_serialized_player convertit les informations du joueur en un dictionnaire pour la sauvegarde.
    def get_serialized_player(self, save_turnament_score=False):
        serialized_player = {
            "name": self.name,  # Nom du joueur
            "first_name": self.first_name,  # Prénom du joueur
            "sex": self.sex,  # Sexe du joueur
            "total_score": self.total_score,  # Score total du joueur
            "rank": self.rank,  # Rang du joueur
        }

        # Si l'argument save_turnament_score est vrai, ajoute le score du tournoi au dictionnaire.
        if save_turnament_score:
            serialized_player["tournament_score"] = self.tournament_score

        return serialized_player  # Retourne le dictionnaire contenant les informations du joueur
