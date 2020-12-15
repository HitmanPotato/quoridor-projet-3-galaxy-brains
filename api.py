'''module docstring'''
import requests


URL = 'https://python.gel.ulaval.ca/quoridor/api/'

def lister_parties(idul):
    """Lister les identifiants de vos parties les plus récentes.
    Récupère les parties en effectuant une requête à l'URL cible
    quoridor/api/parties/
    Cette requête de type GET s'attend en entrée à recevoir
    un seul paramètre nommé `idul` qui identifie son auteur.
    En cas de succès (code `200`), elle retourne en JSON
    un dictionnaire contenant la clé suivante:
        parties: une liste des (max) 20 parties les plus récentes de l'usager;
    où chaque partie dans la liste est elle-même un dictionnaire
    contenant les clés suivantes:
        id: l'identifiant de la partie;
        état: l'état actuel du jeu sous la forme d'un dictionnaire.
    En cas d'erreur, si le code de votre réponse est 406,
    elle retourne en JSON un dictionnaire contenant la clé suivante:
        message: un message en cas d'erreur;
    Args:
        idul (str): Identifiant de l'auteur des parties.
    Returns:
        list: Liste des parties reçues du serveur,
            après avoir décodé le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsqu'il y a présence d'un message
            dans la réponse du serveur.
    Examples:
        >>> idul = "josmi42"
        >>> parties = lister_parties(idul)
        >>> print(parties)
        [{ 'id': 'c1493454-1f7f-446f-9c61-bd7a9d66c92d',
        'état': { 'joueurs': ..., 'murs': ... }}, ... ]
    """
    rep = requests.get(URL + 'parties/', {'idul': idul})
    if rep.status_code == 200:
        liste = rep.json()['parties']
        return liste
    raise RuntimeError(rep.json()['message'])



def initialiser_partie(idul):
    """Initialiser une nouvelle partie.
    Initialise une partie en effectuant une requête à l'URL cible
    quoridor/api/partie/
    Cette requête est de type POST, contrairement à lister_parties,
    car elle modifie l'état interne du serveur en créant une nouvelle partie.
    Elle s'attend en entrée à recevoir une seule donnée nommée idul,
    toujours sous la forme d'une chaîne de caractères.
    En cas de succès (code `200`), elle retourne en JSON
    un dictionnaire contenant les clés suivantes:
        id: l'identifiant de la nouvelle partie;
        état: l'état initial du jeu sous la forme d'un dictionnaire;
    En cas d'erreur (code `406`), elle retourne en JSON
    un dictionnaire contenant la clé suivante:
        message: un message en cas d'erreur.
    Args:
        idul (str): Identifiant du joueur.
    Returns:
        tuple: Tuple constitué de l'identifiant de la partie et de l'état initial du jeu.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
    Examples:
        >>> idul = 'josmi42'
        >>> partie = initialiser_partie(idul)
        >>> print(partie)
        ('c1493454-1f7f-446f-9c61-bd7a9d66c92d', { 'joueurs': ... })
    """
    rep = requests.post(URL + 'partie/', {'idul': idul})
    if rep.status_code == 200:
        start = (rep.json()['id'], rep.json()['état'])
        return start
    raise RuntimeError(rep.json()['message'])


def jouer_coup(id_partie, type_coup, position):
    """Jouer votre coup dans une partie en cours
    Joue un coup en effectuant une requête à l'URL cible
    quoridor/api/jouer/
    Cette requête est de type PUT, contrairement à lister_parties,
    car elle modifie l'état interne du serveur en modifiant une partie existante.
    Elle s'attend à recevoir en entrée trois (3) paramètres associés au PUT:
        id: l'identifiant de la partie;
        type: le type de coup du joueur
            'D' pour déplacer le jeton,
            'MH' pour placer un mur horizontal,
            'MV' pour placer un mur vertical;
        pos: la position (x, y) du coup.
    En cas de succès (code 200), elle retourne en JSON
    un dictionnaire pouvant contenir les clés suivantes:
        état: l'état actuel du jeu;
        gagnant: le nom du joueur gagnant, None s'il n'y a pas encore de gagnant.
    En cas d'erreur (code 406), elle retourne en JSON
    un dictionnaire contenant la clé suivante:
        message: un message en cas d'erreur.
    Args:
        id_partie (str): Identifiant de la partie.
        type_coup (str): Type de coup du joueur :
                            'D' pour déplacer le jeton,
                            'MH' pour placer un mur horizontal,
                            'MV' pour placer un mur vertical;
        position (tuple): La position (x, y) du coup.
    Returns:
        dict: Tuple constitué de l'identifiant de la partie en cours
            et de l'état courant du jeu, après avoir décodé
            le JSON de sa réponse.
    Raises:
        RuntimeError: Erreur levée lorsque le serveur retourne un code 406.
        StopIteration: Erreur levée lorsqu'il y a un gagnant dans la réponse du serveur.
    Examples:
        >>> id_partie = 'c1493454-1f7f-446f-9c61-bd7a9d66c92d'
        >>> type_coup = 'D'
        >>> position = (3, 5)
        >>> partie = jouer_coup(id_partie, type_coup, position)
        >>> print(partie)
        ('c1493454-1f7f-446f-9c61-bd7a9d66c92d', { 'joueurs': ..., 'murs': ... })
    """
    rep = requests.put(URL + 'jouer/', {'id': id_partie, 'type': type_coup, 'pos': position})
    stats = rep.json()
    if stats.get('gagnant'):
        raise StopIteration(rep.json()['gagnant'])
    if rep.status_code == 200:
        tuple_stats = (stats['id'], stats['état'])
        return tuple_stats
    raise RuntimeError(rep.json()['message'])
