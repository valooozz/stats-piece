from typing import List, Tuple

import type
import utils


def print_list(list_to_print: List[str], title: str) -> None:
    """ Affiche une liste donnée

    Args:
        list_to_print (List[str]): liste à afficher
        title (str): titre de la liste
    """
    
    print(f"\n  Liste des {title} :")
    for i in range(len(list_to_print)):
        print(f"   {i} - {list_to_print[i]}")
        

def get_one(title: str, list_to_pick: List[str]) -> str:
    """ Retourne un élément choisi dans une liste

    Args:
        title (str): titre du choix
        list_to_pick (List[str]): liste dans laquelle choisir

    Returns:
        str: valeur choisie dans la liste
    """
    
    print(f"\n  {title}")
    num = int(input("   >>> "))
    result = list_to_pick[num]
    return result


def get_multiple(title: str, list_to_pick: List[str]) -> List[str]:
    """ Retourne une liste d'éléments choisis dans une liste

    Args:
        title (str): titre du choix
        list_to_pick (List[str]): liste dans laquelle choisir

    Returns:
        List[str]: liste d'éléments choisis
    """
    
    print(f"\n  {title} (séparés par une virgule)")
    num = input("   >>> ").split(",")
    result = [list_to_pick[int(i)] for i in num]
    return result


def nw(scenes: List[type.Scene]) -> Tuple[str, int, int, int, str]:
    """ Éditeur d'ajout de scène

    Args:
        scenes (List[type.Scene]): liste des scènes avec leurs informations

    Returns:
        Tuple[str, int, int, int, str]: infos sur la nouvelle scène et scène qui la suit
    """    
    
    list_scenes = utils.extract_list_names(scenes, "Scene")
    
    print("\n  >>>>> Éditeur d'ajout de scène <<<<<")
    
    print("\n  Nom de la nouvelle scène")
    new_scene = input("   >>> ")
    
    print("\n  Nombre de répliques")
    nb_lines = int(input("   >>> "))
    
    print("\n  Nombre de didascalies")
    nb_didascalies = int(input("   >>> "))
    
    print("\n  Nombre de mots")
    nb_words = int(input("   >>> "))    
    
    print_list(list_scenes, "scènes")
    print(f"\n  Scène suivant la nouvelle scène (n'entrez rien si elle doit être ajoutée à la fin)")
    num = input("   >>> ")
    try:
        next_scene = list_scenes[int(num)]
    except:
        next_scene = "last"
        
    return new_scene, nb_lines, nb_didascalies, nb_words, next_scene
    

def rn(characters: List[type.Character], people_name: str) -> Tuple[str, str]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations
        people_name (str): nom des personnages étudiées
        

    Returns:
        Tuple[str, str]: ancien et nouveau nom
    """
    
    list_characters = utils.extract_list_names(characters, "Name")
    
    print(f"\n  >>>>> Éditeur de renommage de {people_name}s <<<<<")
    
    print_list(list_characters, f"{people_name}s")
    old_name = get_one(f"{people_name.capitalize()}s à renommer", list_characters)
    
    print(f"\n  Nouveau nom pour {old_name}")
    new_name = input("   >>> ").strip()
    
    return old_name, new_name


def ad(scenes: List[type.Scene], characters: List[type.Character]) -> Tuple[str, List[str]]:
    """ Éditeur d'ajout de personnage

    Args:
        scenes (List[type.Scene]): liste des scènes avec leurs informations

    Returns:
        Tuple[str, List[str]]: personnage à ajouter et liste des scènes dans lesquelles l'ajouter
    """
    
    list_scenes = utils.extract_list_names(scenes, "Scene")
    list_characters = utils.extract_list_names(characters, "Name")
    
    print("\n  >>>>> Éditeur d'ajout de personnage <<<<<")
    
    print_list(list_characters, "personnages")
        
    print("\n  Personnage à ajouter (si vous souhaitez ajouter un nouveau personnage, entrez son nom)")
    entry = input("   >>> ").strip()
    try:
        new_character = list_characters[int(entry)]
    except:
        new_character = entry
    
    print_list(list_scenes, "scènes")
    scenes_to_add = get_multiple(f"Scènes où ajouter {new_character}", list_scenes)
    
    return new_character, scenes_to_add


def mg(characters: List[type.Character]) -> Tuple[str, List[str]]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, List[str]]: personnages à fusionner (source et destinations)
    """
    
    list_characters = utils.extract_list_names(characters, "Name")
    
    print("\n  >>>>> Éditeur de fusion de personnages <<<<<")
    
    print_list(list_characters, "personnages")
    source_character = get_one("Personnage à fusionner (source)", list_characters)
    destination_characters = get_multiple("Personnages à fusionner (destination)", list_characters)
    
    return source_character, destination_characters


def dt(characters: List[type.Character], people_name: str) -> str:
    """ Éditeur de choix de personnage pour la commande dt

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations
        people_name (str): nom des personnages étudiées

    Returns:
        str: personnage à afficher
    """
    
    list_characters = utils.extract_list_names(characters, "Name")
    
    print(f"\n  >>>>> Choix de {people_name} <<<<<")
    
    print_list(list_characters, f"{people_name}s")
    character = get_one(f"{people_name.capitalize()} à étudier", list_characters)
    
    return character


def tg(characters: List[type.Character], people_name: str) -> List[str]:
    """ Éditeur de choix de personnages pour la commande tg

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations
        people_name (str): nom des personnages étudiées

    Returns:
        List[str]: liste de personnage à étudier
    """
    
    list_characters = utils.extract_list_names(characters, "Name")
    
    print(f"\n  >>>>> Choix des {people_name}s <<<<<")
    
    print_list(list_characters, f"{people_name}s")
    characters_to_study = get_multiple(f"{people_name.capitalize()}s à étudier", list_characters)
    
    return characters_to_study


def sp(characters: List[type.Character]) -> Tuple[str, int, int]:
    """ Éditeur de choix pour la commande sp

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, int, int]: personnage, nombre de répliques, et nombre de mots
    """
    
    list_characters = utils.extract_list_names(characters, "Name")
    
    print("\n  >>>>> Choix de personnage <<<<<")
    
    print_list(list_characters, "personnages")
    character = get_one("Personnage à modifier", list_characters)
    
    print(f"\n  Nombre de répliques à ajouter à {character}")
    nb_lines_to_add = int(input("   >>> "))
    
    print(f"\n  Nombre de mots à ajouter à {character}")
    nb_words_to_add = int(input("   >>> "))
    
    return character, nb_lines_to_add, nb_words_to_add


def dl(characters: List[type.Character], people_name: str) -> str:
    """ Éditeur de choix de personnage pour la commande dl

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations
        people_name (str): nom des personnages étudiées

    Returns:
        str: personnage à afficher
    """
    
    list_characters = utils.extract_list_names(characters, "Name")
    
    print(f"\n  >>>>> Choix de {people_name}s <<<<<")
    
    print_list(list_characters, f"{people_name}s")
    characters_to_study = get_multiple(f"{people_name.capitalize()}s à supprimer", list_characters)
    
    return characters_to_study


def lk(actors: List[type.Actor], characters: List[type.Character]) -> Tuple[str, List[str]]:
    """ Éditeur de création de lien entre comédien·ne et personnage·s

    Args:
        actors (List[type.Actor]): liste des comédien·nes avec leurs infos
        characters (List[type.Character]): liste des personnages avec leurs infos

    Returns:
        Tuple[str, List[str]]: nom du comédien·ne et des personnages à relier
    """
    
    list_actors = utils.extract_list_names(actors, "Name")
    list_characters = utils.extract_list_names(characters, "Name")
    
    print("\n  >>>>> Éditeur de lien <<<<<")
    
    print_list(list_actors, "comédien·nes")
    
    print("\n  Comédien·e à relier (si vous souhaitez ajouter un·e nouveau·lle comédien·ne, entrez son nom)")
    entry = input("   >>> ").strip()
    try:
        actor_to_link = list_actors[int(entry)]
    except:
        actor_to_link = entry
    
    print_list(list_characters, "personnages")
    characters_to_link = get_multiple("Personnages à relier", list_characters)
    
    return actor_to_link, characters_to_link


def ul(actors: List[type.Actor], characters: List[type.Character]) -> Tuple[str, str]:
    """ Éditeur de destruction de lien entre comédien·ne et personnage

    Args:
        actors (List[type.Actor]): liste des comédien·nes avec leurs infos
        characters (List[type.Character]): liste des personnages avec leurs infos

    Returns:
        Tuple[str, str]: nom du comédien·ne et du personnage à séparer
    """
    
    list_actors = utils.extract_list_names(actors, "Name")
    list_characters = utils.extract_list_names(characters, "Name")
    
    print("\n  >>>>> Éditeur de séparation <<<<<")
    
    print_list(list_actors, "comédien·nes")
    actor_to_link = get_one("Comédien·ne à séparer", list_actors)
    
    print_list(list_characters, "personnages")
    characters_to_link = get_one("Personnage à séparer", list_characters)
    
    return actor_to_link, characters_to_link