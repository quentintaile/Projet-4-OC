from Models.Tournament import Tournament
from Controller.Player import create_player, update_rankings
from Controller.Database import save_db, update_db, load_player, load_tournament


def create_tournament():
    menu = View()
    
    # Récupération des infos du tournoi
    user_entries = CreateTournament().display_menu()

    # Choix chargement joueurs:
    user_input = menu.get_user_entry(
        msg_display="Que faire ?\n0 - Créer des joueurs\n1 - Charger des joueurs\n> ",
        msg_error="Entrez un choix valide.",
        value_type="selection",
        assertions=["0", "1"]
    )

    # Initialisation des joueurs
    players = []

    # Chargement des joueurs
    if user_input == "1":
        user_input = menu.get_user_entry(
            msg_display="Charger combien de joueurs ?\n> ",
            msg_error="Entrez un nombre valide.",
            value_type="numeric"
        )

        serialized_players = LoadPlayer().display_menu(nb_players_to_load=int(user_input))

        for serialized_player in serialized_players:
            player = load_player(serialized_player)
            players.append(player)

    # Création des joueurs
    elif user_input == "0":
        print(f"Création de {user_entries['nb_players']} joueurs.")
        while len(players) < int(user_entries['nb_players']):
            players.append(create_player())

    # Création du tournoi
    tournament = Tournament(
        user_entries['name'],
        user_entries['place'],
        user_entries['date'],
        user_entries['time_control'],
        players,
        user_entries['nb_rounds'],
        user_entries['desc']
    )

    # Sauvegarde du tournoi dans la base de données
    save_db("tournaments", tournament.get_serialized_tournament())

    return tournament


def play_tournament(tournament, new_tournament_loaded=False):
    menu = View()
    print()
    print(f"Début du tournoi {tournament.name}")
    print()

    while True:
        # Si un nouveau tournoi est chargé, calculer les rounds restants à jouer
        if new_tournament_loaded:
            a = 0
            for round_ in tournament.rounds:
                if round_.end_date == "":
                    a += 1
            nb_rounds_to_play = tournament.nb_rounds - a
            new_tournament_loaded = False
        else:
            nb_rounds_to_play = tournament.nb_rounds

        for i in range(nb_rounds_to_play):
            # Création du round
            tournament.create_round(round_number=i + a)

            # Jouer le dernier round créé
            current_round = tournament.rounds[-1]
            print()
            print(f"{current_round.start_date} : Début du {current_round.name}")

            while True:
                print()
                user_input = menu.get_user_entry(
                    msg_display="Que faire ?\n"
                                "0 - Round suivant\n"
                                "1 - Voir les classements\n"
                                "2 - Mettre à jour les classements\n"
                                "3 - Sauvegarder le tournoi\n"
                                "4 - Charger un tournoi\n> ",
                    msg_error="Veuillez faire un choix.",
                    value_type="selection",
                    assertions=["0", "1", "2", "3", "4"]
                )
                print()

                # Round suivant
                if user_input == "0":
                    current_round.mark_as_complete()
                    break

                # Affichage des classements
                elif user_input == "1":
                    print(f"Classement du tournoi {tournament.name}:")
                    for i, player in enumerate(tournament.get_rankings()):
                        print(f"{i + 1} - {player.first_name} {player.name} (Rank: {player.rank}, Score: {player.total_score})")

                # Changement des rangs
                elif user_input == "2":
                    for player in tournament.players:
                        rank = menu.get_user_entry(
                            msg_display=f"Rang de {player.first_name} {player.name}:\n> ",
                            msg_error="Veuillez entrer un nombre entier.",
                            value_type="numeric"
                        )
                        update_rankings(player, rank, score=False)

                # Sauvegarde du tournoi
                elif user_input == "3":
                    rankings = tournament.get_rankings()
                    for i, player in enumerate(rankings):
                        for t_player in tournament.players:
                            if player.name == t_player.name:
                                t_player.rank = str(i + 1)
                    update_db("tournaments", tournament.get_serialized_tournament(save_rounds=True))

                # Charger un tournoi
                elif user_input == "4":
                    serialized_loaded_tournament = LoadTournament().display_menu()
                    tournament = load_tournament(serialized_loaded_tournament)
                    new_tournament_loaded = True
                    break

            if new_tournament_loaded:
                break

        if new_tournament_loaded:
            continue
        else:
            break

    # Une fois le tournoi terminé, on le sauvegarde et met à jour les résultats
    rankings = tournament.get_rankings()
    for i, player in enumerate(rankings):
        for t_player in tournament.players:
            if player.name == t_player.name:
                t_player.total_score += player.tournament_score
                t_player.rank = str(i + 1)
    update_db("tournaments", tournament.get_serialized_tournament(save_rounds=True))
    
    return rankings