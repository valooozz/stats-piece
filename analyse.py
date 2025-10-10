from typing import List
import warnings
from matplotlib import pyplot as plt
from prettytable import PrettyTable

import type
import utils

warnings.filterwarnings("ignore") # Pour ignorer les warnings de matplotlib


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
    rects1 = ax.bar(x, lines, width, label="Répliques")
    rects2 = ax.bar([p + width for p in x], words, width, label="Mots")

    # Ajouter des étiquettes, un titre et une légende
    ax.set_xlabel("Personnages")
    ax.set_ylabel("Nombre")
    ax.set_title("Nombre de répliques et de mots par personnage")
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
                        ha="center", va="bottom")

    autolabel(rects1)
    autolabel(rects2)

    plt.show()


def print_scenes(scenes: List[type.Scene], graphic: bool, ac: bool) -> None:
    """ Affiche les scènes et les personnages présents dans ces scènes

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        graphic (bool): affichage d'un graphique si cet argument est True
    """
    
    to_show, to_tell = utils.handle_ac(ac)

    table = PrettyTable()
    table.field_names = ["Scène", "Répliques", "Didascalies", "Mots", f"{to_tell.capitalize()}s"]

    current_act = None
    for scene in scenes:
        act, numero_scene = scene["Scene"].split(":")
        if act != current_act:
            current_act = act
            table.add_row(utils.get_act_separator(act))

        characters = scene[to_show]
        characters_formated = ', '.join(sorted(character for character in characters if character))
        table.add_row([numero_scene, scene['Lines'], scene['Didascalies'], scene['Words'], characters_formated])

    print(table)
    
    if graphic:
        scene_names = [scene['Scene'] for scene in scenes]
        total_lines = [int(scene['Lines']) for scene in scenes]
        total_words = [int(scene['Words']) for scene in scenes]
        
        print_graphic(scene_names, total_lines, total_words)


def print_acts(scenes: List[type.Scene], graphic: bool, ac: bool) -> None:
    """ Affiche les actes et les personnages présents dans ces actes

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        graphic (bool): affichage d'un graphique si cet argument est True
        ac (bool): on affiche les comédien·nes si cet argument est True
    """
    
    to_show, to_tell = utils.handle_ac(ac)
    
    # Grouper les scènes par acte
    acts_data = {}
    for scene in scenes:
        act, _ = scene["Scene"].split(":")
        if act not in acts_data:
            acts_data[act] = {
                'Lines': 0,
                'Didascalies': 0,
                'Words': 0,
                'Characters': set(),
            }
        
        # Agréger les données
        acts_data[act]['Lines'] += int(scene['Lines'])
        acts_data[act]['Didascalies'] += int(scene['Didascalies'])
        acts_data[act]['Words'] += int(scene['Words'])
        acts_data[act]['Characters'].update(scene[to_show])
    
    table = PrettyTable()
    table.field_names = ["Acte", "Répliques", "Didascalies", "Mots", f"{to_tell.capitalize()}s"]
    
    # Trier les actes par numéro
    sorted_acts = sorted(acts_data.keys(), key=lambda x: int(x) if x.isdigit() else float('inf'))
    
    for act in sorted_acts:
        data = acts_data[act]
        characters_formated = ', '.join(sorted(character for character in data['Characters'] if character))
        table.add_row([act, data['Lines'], data['Didascalies'], data['Words'], characters_formated])
    
    print(table)
    
    if graphic:
        act_names = [f"Acte {act}" for act in sorted_acts]
        total_lines = [acts_data[act]['Lines'] for act in sorted_acts]
        total_words = [acts_data[act]['Words'] for act in sorted_acts]
        
        print_graphic(act_names, total_lines, total_words)


def print_scenes_with_nb(scenes: List[type.Scene], nb: int) -> None:
    """ Affiche les scènes contenant un certain nombre de personnages

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        nb (int): nombre de personnages à rechercher
    """
    
    table = PrettyTable()
    table.field_names = ["Scène", "Répliques", "Didascalies", "Mots", "Personnages"]

    current_act = None
    for scene in scenes:
        act, numero_scene = scene["Scene"].split(':')
        if act != current_act:
            current_act = act
            table.add_row(utils.get_act_separator(act))

        characters = scene["Characters"]
        if len(characters) == nb:
            characters_formated = ', '.join(sorted(character for character in characters if character))
            table.add_row([numero_scene, scene['Lines'], scene['Didascalies'], scene['Words'], characters_formated])

    print(table)
    

def print_nb_of_characters_in_scenes(scenes: List[type.Scene], nb_of_characters_in_piece: int) -> None:
    """ Affiche le nombre de scènes pour chaque nombre de personnages présent dans la pièce

    Args:
        scenes (List[type.Scene]): liste des scènes avec les informations associées
        nb_of_characters_in_piece (int): nombre total de personnages dans la pièce
    """
    
    info_nb_characters: List[int] = [0] * (nb_of_characters_in_piece+1)
    for scene in scenes:
        characters = scene["Characters"]
        info_nb_characters[len(characters)] += 1
    
    for i in range(len(info_nb_characters)):
        if info_nb_characters[i] > 0:
            print(f"Avec {i} personnage·s : {info_nb_characters[i]} scène·s")


def print_characters(characters: List[type.Character], ac: bool, graphic: bool) -> None:
    """ Affiche les personnages triés par nombre de mots décroissant

    Args:
        characters (List[type.Character]): liste des personnages
        ac (bool): on affiche les comédien·nes si cet argument est True
        graphic (bool): affichage d'un graphique si cet argument est True
    """

    table = PrettyTable()
    if ac:
        table.field_names = ["Nom", "Répliques", "Mots", "Rôles"]
    else:
        table.field_names = ["Nom", "Répliques", "Mots"]

    characters_sorted = sorted(characters, key=lambda x: x["Words"], reverse=True)
    for character in characters_sorted:
        if ac:
            roles = ", ".join(character["Characters"])
            table.add_row([character['Name'], character['Lines'], character['Words'], roles])
        else:
            table.add_row([character['Name'], character['Lines'], character['Words']])

    print(table)
    
    if graphic:
        characters_names = [character["Name"] for character in characters_sorted]
        total_lines = [character["Lines"] for character in characters_sorted]
        total_words = [character["Words"] for character in characters_sorted]
        
        print_graphic(characters_names, total_lines, total_words)
        
        
def print_character_detail(characters: List[type.Character], scenes: List[type.Scene], nom_personnage: str, ac: bool) -> None:
    """ Affiche les informations détaillées d'un personnage spécifique

    Args:
        characters (List[type.Character]): liste des personnages
        scenes (List[type.Scene]): liste des scènes
        nom_personnage (str): nom du personnage
        ac (bool): on regarde un·e comédien·ne plutôt qu'un personnage si cet argument est True
    """
    
    to_show, to_tell = utils.handle_ac(ac)
    
    # Recherche le personnage dans la liste des personnages
    personnage = next((c for c in characters if c["Name"] == nom_personnage), None)
    if personnage is None:
        print(f"{to_tell.capitalize()} '{nom_personnage}' non trouvé.")
        return

    # Recherche les scènes où le personnage est présent
    scenes_personnage = [scene for scene in scenes if nom_personnage in scene[to_show]]

    base_info_table = PrettyTable()
    if ac:
        base_info_table.field_names = ["Nom", "Répliques", "Mots", "Nombre de scènes", "Personnages joués"]
        roles = ", ".join(personnage["Characters"])
        base_info_table.add_row([personnage['Name'], personnage['Lines'], personnage['Words'], len(scenes_personnage), roles])
    else:
        base_info_table.field_names = ["Nom", "Répliques", "Mots", "Nombre de scènes"]
        base_info_table.add_row([personnage['Name'], personnage['Lines'], personnage['Words'], len(scenes_personnage)])

    print(base_info_table)

    if not scenes_personnage:
        print(f"Le {to_tell} '{nom_personnage}' n'est présent·e dans aucune scène.")
        return

    # Tableau pour les scènes où le personnage est présent
    scenes_table = PrettyTable()
    scenes_table.field_names = ["Scène", f"{to_tell.capitalize()}s présents avec {nom_personnage}"]

    current_act = None
    for scene in scenes_personnage:
        act, numero_scene = scene["Scene"].split(':')
        if act != current_act:
            current_act = act
            scenes_table.add_row([f"=== Acte {act} ===", "=========="])

        personnages = scene[to_show]
        personnages_formates = ', '.join(sorted(personnage for personnage in personnages if personnage and personnage != nom_personnage))
        scenes_table.add_row([numero_scene, personnages_formates])

    print(scenes_table)

    # Recherche les autres personnages présents dans les scènes avec ce personnage
    shared_scene_characters = set()
    for scene in scenes_personnage:
        personnages = scene[to_show]
        shared_scene_characters.update(personnage for personnage in personnages if personnage and personnage != nom_personnage)
    
    other_characters = []
    for c in characters:
        if c["Name"] not in shared_scene_characters and c["Name"] != nom_personnage:
            other_characters.append(c["Name"])

    # Tableau pour les personnages présents dans les scènes avec lui
    other_characters_table = PrettyTable()
    other_characters_table.field_names = [f"{to_tell.capitalize()}s sur scène avec {nom_personnage}", "Aucune scène en commun"]
    other_characters_table.add_row([", ".join(sorted(shared_scene_characters)), ", ".join(sorted(other_characters))])
    print(other_characters_table)


def print_characters_together(scenes: List[type.Scene], list_characters: List[str], ac: bool) -> None:
    """ Affiche les scènes où les personnages entrés sont ensemble

    Args:
        scenes (List[type.Scene]): liste des scènes avec les données collectées
        list_characters (List[str]): liste des personnages à rechercher
    """
    
    to_show, to_tell = utils.handle_ac(ac)

    characters_set = set(list_characters)
    nb_scenes_together = 0

    scenes_table = PrettyTable()
    scenes_table.field_names = ["Scène", f"Autres {to_tell}s présents"]

    current_act = None
    for scene in scenes:
        act, numero_scene = scene["Scene"].split(':')
        if act != current_act:
            current_act = act
            scenes_table.add_row([f"=== Acte {act} ===", "=========="])

        characters_scene = set(scene[to_show])

        if characters_set.issubset(characters_scene):
            nb_scenes_together += 1
            other_characters = characters_scene - characters_set
            other_characters_formated = ', '.join(sorted(other_characters))
            scenes_table.add_row([numero_scene, other_characters_formated])

    print(scenes_table)

    print(f"\nCes {to_tell}s partagent {nb_scenes_together} scènes")