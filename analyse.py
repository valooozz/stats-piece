import csv
from typing import List
import warnings
from matplotlib import pyplot as plt

import type

warnings.filterwarnings("ignore") # Pour ignorer les warnings de matplotlib

def get_characters(file_name: str) -> List[type.Character]:
    """ Récupère les données des personnages depuis le fichier CSV

    Args:
        file_name (str): nom du fichier à lire

    Returns:
        List[type.Character]: liste de personnages avec les informations associées à chacun
    """
    
    characters = []
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            characters.append({
                'Name': row[type.HEADER_CHARACTERS["CharacterName"]],
                'Lines': int(row[type.HEADER_CHARACTERS["Lines"]]),
                'Words': int(row[type.HEADER_CHARACTERS["Words"]])
            })
    return characters


def get_scenes(file_name: str) -> List[type.Scene]:
    """ Récupère les données des scènes depuis le fichier CSV

    Args:
        file_name (str): nom du fichier

    Returns:
        List[type.Scene]: Liste des scènes avec les informations associées
    """
    
    scenes = []
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            scenes.append({
                'Scene': row[type.HEADER_SCENES["SceneName"]],
                'Lines': row[type.HEADER_SCENES["Lines"]],
                "Didascalies": row[type.HEADER_SCENES["Didascalies"]],
                'Words': row[type.HEADER_SCENES["Words"]],
                'Characters': row[type.HEADER_SCENES["Characters"]]
            })
    return scenes


def get_actors(file_name: str, characters: List[type.Character]) -> List[type.Actor]:
    """ Récupère les données des acteurs depuis le fichier CSV et les informations des personnages

    Args:
        file_name (str): _description_
        characters (List[type.Character]): _description_

    Returns:
        List[type.Actor]: _description_
    """
    
    actors = []
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        total_lines = 0
        total_words = 0
        for row in reader:
            characters_played = row[type.HEADER_ACTORS["CharactersPlayed"]].split(":")
            for character_played in characters_played:
                character = next((c for c in characters if c["Name"] == character_played), None)
                total_lines += character["Lines"]
                total_words += character["Words"]
            actors.append({
                "Name": row[type.HEADER_ACTORS["ActorName"]],
                "Lines": total_lines,
                "Words": total_words
            })
    if not actors:
        actors.append({
            "Name": "Aucun acteur enregistré",
            "Lines": 0,
            "Words": 0
        })
    return actors


def print_graphic(labels: List[str], lines: List[int], words: List[int]) -> None:
    """ Affiche un graphique avec matplotlib

    Args:
        labels (List[str]): liste des noms des personnages ou des scènes
        lines (List[int]): liste des nombres de répliques
        words (List[int]): liste des nombres de mots
    """

    x = range(len(labels))
    width = 0.35  # Largeur des barres

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, lines, width, label='Répliques')
    rects2 = ax.bar([p + width for p in x], words, width, label='Mots')

    # Ajouter des étiquettes, un titre et une légende
    ax.set_xlabel('Personnages')
    ax.set_ylabel('Nombre')
    ax.set_title('Nombre de répliques et de mots par personnage')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(labels)
    ax.legend()

    # Ajouter des valeurs au-dessus des barres
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points de décalage vertical
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    # Afficher le graphique
    plt.show()


def print_scenes(scenes: List[type.Scene], graphic: bool) -> None:
    """ Affiche les scènes et les personnages présents dans ces scènes

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        graphic (bool): affichage d'un graphique si cet argument est True
    """
    
    current_act = None
    for scene in scenes:
        act, numero_scene = scene['Scene'].split(':')
        if act != current_act:
            current_act = act
            print(f"=== Acte {act} ===")
        characters = scene['Characters'].split(':')
        characters_formated = ', '.join(sorted(character for character in characters if character))
        print(f"Scène {numero_scene}, Répliques : {scene['Lines']}, Didascalies : {scene['Didascalies']}, Mots : {scene['Words']}, Personnages : {characters_formated}")
    
    if graphic:
        scene_names = [scene['Scene'] for scene in scenes]
        total_lines = [int(scene['Lines']) for scene in scenes]
        total_words = [int(scene['Words']) for scene in scenes]
        
        print_graphic(scene_names, total_lines, total_words)


def print_scenes_with_nb(scenes: List[type.Scene], nb: int) -> None:
    """ Affiche les scènes contenant un certain nombre de personnages

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        nb (int): nombre de personnages à rechercher
    """
    
    current_act = None
    for scene in scenes:
        act, numero_scene = scene['Scene'].split(':')
        if act != current_act:
            current_act = act
            print(f"=== Acte {act} ===")
        characters = scene['Characters'].split(':')
        if len(characters) == nb:
            characters_formated = ', '.join(sorted(character for character in characters if character))
            print(f"Scène {numero_scene}, Répliques : {scene['Lines']}, Didascalies : {scene['Didascalies']}, Mots : {scene['Words']}, Personnages : {characters_formated}")


def print_nb_of_characters_in_scenes(scenes: List[type.Scene], nb_of_characters_in_piece: int) -> None:
    """ Affiche le nombre de scènes pour chaque nombre de personnages présent dans la pièce

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        nb_of_characters_in_piece (int): nombre total de personnages dans la pièce
    """
    
    info_nb_characters: List[int] = [0] * (nb_of_characters_in_piece+1)
    for scene in scenes:
        characters = scene["Characters"].split(":")
        info_nb_characters[len(characters)] += 1
    
    for i in range(len(info_nb_characters)):
        if info_nb_characters[i] > 0:
            print(f"Avec {i} personnage·s : {info_nb_characters[i]} scène·s")


def print_characters(characters: List[type.Character], graphic: bool) -> None:
    """ Affiche les personnages triés par nombre de mots décroissant

    Args:
        characters (List[type.Character]): liste des personnages
        graphic (bool): affichage d'un graphique si cet argument est True
    """
    
    characters_sorted = sorted(characters, key=lambda x: x["Words"], reverse=True)
    for character in characters_sorted:
        print(f"- {character['Name']}, Répliques : {character['Lines']}, Mots : {character['Words']}")
    
    if graphic:
        characters_names = [character["Name"] for character in characters_sorted]
        total_lines = [character["Lines"] for character in characters_sorted]
        total_words = [character["Words"] for character in characters_sorted]
        
        print_graphic(characters_names, total_lines, total_words)
        
        
def print_character_detail(characters: List[type.Character], scenes: List[type.Scene], nom_personnage: str) -> None:
    """ Affiche les informations détaillées d'un personnage spécifique

    Args:
        characters (List[type.Character]): liste des personnages
        scenes (List[type.Scene]): liste des scènes
        nom_personnage (str): nom du personnage
        graphic (bool): affichage d'un graphique si cet argument est True
    """
    
    # Recherche le personnage dans la liste des personnages
    personnage = next((c for c in characters if c["Name"] == nom_personnage), None)
    if personnage is None:
        print(f"Personnage '{nom_personnage}' non trouvé.")
        return

    # Recherche les scènes où le personnage est présent
    scenes_personnage = [scene for scene in scenes if nom_personnage in scene['Characters'].split(':')]

    # Affiche les informations de base du personnage
    print(f"\n=== {personnage['Name']} ===\nRépliques : {personnage['Lines']}\nMots : {personnage['Words']}\nNombre de scènes : {len(scenes_personnage)}")

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


def print_characters_together(scenes: List[type.Scene], list_characters: List[str]) -> None:
    """ Affiche les scènes où les personnages entrés sont ensemble

    Args:
        scenes (List[type.Scene]): liste des scènes avec les données collectées
        list_characters (List[str]): liste des personnages à rechercher
    """
    
    characters_set = set(list_characters)
    
    nb_scenes_together = 0
    
    current_act = None
    for scene in scenes:
        act, numero_scene = scene['Scene'].split(':')
        if act != current_act:
            current_act = act
            print(f"=== Acte {act} ===")
        characters_scene = set(scene['Characters'].split(':'))

        if characters_set.issubset(characters_scene):
            nb_scenes_together += 1
            other_characters = characters_scene - characters_set
            other_characters_formated = ', '.join(sorted(other_characters))
            print(f"Scène {numero_scene} avec : {other_characters_formated}")
    
    print(f"\nCes personnages partagent {nb_scenes_together} scènes")