class View:
    def get_player_info(self):
        last_name = input("Nom de famille: ")
        first_name = input("Prénom: ")
        birth_date = input("Date de naissance (YYYY-MM-DD): ")
        chess_id = input("Identifiant national d'échecs (AB12345): ")
        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "chess_id": chess_id
        }

    def get_tournament_info(self):
        name = input("Nom du tournoi: ")
        place = input("Lieu: ")
        start_date = input("Date de début (YYYY-MM-DD): ")
        end_date = input("Date de fin (YYYY-MM-DD): ")
        description = input("Description: ")
        return {
            "name": name,
            "place": place,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        }

    def display_players(self, players):
        for player in players:
            print(f"{player.last_name} {player.first_name} ({player.chess_id})")

    def display_tournaments(self, tournaments):
        for tournament in tournaments:
            print(f"{tournament.name} à {tournament.place} du {tournament.start_date} au {tournament.end_date}")

    def choose_tournament(self, tournaments):
        if not tournaments:
            print("Aucun tournoi disponible.")
            return None
        for idx, t in enumerate(tournaments):
            print(f"{idx + 1}. {t.name}")
        choice = int(input("Choisir un tournoi: ")) - 1
        return tournaments[choice]

    def display_round(self, round_):
        print(f"--- {round_.name} ---")
        for idx, match in enumerate(round_.matches):
            print(f"{idx + 1}: {match.player1.first_name} {match.player1.last_name} VS "
                  f"{match.player2.first_name} {match.player2.last_name}")

    def get_match_result(self, match):
        score1 = float(input(f"Résultat pour {match.player1.first_name} {match.player1.last_name}: "))
        score2 = float(input(f"Résultat pour {match.player2.first_name} {match.player2.last_name}: "))
        return score1, score2

    def show_message(self, message):
        print(message)
