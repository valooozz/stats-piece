from typing import Tuple
import os

def get_characters_file(piece: str) -> str:
    return f"{piece}/characters.csv"

def get_scenes_file(piece: str) -> str:
    return f"{piece}/scenes.csv"

def get_actors_file(piece: str) -> str:
    return f"{piece}/actors.csv"

def get_text_file(piece: str) -> str:
    return f"texts/{piece}.txt"

def handle_ac(ac: bool) -> Tuple[str, str]:
    if ac:
        return "Actors", "Comédien·ne"
    else:
        return "Characters", "Personnage"
    
def create_directory(dir_name: str) -> bool:
    """ Crée un dossier

    Args:
        dir_name (str): nom du dossier à créer

    Returns:
        bool: Retourne True si le dossier a bien été créé
    """
    try:
        os.makedirs(dir_name, exist_ok=True)
        return True
    except OSError as e:
        print(f"Erreur lors de la création du dossier '{dir_name}': {e}")
        return False