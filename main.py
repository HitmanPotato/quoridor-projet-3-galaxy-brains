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
        try:
            while not game.partie_terminée():
                coup = game.jouer_coup(1)
                game.afficher()
                etat = jouer_coup(game_info[0], coup[0], tuple(coup[1]))[1]
                # Type coup robot | Deplacement
                if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                    newpos = tuple(etat['joueurs'][1]['pos'])
                    game.déplacer_jeton(2, newpos)
                # Type coup robot | Mur horizontal
                elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                    wallpos = tuple(etat['murs']['horizontaux'][-1])
                    game.placer_mur(2, wallpos, 'horizontal')
                # Type coup robot | Mur vertical
                elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                    wallpos = tuple(etat['murs']['verticaux'][-1])
                    game.placer_mur(2, wallpos, 'vertical')
                game.afficher()
        except StopIteration as stop:
            turtle.textinput('Game Over!', f'The winner is {stop}!')



    elif parsed.automatique:
        # Mode auto simple [complete]
        game = Quoridor(game_info[1]['joueurs'])
        print(game)
        try:
            while not game.partie_terminée():
                coup = game.jouer_coup(1)
                print(game)
                etat = jouer_coup(game_info[0], coup[0], tuple(coup[1]))[1]
                # Type coup robot | Deplacement
                if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                    newpos = tuple(etat['joueurs'][1]['pos'])
                    game.déplacer_jeton(2, newpos)
                # Type coup robot | Mur horizontal
                elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                    wallpos = tuple(etat['murs']['horizontaux'][-1])
                    game.placer_mur(2, wallpos, 'horizontal')
                # Type coup robot | Mur vertical
                elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                    wallpos = tuple(etat['murs']['verticaux'][-1])
                    game.placer_mur(2, wallpos, 'vertical')
                print(game)
        except StopIteration as stop:
            print(f'Game Over! The winner is {stop}')























    elif parsed.graphique:
        # Mode manuel graphique
        game = QuoridorX(game_info[1]['joueurs'])
        while not game.partie_terminée():
            game.afficher()
            game.afficher()
            type_coup = turtle.textinput("Choisissez votre type de coup", 'D, MH, ou MV')
            col = int(turtle.numinput('Définissez la colonne de votre coup', 'Numéro de colonne:', minval=1, maxval=9))
            row = int(turtle.numinput('Définissez la ligne de votre coup', 'Numéro de ligne:', minval=1, maxval=9))
            # Type coup joueur | Deplacement
            if type_coup.upper() == 'D':
                try:
                    game.déplacer_jeton(1, (int(col), int(row)))
                except QuoridorError as err:
                    turtle.textinput('Error', err)
                    continue
                except StopIteration as stop:
                    turtle.textinput('Game Over!', f'The winner is {stop}!')
                else:
                    game.afficher()
                    game.afficher()
                    etat = jouer_coup(game_info[0], 'D', (int(col), int(row)))[1]
                    # Type coup robot | Deplacement
                    if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                        newpos = tuple(etat['joueurs'][1]['pos'])
                        game.déplacer_jeton(2, newpos)
                        game.afficher()
                    # Type coup robot | Mur horizontal
                    elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                        hwallpos = tuple(etat['murs']['horizontaux'][-1])
                        game.placer_mur(2, hwallpos, 'horizontal')
                        game.afficher()
                    # Type coup robot | Mur vertical
                    elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                        vwallpos = tuple(etat['murs']['verticaux'][-1])
                        game.placer_mur(2, vwallpos, 'vertical')
                        game.afficher()
            #Type coup joueur | Mur horizontal
            elif type_coup.upper() == 'MH':
                try:
                    game.placer_mur(1, (int(col), int(row)), 'horizontal')
                except QuoridorError as err:
                    turtle.textinput('Error', err)
                    continue
                except StopIteration as stop:
                    turtle.textinput('Game Over!', f'The winner is {stop}!')
                else:
                    game.afficher()
                    etat = jouer_coup(game_info[0], 'MH', (col, row))[1]
                    # Type coup robot | Deplacement
                    if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                        newpos = tuple(etat['joueurs'][1]['pos'])
                        game.déplacer_jeton(2, newpos)
                        game.afficher()
                    # Type coup robot | Mur horizontal
                    elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                        hwallpos = tuple(etat['murs']['horizontaux'][-1])
                        game.placer_mur(2, hwallpos, 'horizontal')
                        game.afficher()
                    # Type coup robot | Mur vertical
                    elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                        vwallpos = tuple(etat['murs']['verticaux'][-1])
                        game.placer_mur(2, vwallpos, 'vertical')
                        game.afficher()
            # Type coup joueur | Mur vertical
            elif type_coup.upper() == 'MV':
                try:
                    game.placer_mur(1, (int(col), int(row)), 'vertical')
                except QuoridorError as err:
                    turtle.textinput('Error', err)
                    continue
                except StopIteration as stop:
                    turtle.textinput('Game Over!', f'The winner is {stop}!')
                else:
                    game.afficher()
                    etat = jouer_coup(game_info[0], 'MV', (col, row))[1]
                    # Type coup robot | Deplacement
                    if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                        newpos = tuple(etat['joueurs'][1]['pos'])
                        game.déplacer_jeton(2, newpos)
                        game.afficher()
                    # Type coup robot | Mur horizontal
                    elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                        hwallpos = tuple(etat['murs']['horizontaux'][-1])
                        game.placer_mur(2, hwallpos, 'horizontal')
                        game.afficher()
                    # Type coup robot | Mur vertical
                    elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                        vwallpos = tuple(etat['murs']['verticaux'][-1])
                        game.placer_mur(2, vwallpos, 'vertical')
                        game.afficher()
            else:
                turtle.textinput('Undefined',  'Incorrect input | Try again')
                continue























    else:
        # Mode manuel simple [complete]
        game = Quoridor(game_info[1]['joueurs'])
        while not game.partie_terminée():
            print(game)
            print('''Type de coup disponible : \n        - D : Déplacement
                \n        - MH: Mur Horizontal\n        - MV: Mur Vertical''')
            type_coup = input("Choisissez votre type de coup (D, MH ou MV) : ")
            col = input('Définissez la colonne de votre coup : ')
            row = input('Définissez la ligne de votre coup : ')


            # Type coup joueur | Deplacement
            if type_coup.upper() == 'D':
                try:
                    game.déplacer_jeton(1, (int(col), int(row)))
                except QuoridorError as err:
                    print(err)
                    continue
                except StopIteration as stop:
                    print(f'Game Over! The winner is {stop}')
                else:
                    print(game)
                    etat = jouer_coup(game_info[0], 'D', (col, row))[1]
                    print(etat)
                    # Type coup robot | Deplacement
                    if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                        print(game.état_partie()['joueurs'][1]['pos'])
                        print(etat['joueurs'][1]['pos'])
                        newpos = tuple(etat['joueurs'][1]['pos'])
                        print(f'Robot moved to new position: {newpos}')
                        game.déplacer_jeton(2, newpos)
                        print(game.état_partie())
                    # Type coup robot | Mur horizontal
                    elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                        wallpos = tuple(etat['murs']['horizontaux'][-1])
                        print(f'Robot placed horizontal wall at: {wallpos}')
                        game.placer_mur(2, wallpos, 'horizontal')
                    # Type coup robot | Mur vertical
                    elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                        wallpos = tuple(etat['murs']['verticaux'][-1])
                        print(f'Robot placed horizontal wall at: {wallpos}')
                        game.placer_mur(2, wallpos, 'vertical')
            #Type coup joueur | Mur horizontal
            elif type_coup.upper() == 'MH':
                try:
                    game.placer_mur(1, (int(col), int(row)), 'horizontal')
                except QuoridorError as err:
                    print(err)
                    continue
                except StopIteration as stop:
                    print(f'Game Over! The winner is {stop}')
                else:
                    print(game)
                    etat = jouer_coup(game_info[0], 'MH', (col, row))[1]
                    print(etat)
                    # Type coup robot | Deplacement
                    if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                        newpos = tuple(etat['joueurs'][1]['pos'])
                        print(f'Robot moved to new position: {newpos}')
                        game.déplacer_jeton(2, newpos)
                        print(game.état_partie())
                    # Type coup robot | Mur horizontal
                    elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                        wallpos = tuple(etat['murs']['horizontaux'][-1])
                        print(f'Robot placed horizontal wall at: {wallpos}')
                        game.placer_mur(2, wallpos, 'horizontal')
                    # Type coup robot | Mur vertical
                    elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                        wallpos = tuple(etat['murs']['verticaux'][-1])
                        print(f'Robot placed horizontal wall at: {wallpos}')
                        game.placer_mur(2, wallpos, 'vertical')
            # Type coup joueur | Mur vertical
            elif type_coup.upper() == 'MV':
                try:
                    game.placer_mur(1, (int(col), int(row)), 'vertical')
                except QuoridorError as err:
                    print(err)
                    continue
                except StopIteration as stop:
                    print(f'Game Over! The winner is {stop}')
                else:
                    print(game)
                    etat = jouer_coup(game_info[0], 'MV', (col, row))[1]
                    print(etat)
                    # Type coup robot | Deplacement
                    if game.état_partie()['joueurs'][1]['pos'] != tuple(etat['joueurs'][1]['pos']):
                        newpos = tuple(etat['joueurs'][1]['pos'])
                        print(f'Robot moved to new position: {newpos}')
                        game.déplacer_jeton(2, newpos)
                    # Type coup robot | Mur horizontal
                    elif  len(game.état_partie()['murs']['horizontaux']) != len(etat['murs']['horizontaux']):
                        wallpos = tuple(etat['murs']['horizontaux'][-1])
                        print(f'Robot placed horizontal wall at: {wallpos}')
                        game.placer_mur(2, wallpos, 'horizontal')
                    # Type coup robot | Mur vertical
                    elif  len(game.état_partie()['murs']['verticaux']) != len(etat['murs']['verticaux']):
                        wallpos = tuple(etat['murs']['verticaux'][-1])
                        print(f'Robot placed horizontal wall at: {wallpos}')
                        game.placer_mur(2, wallpos, 'vertical')
            else:
                print('Invalid command')
                continue
