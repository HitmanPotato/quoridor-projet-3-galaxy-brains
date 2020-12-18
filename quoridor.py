'''module docstring'''

import networkx as nx
#import matplotlib.pyplot as mpl


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    '''Crée le graphe des déplacements admissibles pour les joueurs.'''
    graphe = nx.DiGraph()
    # ajouter les arcs de tous les déplacements possibles pour cette tuile
    for col in range(1, 10):
        for row in range(1, 10):
            if col > 1:
                graphe.add_edge((col, row), (col-1, row))
            if col < 9:
                graphe.add_edge((col, row), (col+1, row))
            if row > 1:
                graphe.add_edge((col, row), (col, row-1))
            if row < 9:
                graphe.add_edge((col, row), (col, row+1))
    # retirer tous les arcs qui croisent les murs horizontaux
    for col, row in murs_horizontaux:
        graphe.remove_edge((col, row-1), (col, row))
        graphe.remove_edge((col, row), (col, row-1))
        graphe.remove_edge((col+1, row-1), (col+1, row))
        graphe.remove_edge((col+1, row), (col+1, row-1))
    # retirer tous les arcs qui croisent les murs verticaux
    for col, row in murs_verticaux:
        graphe.remove_edge((col-1, row), (col, row))
        graphe.remove_edge((col, row), (col-1, row))
        graphe.remove_edge((col-1, row+1), (col, row+1))
        graphe.remove_edge((col, row+1), (col-1, row+1))
    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j_1, j_2 = tuple(joueurs[0]), tuple(joueurs[1])
    # traiter le cas des joueurs adjacents
    if j_2 in graphe.successors(j_1) or j_1 in graphe.successors(j_2):
        # retirer les liens entre les joueurs
        graphe.remove_edge(j_1, j_2)
        graphe.remove_edge(j_2, j_1)
        def ajouter_lien_sauteur(noeud, voisin):
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]
            if saut in graphe.successors(voisin):
                graphe.add_edge(noeud, saut)
            else:
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)
        ajouter_lien_sauteur(j_1, j_2)
        ajouter_lien_sauteur(j_2, j_1)
    for col in range(1, 10):
        graphe.add_edge((col, 9), 'B1')
        graphe.add_edge((col, 1), 'B2')
    return graphe


class QuoridorError(Exception):
    '''Exception raised when a wrong move is played'''
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        if self.message:
            return f'QuoridorError: {self.message}'
        return 'QuoridorError'


class Quoridor:
    '''Classe pour encapsuler le jeu Quoridor'''
    def __init__(self, joueurs, murs=None):
        '''Constructeur de la classe Quoridor'''
        # -Exception- Arg. 'joueurs' n'est pas iterable
        if '__iter__' not in dir(joueurs):
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable.")
        # -Exception- Number of players must be 2.
        if len(joueurs) != 2:
            raise QuoridorError("L'itérable de joueurs en contient un nombre différent de deux.")
        # -Instance- Arg. 'joueurs' is a string
        if isinstance(joueurs[0], str):
            self.etat = {'joueurs': [{'nom': joueurs[0], 'murs': 10, 'pos': (5, 1)},
                                    {'nom': joueurs[1], 'murs': 10, 'pos': (5, 9)}],
                        'murs': {'horizontaux': [], 'verticaux': []}}
        # -Exception- Numbre of walls not within 0-10
        elif joueurs[0]['murs'] not in range(0, 11) or joueurs[1]['murs'] not in range(0, 11):
            raise QuoridorError('''Le nombre de murs qu'un joueur peut placer est plus grand que 10
        , ou négatif.''')
        # -Instance- Arg. 'joueurs' is a dictionnary
        else:
            self.etat = {'joueurs': joueurs,
                        'murs': {'horizontaux': [], 'verticaux': []}}
        # Converts positions in tuples
        self.etat['joueurs'][0]['pos'] = tuple(self.etat['joueurs'][0]['pos'])
        self.etat['joueurs'][1]['pos'] = tuple(self.etat['joueurs'][1]['pos'])
        # Check if optional 'murs' is present
        if murs is not None:
            if not isinstance(murs, dict):
                raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
            self.etat['murs']['horizontaux'] = murs['horizontaux']
            self.etat['murs']['verticaux'] = murs['verticaux']
        # -Exception- | Number of walls is > than 20.
        if (self.etat['joueurs'][0]['murs'] +
        self.etat['joueurs'][1]['murs'] +
        len(self.etat['murs']['verticaux']) +
        len(self.etat['murs']['horizontaux'])) != 20:
            raise QuoridorError("""Le total des murs placés e
        t plaçables n'est pas égal à 20.""")
        # -Exception- Wall not in grid or on top of wall
        # Error - If dict. entry isn't empty | Wall outside of bounds, horizontal
        if self.etat["murs"]["horizontaux"]:
            for pos in self.etat["murs"]["horizontaux"]:
                if not (1 <= pos[0] <= 8 and 2 <= pos[1] <= 9):
                    raise QuoridorError("La position d'un mur est invalide.")
        # Error - If dict. entry isn't empty | Wall outside of bounds, vertical
        if self.etat["murs"]["verticaux"]:
            for pos in self.etat["murs"]["verticaux"]:
                if not (2 <= pos[0] <=9 and 1 <= pos[1] <= 8):
                    raise QuoridorError("La position d'un mur est invalide.")
        for pos in self.etat["murs"]["horizontaux"]:
            # Error - Same wall position repeated, horizontal
            if (self.etat['murs']['horizontaux'].count(tuple(pos)) +
                self.etat['murs']['horizontaux'].count(list(pos))) != 1:
                raise QuoridorError("La position d'un mur est invalide.")
            # Error - Two walls in a row, horizontal
            if (((pos[0] + 1, pos[1]) in self.etat['murs']['horizontaux']) or
                ([pos[0] + 1, pos[1]] in self.etat['murs']['horizontaux'])):
                raise QuoridorError("La position d'un mur est invalide.")
            # Error - Crossed walls
            if (((pos[0] + 1, pos[1] - 1) in self.etat['murs']['verticaux']) or
                ([pos[0] + 1, pos[1] - 1] in self.etat['murs']['verticaux'])):
                raise QuoridorError("La position d'un mur est invalide.")
        for pos in self.etat["murs"]["verticaux"]:
            # Error - Same wall position repeated, vertical
            if (self.etat['murs']['verticaux'].count(tuple(pos)) +
                self.etat['murs']['verticaux'].count(list(pos))) != 1:
                raise QuoridorError("La position d'un mur est invalide.")
            # Error - Two walls in a row, vertical
            if (((pos[0], pos[1] + 1) in self.etat['murs']['verticaux']) or
                ([pos[0], pos[1] + 1] in self.etat['murs']['verticaux'])):
                raise QuoridorError("La position d'un mur est invalide.")
        # Initialize graphe of possible paths
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])
        # -Exception- | The path from a player to the objective is blocked.
        if (not nx.has_path(graphe, self.etat['joueurs'][0]['pos'], 'B1')
            or not nx.has_path(graphe, self.etat['joueurs'][1]['pos'], 'B2')):
            raise QuoridorError("La position d'un mur est invalide.")

    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.
        Returns:
            str: La chaîne de caractères de la représentation.
        """
    # 1) Affichage de la légende
        j1 = [self.etat['joueurs'][0]['nom'], self.etat['joueurs'][0]['murs']]
        j2 = [self.etat['joueurs'][1]['nom'], self.etat['joueurs'][1]['murs']]
        if len(j1[0]) >= len(j2[0]):
            lenx = len(j1[0]) + 1
        else:
            lenx = len(j2[0]) + 1
        legende = f'Légende:\n   1={j1[0] + ",":<{lenx}} murs={j1[1] * "|"}\n'
        legende += f'   2={j2[0] + ",":<{lenx}} murs={j2[1] * "|"}\n'
        legende += f'   {"-" * 35}'
    # 2) Affichage du damier initial vide:
        forme1 = ''
        for i in range(19, 2, -1):
            if i % 2 == 0:
                forme1 += f'  |{" " * 35}|\n'
            else:
                forme1 += f'{i // 2} |{" .  " * 8} . |\n'
        forme1 = list(forme1)
        forme2 = ''
        for j in range(2, 19):
            if j==2:
                forme2 += f'--|{"-" * 35}\n  | '
            if j % 2 == 0:
                forme2 += f'{j // 2}   '
    # 3) Affichage des joueurs:
        forme1[-80 * self.etat['joueurs'][0]['pos'][1] +
        4 * self.etat['joueurs'][0]['pos'][0] + 40] = '1'
        forme1[-80 * self.etat['joueurs'][1]['pos'][1] +
        4 * self.etat['joueurs'][1]['pos'][0] + 40] = '2'
    # 4) Affichage des murs:
        for mur in self.etat['murs']['verticaux']:
            for i in range(3):
                forme1[-80 * mur[1] + 4 * mur[0] + 38 - 40 * i] = '|'
        for mur in self.etat['murs']['horizontaux']:
            for i in range(7):
                forme1[-80 * mur[1] + 4 * mur[0] + 79 + i] = '-'
    # 5) Affichage de tout:
        return legende + '\n' + ''.join(forme1) + forme2

    def déplacer_jeton(self, joueur, position):
        '''Pour le joueur spécifié, déplacer son jeton à la position spécifiée.'''
        # -Exception- Arg. joueur != 1 ou 2
        if joueur not in (1, 2):
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')
        # -Exception- Arg. position outside of grid
        if not (1 <= position[0] <= 9 and 1 <= position[1] <= 9):
            raise QuoridorError('La position est invalide (en dehors du damier).')
        # Initialize graphe of possible moves
        graphe = construire_graphe(
            [j['pos'] for j in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])
        # -Exception- | Invalid move
        if position not in list(graphe.successors(self.etat['joueurs'][joueur - 1]['pos'])):
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")
        self.etat['joueurs'][joueur - 1]['pos'] = tuple(position)

    def état_partie(self):
        '''Produire l'état actuel de la partie.(Dict)'''
        return self.etat

    def jouer_coup(self, joueur):
        """Jouer un coup automatique pour un joueur."""
        # -Exceptions-
        if self.partie_terminée():
            raise QuoridorError('La partie est déjà terminée.')

        if joueur == 1:
            player = (1, 'B1')
            adv = (2, 'B2')
        elif joueur == 2:
            player = (2, 'B2')
            adv = (1, 'B1')
        else:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')

        graphe = construire_graphe(
            [j['pos'] for j in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])

        playerpath = nx.shortest_path(graphe, self.etat['joueurs'][player[0] - 1]['pos'], player[1])
        advpath = nx.shortest_path(graphe, self.etat['joueurs'][adv[0] - 1]['pos'], adv[1])
        if len(playerpath) <= len(advpath):
            self.déplacer_jeton(player[0], playerpath[1])
            return ['D', playerpath[1]]
        else:
            try:
                self.placer_mur(1, advpath[1], 'horizontal')
                return ['MH', advpath[1]]
            except Exception:
                try:
                    self.placer_mur(1, advpath[1], 'vertical')
                    return ['MV', advpath[1]]
                except Exception:
                    try:
                        self.placer_mur(1, advpath[1] - 1, 'horizontal')
                        return ['MH', advpath[1] - 1]
                    except Exception:
                        try:
                            self.placer_mur(1, advpath[1] - 1, 'vertical')
                            return ['MV', advpath[1] - 1]
                        except Exception:
                            self.déplacer_jeton(player[0], playerpath[1])
                            return ['D', playerpath[1]]

    def partie_terminée(self):
        """Déterminer si la partie est terminée.
        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.etat['joueurs'][0]['pos'][1] == 9:
            return self.etat['joueurs'][0]['nom']
        if self.etat['joueurs'][1]['pos'][1] == 1:
            return self.etat['joueurs'][1]['nom']
        return False


    def placer_mur(self, joueur, position, orientation):
        """Placer un mur.
        Pour le joueur spécifié, placer un mur à la position spécifiée.
        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """
        # -Exception- | Joueur != 1 or 2
        if joueur not in [1,2]:
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')
        # -Exception- | Joueur walls = 0
        if self.etat['joueurs'][joueur - 1]['murs'] == 0:
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')

        horizontal_walls = self.etat['murs']['horizontaux']
        vertical_walls = self.etat['murs']['verticaux']
        if orientation == 'horizontal':
            # -Exception- | Position outside grid | horizontal
            if not (1 <= position[0] <= 8 and 2 <= position[1] <= 9):
                raise QuoridorError('La position est invalide pour cette orientation.')
            # Error - Same wall position repeated, horizontal
            if (self.etat['murs']['horizontaux'].count(tuple(position)) +
            self.etat['murs']['horizontaux'].count(list(position))) != 0:
                raise QuoridorError('Un mur occupe déjà cette position.')
            # Error - Two walls in a row, horizontal
            if (((position[0] + 1, position[1]) in self.etat['murs']['horizontaux']) or
                ([position[0] + 1, position[1]] in self.etat['murs']['horizontaux']) or
                ((position[0] - 1, position[1]) in self.etat['murs']['horizontaux']) or
                ((position[0] - 1, position[1]) in self.etat['murs']['horizontaux'])):
                raise QuoridorError('Un mur occupe déjà cette position.')
            # Error - Crossed walls
            if (((position[0] + 1, position[1] - 1) in self.etat['murs']['verticaux']) or
                ([position[0] + 1, position[1] - 1] in self.etat['murs']['verticaux'])):
                raise QuoridorError('La position est invalide pour cette orientation.')
            horizontal_walls.append(tuple(position))
            graphe = construire_graphe(
                [j['pos'] for j in self.etat['joueurs']],
                horizontal_walls,
                vertical_walls)
            if not nx.has_path(graphe, self.etat['joueurs'][0]['pos'], 'B1'):
                horizontal_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.etat['joueurs'][0]['pos'], 'B2'):
                horizontal_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.etat['joueurs'][1]['pos'], 'B2'):
                horizontal_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.etat['joueurs'][1]['pos'], 'B1'):
                horizontal_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")

        if orientation == 'vertical':
            # -Exception- | Position outside grid | vertical
            if not (2 <= position[0] <=9 and 1 <= position[1] <= 8):
                raise QuoridorError('La position est invalide pour cette orientation.')
            # Error - Same wall position repeated, horizontal
            if (self.etat['murs']['verticaux'].count(tuple(position)) +
            self.etat['murs']['verticaux'].count(list(position))) != 0:
                raise QuoridorError('Un mur occupe déjà cette position.')
            # Error - Two walls in a row, vertical
            if (((position[0], position[1] + 1) in self.etat['murs']['verticaux']) or
                ((position[0], position[1] + 1) in self.etat['murs']['verticaux']) or
                ((position[0], position[1] - 1) in self.etat['murs']['verticaux']) or
                ([position[0], position[1] - 1] in self.etat['murs']['verticaux'])):
                raise QuoridorError('Un mur occupe déjà cette position.')
            # Error - Crossed walls
            if (((position[0] - 1, position[1] + 1) in self.etat['murs']['horizontaux']) or
                ([position[0] - 1, position[1] + 1] in self.etat['murs']['horizontaux'])):
                raise QuoridorError('La position est invalide pour cette orientation.')
            vertical_walls.append(tuple(position))
            graphe = construire_graphe(
                [j['pos'] for j in self.etat['joueurs']],
                horizontal_walls,
                vertical_walls)
            if not nx.has_path(graphe, self.etat['joueurs'][0]['pos'], 'B1'):
                vertical_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.etat['joueurs'][0]['pos'], 'B2'):
                vertical_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.etat['joueurs'][1]['pos'], 'B2'):
                vertical_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")
            if not nx.has_path(graphe, self.etat['joueurs'][1]['pos'], 'B1'):
                vertical_walls.pop()
                raise QuoridorError("La position d'un mur est invalide.")

        self.etat['joueurs'][joueur - 1]['murs'] -= 1
