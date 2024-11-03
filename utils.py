from typing import Tuple

def get_characters_file(piece: str) -> str:
    return f"{piece}/characters.csv"

def get_scenes_file(piece: str) -> str:
    return f"{piece}/scenes.csv"

def get_actors_file(piece: str) -> str:
    return f"{piece}/actors.csv"

def handle_ac(ac: bool) -> Tuple[str, str]:
    if ac:
        return "Actors", "Comédien·ne"
    else:
        return "Characters", "Personnage"