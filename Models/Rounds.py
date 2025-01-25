from Models.Match import Match

class Round:
    # Le constructeur initialise les informations relatives au round.
    def __init__(self, name, players_pairs, load_match: bool = False):
        self.name = name  # Nom du round
        self.players_pairs = players_pairs  # Paires de joueurs pour ce round

        # Si on charge des matchs existants (load_match=True), on initialise une liste vide pour les matchs.
        # Sinon, on crée les matchs normalement en appelant la méthode create_matchs.
        if load_match:
            self.matchs = []
        else:
            self.matchs = self.create_matchs()  # Crée les matchs pour ce round.

        self.start_date = get_timestamp()  # Enregistre le timestamp du début du round.
        self.end_date = ""  # La date de fin est vide tant que le round n'est pas terminé.

    # La méthode __str__ permet de définir la chaîne de caractères qui sera utilisée pour afficher l'objet Round.
    def __str__(self):
        return self.name  # Affiche le nom du round.

    # La méthode create_matchs crée les matchs pour ce round en fonction des paires de joueurs.
    def create_matchs(self):
        matchs = []  # Liste qui contiendra tous les matchs créés.
        for i, pair in enumerate(self.players_pairs):  # On parcourt chaque paire de joueurs.
            matchs.append(Match(name=f"Match {i}", players_pair=pair))  # On crée un match pour chaque paire et on l'ajoute à la liste.
        return matchs  # On retourne la liste de matchs.

    # La méthode mark_as_complete marque le round comme terminé en ajoutant la date de fin.
    # Elle permet aussi de saisir les résultats des matchs.
    def mark_as_complete(self):
        self.end_date = get_timestamp()  # On enregistre la date de fin du round.
        print(f"{self.end_date} : {self.name} terminé.")  # Affiche la date et le nom du round terminé.
        print("Rentrer les résultats des matchs:")  # Demande à l'utilisateur de rentrer les résultats.
        for match in self.matchs:  # Pour chaque match dans ce round.
            match.play_match()  # On appelle la méthode pour jouer et enregistrer les résultats du match.

    # La méthode get_serialized_round permet de convertir le round en un dictionnaire pour la sauvegarde.
    def get_serialized_round(self):
        ser_players_pairs = []  # Liste pour stocker les paires de joueurs sérialisées.

        # On sérialise chaque paire de joueurs (chaque joueur dans la paire).
        for pair in self.players_pairs:
            ser_players_pairs.append(
                (
                    pair[0].get_serialized_player(save_turnament_score=True),  # Sérialisation du premier joueur de la paire
                    pair[1].get_serialized_player(save_turnament_score=True)   # Sérialisation du deuxième joueur de la paire
                )
            )

        # Retourne un dictionnaire contenant les informations du round, y compris les matchs et les paires de joueurs.
        return {
            "name": self.name,  # Nom du round
            "players_pairs": ser_players_pairs,  # Paires de joueurs sérialisées
            "matchs": [match.get_serialized_match() for match in self.matchs],  # Sérialisation des matchs
            "start_date": self.start_date,  # Date de début
            "end_date": self.end_date,  # Date de fin
        }
