from Controller.Database import save_db, update_player_rank
from Models.Player import Player



def create_player():
    # Récupération des infos du joueur
    user_entries = CreatePlayer().display_menu()

    # Création du joueur
    player = Player(
        user_entries['name'],
        user_entries['first_name'],
        user_entries['sex'],
        user_entries['total_score'],
        user_entries['rank']
    )

    # Sérialisation :
    serialized_player = player.get_serialized_player()
    print(serialized_player)

    # Sauvegarde du joueur dans la base de données
    save_db("players", serialized_player)

    return player


def update_rankings(player, rank, score=True):
    # Mise à jour du score total du joueur si nécessaire
    if score:
        player.total_score += player.tournament_score

    # Mise à jour du rang du joueur
    player.rank = rank

    # Sérialisation du joueur avec la mise à jour du tournoi (si applicable)
    serialized_player = player.get_serialized_player(save_turnament_score=True)

    # Affichage du joueur sérialisé pour vérification
    print(serialized_player['name'])

    # Mise à jour du rang du joueur dans la base de données
    update_player_rank("players", serialized_player)

    # Affichage du statut du joueur après la mise à jour
    print(f"Update du rang de {player.first_name} {player.name} :\n"
          f"Score total: {player.total_score}\nRang: {player.rank}")
