from typing import List, Tuple

import type


def print_list(list_to_print: List[str], title: str) -> None:
    """ Affiche une liste donnée

    Args:
        list_to_print (List[str]): liste à afficher
        title (str): titre de la liste
    """
    
    print(f"\n  Liste des {title} :")
    for i in range(len(list_to_print)):
        print(f"   {i} - {list_to_print[i]}")
        

def rn(characters: List[type.Character]) -> Tuple[str, str]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, str]: ancien et nouveau nom
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur de renommage de personnage <<<<<")
    
    print_list(list_characters, "personnages")
    
    print("\n  Personnage à renommer")
    old_name = list_characters[int(input("   >>> "))]
    
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
    
    list_scenes = [s["Scene"] for s in scenes]
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur d'ajout de personnage <<<<<")
    
    print_list(list_characters, "personnages")
        
    print("\n  Personnage à ajouter (si vous souhaitez ajouter un nouveau personnage, entrez son nom)")
    entry = input("   >>> ").strip()
    try:
        new_character = list_characters[int(entry)]
    except:
        new_character = entry
    
    print_list(list_characters, "scènes")
    
    scenes_to_add = []
    print(f"\n  Scènes où ajouter {new_character} (séparées par une virgule)")
    num_sc = input("   >>> ").split(",")
    for num in num_sc:
        scenes_to_add.append(list_scenes[int(num)])
    
    return new_character, scenes_to_add


def mg(characters: List[type.Character]) -> Tuple[str, List[str]]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, List[str]]: personnages à fusionner (source et destinations)
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur de fusion de personnages <<<<<")
    
    print_list(list_characters, "personnages")
    
    print("\n  Personnage à fusionner (source)")
    source_character = list_characters[int(input("   >>> "))]
    
    print("\n  Personnages à fusionner (destination) (séparés par une virgule)")
    num = input("   >>> ").split(",")
    destination_characters = [list_characters[int(i)] for i in num]
    
    return source_character, destination_characters


def dt(characters: List[type.Character]) -> str:
    """ Éditeur de choix de personnage pour la commande dt

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations

    Returns:
        str: personnage à afficher
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Choix de personnage <<<<<")
    
    print_list(list_characters, "personnages")
    
    print("\n  Personnage à étudier")
    character = list_characters[int(input("   >>> "))]
    
    return character


def tg(characters: List[type.Character]) -> List[str]:
    """ Éditeur de choix de personnages pour la commande tg

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations

    Returns:
        List[str]: liste de personnage à étudier
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Choix des personnages <<<<<")
    
    print_list(list_characters, "personnages")
    
    print("\n  Personnages à étudier (séparés par une virgule)")
    num = input("   >>> ").split(",")
    characters_to_study = [list_characters[int(i)] for i in num]
    
    return characters_to_study


def sp(characters: List[type.Character]) -> Tuple[str, int, int]:
    """ Éditeur de choix pour la commande sp

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, int, int]: personnage, nombre de répliques, et nombre de mots
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Choix de personnage <<<<<")
    
    print_list(list_characters, "personnages")
    
    print("\n  Personnage à modifier")
    character = list_characters[int(input("   >>> "))]
    
    print(f"\n  Nombre de répliques à ajouter à {character}")
    nb_lines_to_add = int(input("   >>> "))
    
    print(f"\n  Nombre de mots à ajouter à {character}")
    nb_words_to_add = int(input("   >>> "))
    
    return character, nb_lines_to_add, nb_words_to_add


def dl(characters: List[type.Character]) -> str:
    """ Éditeur de choix de personnage pour la commande dl

    Args:
        characters (List[type.Character]): liste des personnages avec leurs informations

    Returns:
        str: personnage à afficher
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Choix de personnage <<<<<")
    
    print_list(list_characters, "personnages")
    
    print("\n  Personnages à supprimer (séparés par une virgule)")
    num = input("   >>> ").split(",")
    characters_to_study = [list_characters[int(i)] for i in num]
    
    return characters_to_study


def lk():
    print("Editeur pas encore développé")