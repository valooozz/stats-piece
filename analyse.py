import csv
from typing import List, Dict


def get_characters(file_name: str) -> List[Dict[str, int]]:
    """ Récupère les données des personnages depuis le fichier CSV

    Args:
        file_name (str): nom du fichier à lire

    Returns:
        List[Dict[str, int]]: liste de personnages avec les informations associées à chacun
    """
    
    characters = []
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            characters.append({
                'Character': row['Character'],
                'Total lines': int(row['Total lines']),
                'Total Words': int(row['Total Words'])
            })
    return characters


def get_scenes(file_name: str) -> List[Dict[str, str]]:
    """ Récupère les données des scènes depuis le fichier CSV

    Args:
        file_name (str): nom du fichier

    Returns:
        List[Dict[str, str]]: Liste des scènes avec les informations associées
    """
    
    scenes = []
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            scenes.append({
                'Scene': row['Scene'],
                'Characters': row['Characters']
            })
    return scenes


def print_scenes(scenes: List[Dict[str, str]]) -> None:
    """ Affiche les scènes et les personnages présents dans ces scènes

    Args:
        scenes (List[Dict[str, str]]): _description_
    """
    current_act = None
    for scene in scenes:
        act, numero_scene = scene['Scene'].split(':')
        if act != current_act:
            current_act = act
            print(f"=== Acte {act} ===")
        personnages = scene['Characters'].split(':')
        personnages_formates = ', '.join(sorted(personnage for personnage in personnages if personnage))
        print(f"Scène {numero_scene} : {personnages_formates}")


def print_characters(characters: List[Dict[str, int]]) -> None:
    """ Affiche les personnages triés par nombre de mots décroissant

    Args:
        characters (List[Dict[str, int]]): liste des personnages
    """
    
    characters_sorted = sorted(characters, key=lambda x: x['Total Words'], reverse=True)
    for character in characters_sorted:
        print(f"- {character['Character']}, Répliques : {character['Total lines']}, Mots : {character['Total Words']}")
        
        
def print_character_detail(characters: List[Dict[str, int]], scenes: List[Dict[str, str]], nom_personnage: str) -> None:
    """ Affiche les informations détaillées d'un personnage spécifique

    Args:
        characters (List[Dict[str, int]]): liste des personnages
        scenes (List[Dict[str, str]]): liste des scènes
        nom_personnage (str): nom du personnage
    """
    
    # Recherche le personnage dans la liste des personnages
    personnage = next((c for c in characters if c['Character'] == nom_personnage), None)
    if personnage is None:
        print(f"\nPersonnage '{nom_personnage}' non trouvé.")
        return

    # Affiche les informations de base du personnage
    print(f"\n=== {personnage['Character']}===\nRépliques : {personnage['Total lines']}\nMots : {personnage['Total Words']}")

    # Recherche les scènes où le personnage est présent
    scenes_personnage = [scene for scene in scenes if nom_personnage in scene['Characters'].split(':')]
    if not scenes_personnage:
        print(f"Le personnage '{nom_personnage}' n'est présent·e dans aucune scène.")
        return

    print(f"\nScènes où {nom_personnage} est présent·e :")
    current_act = None
    for scene in scenes_personnage:
        act, numero_scene = scene['Scene'].split(':')
        if act != current_act:
            current_act = act
            print(f"=== Acte {act} ===")
        act, numero_scene = scene['Scene'].split(':')
        personnages = scene['Characters'].split(':')
        personnages_formates = ', '.join(sorted(personnage for personnage in personnages if personnage and personnage != nom_personnage))
        print(f"Scène {numero_scene} avec : {personnages_formates}")

    # Recherche les autres personnages présents dans les scènes avec ce personnage
    other_characters = set()
    for scene in scenes_personnage:
        personnages = scene['Characters'].split(':')
        other_characters.update(personnage for personnage in personnages if personnage and personnage != nom_personnage)

    print(f"\nPersonnages sur scène avec {nom_personnage}:")
    print(', '.join(sorted(other_characters)))


def print_characters_together(scenes: List[Dict[str, str]], list_characters: List[str]) -> None:
    """ Affiche les scènes où les personnages entrés sont ensemble

    Args:
        scenes (List[Dict[str, str]]): liste des scènes avec les données collectées
        list_characters (List[str]): liste des personnages à rechercher
    """
    
    characters_set = set(list_characters)
    
    current_act = None
    for scene in scenes:
        act, numero_scene = scene['Scene'].split(':')
        if act != current_act:
            current_act = act
            print(f"=== Acte {act} ===")
        characters_scene = set(scene['Characters'].split(':'))

        if characters_set.issubset(characters_scene):
            other_characters = characters_scene - characters_set
            other_characters_formated = ', '.join(sorted(other_characters))
            print(f"Scène {numero_scene} avec : {other_characters_formated}")