from typing import List, Tuple

import type

def rename(characters: List[type.Character]) -> Tuple[str, str]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, str]: ancien et nouveau nom
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur de renommage de personnage <<<<<")
    
    print("\n  Liste des personnages :")
    for i in range(len(list_characters)):
        print(f"   {i} - {list_characters[i]}")
    
    print("\n  Personnage à renommer")
    old_name = list_characters[int(input("   >>> "))]
    
    print(f"\n  Nouveau nom pour {old_name}")
    new_name = input("   >>> ").strip()
    
    return old_name, new_name


def add(scenes: List[type.Scene], characters: List[type.Character]) -> Tuple[str, List[str]]:
    """ Éditeur d'ajout de personnage

    Args:
        scenes (List[type.Scene]): liste des scènes avec leurs informations

    Returns:
        Tuple[str, List[str]]: personnage à ajouter et liste des scènes dans lesquelles l'ajouter
    """
    
    list_scenes = [s["Scene"] for s in scenes]
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur d'ajout de personnage <<<<<")
    
    print("\n  Liste des personnages :")
    for i in range(len(list_characters)):
        print(f"   {i} - {list_characters[i]}")
        
    print("\n  Personnage à ajouter (si vous souhaitez ajouter un nouveau personnage, entrez son nom)")
    entry = input("   >>> ").strip()
    try:
        new_character = list_characters[int(entry)]
    except:
        new_character = entry
    
    print("\n  Liste des scènes :")
    for i in range(len(list_scenes)):
        print(f"   {i} - {list_scenes[i]}")
    
    scenes_to_add = []
    print(f"\n  Scènes où ajouter {new_character} (séparées par une virgule)")
    num_sc = input("   >>> ").split(",")
    for num in num_sc:
        scenes_to_add.append(list_scenes[int(num)])
    
    return new_character, scenes_to_add


def merge(characters: List[type.Character]) -> Tuple[str, str]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, str]: personnages à fusionner (source et destination)
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur de fusion de personnages <<<<<")
    
    print("\n  Liste des personnages :")
    for i in range(len(list_characters)):
        print(f"   {i} - {list_characters[i]}")
    
    print("\n  Personnage à fusionner (source) :")
    source_character = list_characters[int(input("   >>> "))]
    
    print(f"\n  Personnage à fusionner (destination) :")
    destination_character = list_characters[int(input("   >>> "))]
    
    return source_character, destination_character