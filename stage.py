from typing import List
import csv

import utils

def link(piece: str, actor_name: str, character_names: List[str]) -> None:
    """ Relie un·e comédien·ne à des personnages

    Args:
        piece (str): nom de la pièce
        actor_name (str): nom du comédien
        character_names (List[str]): liste des noms des personnages
    """
    
    actors_file = utils.get_actors_file(piece)
    
    try:
        with open(actors_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
    except:
        rows = []
    
    found = False
    with open(actors_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            if row[0] == actor_name:
                found = True
                list_characters = row[1].split(":")
                for character in character_names:
                    if character not in list_characters:
                        list_characters.append(character)
                row[1] = ":".join(list_characters)
            writer.writerow(row)
        
        if not found:
            str_characters = ":".join(character_names)
            writer.writerow([actor_name, str_characters])


def unlink(piece: str, actor_name: str, character_name: str) -> None:
    """ Retirer un lien entre un·e comédien·ne et un personnage

    Args:
        piece (str): nom de la pièce
        actor_name (str): nom du comédien
        character_name (str): nom du personnage
    """
    
    actors_file = utils.get_actors_file(piece)
    
    with open(actors_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open(actors_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            if row[0] == actor_name:
                list_characters = row[1].split(":")
                if character_name in list_characters:
                    list_characters.remove(character_name)
                row[1] = ":".join(list_characters)
            writer.writerow(row)