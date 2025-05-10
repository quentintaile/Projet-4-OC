from controller.tournament_controller import TournamentController
from views.view import View


def main():
    view = View()
    controller = TournamentController(view)

    while True:
        print("\n1. Ajouter un joueur")
        print("2. Créer un tournoi")
        print("3. Lister les joueurs")
        print("4. Lister les tournois")
        print("5. Démarrer un tournoi")
        print("6. Quitter")

        choice = input("Choix: ")
        if choice == "1":
            controller.add_player()
        elif choice == "2":
            controller.create_tournament()
        elif choice == "3":
            controller.list_players()
        elif choice == "4":
            controller.list_tournaments()
        elif choice == "5":
            controller.start_tournament()
        elif choice == "6":
            break


if __name__ == "__main__":
    main()
