'''module docstring'''
import turtle
import argparse
from api import lister_parties, initialiser_partie, jouer_coup
from quoridor import Quoridor
from quoridor import QuoridorError
from quoridorx import QuoridorX


def analyser_commande():
    """Génère un analyseur de ligne de commande."""
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter,
    description='Jeu Quoridor - phase 3')
    parser.add_argument('idul', metavar='idul',
    help='IDUL du joueur')
    parser.add_argument('-a', '--automatique', action = ('store_true'),
    help='Activer le mode automatique.')
    parser.add_argument('-x', '--graphique', action = ('store_true'),
    help='Activer le mode graphique.')
    return parser.parse_args()




if __name__ == "__main__":
    parsed = analyser_commande()
    game_info = initialiser_partie(parsed.idul)

    if parsed.automatique and parsed.graphique:
        # Mode auto graphique
        game = QuoridorX(game_info[1]['joueurs'])
        while not game.partie_terminée():
            pass


    elif parsed.automatique:
        # Mode auto simple
        game = Quoridor(game_info[1]['joueurs'])
        print(game)
        while not game.partie_terminée():
            coup = game.jouer_coup(1)
            print(game)
            etat = jouer_coup(game_info[0], coup[0], tuple(coup[1]))[1]
            game = QuoridorX(etat['joueurs'], murs=etat['murs'])
            print(game)



    elif parsed.graphique:
        # Mode manuel graphique
        game = QuoridorX(game_info[1]['joueurs'])
        while not game.partie_terminée():
            pass


    else:
        # Mode manuel simple
        game = Quoridor(game_info[1]['joueurs'])
        while not game.partie_terminée():
            print(game)
            print('''Type de coup disponible : \n        - D : Déplacement
                \n        - MH: Mur Horizontal\n        - MV: Mur Vertical''')
            type_coup = input("Choisissez votre type de coup (D, MH ou MV) : ")
            col = input('Définissez la colonne de votre coup : ')
            row = input('Définissez la ligne de votre coup : ')
            if type_coup == 'D':
                try:
                    game.déplacer_jeton(1, (int(col), int(row)))
                except QuoridorError as err:
                    print(err)
                    continue
                except StopIteration as stop:
                    print(f'Game Over! The winner is {stop}')
                else:
                    etat = jouer_coup(game_info[0], 'D', (col, row))[1]
                    game = Quoridor(etat['joueurs'], murs=etat['murs'])
            elif type_coup == 'MH':
                try:
                    game.placer_mur(1, (int(col), int(row)), 'horizontal')
                except QuoridorError as err:
                    print(err)
                    continue
                except StopIteration as stop:
                    print(f'Game Over! The winner is {stop}')
                else:
                    etat = jouer_coup(game_info[0], 'MH', (col, row))[1]
                    game = Quoridor(etat['joueurs'], murs=etat['murs'])
            elif type_coup == 'MV':
                try:
                    game.placer_mur(1, (int(col), int(row)), 'vertical')
                except QuoridorError as err:
                    print(err)
                    continue
                except StopIteration as stop:
                    print(f'Game Over! The winner is {stop}')
                else:
                    etat = jouer_coup(game_info[0], 'MV', (col, row))[1]
                    game = Quoridor(etat['joueurs'], murs=etat['murs'])
