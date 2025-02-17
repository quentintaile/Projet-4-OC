from Controller.Database import load_db


class CreatePlayer(View):

    def display_menu(self):
        """Affiche le menu de création d'un joueur et récupère ses informations."""

        name = input("Nom du joueur:\n> ")

        first_name = input("Prénom du joueur:\n> ")

        dob = self.get_user_entry(
            msg_display="Date de naissance (format DD-MM-YYYY):\n> ",
            msg_error="Veuillez entrer une date au format valide: DD-MM-YYYY",
            value_type="date"
        )

        sex = self.get_user_entry(
            msg_display="Sexe (H ou F):\n> ",
            msg_error="Veuillez entrer H ou F",
            value_type="selection",
            assertions=["H", "h", "F", "f"]
        ).upper()

        rank = self.get_user_entry(
            msg_display="Rang:\n> ",
            msg_error="Veuillez entrer une valeur numérique valide.",
            value_type="numeric"
        )

        print(f"Joueur {first_name} {name} créé avec succès.")

        return {
            "name": name,
            "first_name": first_name,
            "dob": dob,
            "sex": sex,
            "total_score": 0,  # Initialiser à 0, il pourra être mis à jour plus tard.
            "rank": int(rank)  # Assurez-vous que le rang est un entier.
        }


class LoadPlayer(View):

    def display_menu(self, nb_players_to_load):
        """Affiche le menu pour charger des joueurs à partir de la base de données."""

        all_players = load_db("players")
        serialized_loaded_players = []

        # Tant qu'il reste des joueurs à charger
        for i in range(nb_players_to_load):
            print(f"Plus que {nb_players_to_load - i} joueurs à charger.")
            display_msg = "Choisir un joueur:\n"

            assertions = []
            for index, player in enumerate(all_players):
                display_msg += f"{index + 1} - {player['first_name']} {player['name']}\n"
                assertions.append(str(index + 1))

            # Demander à l'utilisateur de choisir un joueur
            user_input = int(self.get_user_entry(
                msg_display=display_msg,
                msg_error="Veuillez entrer un nombre entier valide.",
                value_type="selection",
                assertions=assertions
            ))

            # Vérification que le joueur n'est pas déjà chargé
            selected_player = all_players[user_input - 1]

            if selected_player not in serialized_loaded_players:
                serialized_loaded_players.append(selected_player)
            else:
                print("Joueur déjà chargé. Merci de choisir un autre joueur.")
                nb_players_to_load += 1  # Ne pas décrémenter nb_players_to_load car l'utilisateur a fait une erreur.

        return serialized_loaded_players
