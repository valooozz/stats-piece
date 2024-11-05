from typing import List
import csv

import utils
import type


def get_characters(piece: str) -> List[type.Character]:
    """ Récupère les données des personnages depuis le fichier CSV

    Args:
        piece (str): nom de la pièce

    Returns:
        List[type.Character]: liste de personnages avec les informations associées à chacun
    """
    
    characters_file = utils.get_characters_file(piece)
    
    characters = []
    with open(characters_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            characters.append({
                'Name': row[type.HEADER_CHARACTERS["CharacterName"]],
                'Lines': int(row[type.HEADER_CHARACTERS["Lines"]]),
                'Words': int(row[type.HEADER_CHARACTERS["Words"]])
            })
    return characters


def get_scenes(piece: str) -> List[type.Scene]:
    """ Récupère les données des scènes depuis le fichier CSV

    Args:
        piece (str): nom de la pièce

    Returns:
        List[type.Scene]: Liste des scènes avec les informations associées
    """
    
    scenes_file = utils.get_scenes_file(piece)
    
    scenes = []
    with open(scenes_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            list_characters = row[type.HEADER_SCENES["Characters"]].split(":")
            list_actors = get_actors_linked_to_characters(piece, list_characters)
            
            scenes.append({
                'Scene': row[type.HEADER_SCENES["SceneName"]],
                'Lines': row[type.HEADER_SCENES["Lines"]],
                "Didascalies": row[type.HEADER_SCENES["Didascalies"]],
                'Words': row[type.HEADER_SCENES["Words"]],
                'Characters': list_characters,
                "Actors": list_actors
            })
            
    return scenes


def get_actors_linked_to_characters(piece: str, list_characters: List[str]) -> List[str]:
    """ Donne la liste de comédien·nes lié·es à une liste de personnages

    Args:
        piece (str): nom de la pièce
        list_characters (List[str]): liste des personnages

    Returns:
        List[str]: liste des comédien·nes
    """
    
    actors_file = utils.get_actors_file(piece)
    
    list_actors = []
    with open(actors_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for character in list_characters:
            for row in rows:
                if character in row[type.HEADER_ACTORS["CharactersPlayed"]].split(":"):
                    list_actors.append(row[type.HEADER_ACTORS["ActorName"]])
    return list_actors
            

def get_actors(piece: str, characters: List[type.Character]) -> List[type.Actor]:
    """ Récupère les données des acteurs depuis le fichier CSV et les informations des personnages

    Args:
        piece (str): nom de la pièce
        characters (List[type.Character]): liste des personnages avec les informations associées

    Returns:
        List[type.Actor]: liste de comédien·nes avec leurs informations associées
    """
    
    actors_file = utils.get_actors_file(piece)
    
    actors = []
    with open(actors_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_lines = 0
            total_words = 0
            
            characters_played = row[type.HEADER_ACTORS["CharactersPlayed"]].split(":")
            for character_played in characters_played:
                character = next((c for c in characters if c["Name"] == character_played), None)            
                total_lines += character["Lines"]
                total_words += character["Words"]

            actors.append({
                "Name": row[type.HEADER_ACTORS["ActorName"]],
                "Lines": total_lines,
                "Words": total_words,
                "Characters": characters_played
            })
    if not actors:
        actors.append({
            "Name": "Aucun acteur enregistré",
            "Lines": 0,
            "Words": 0
        })
    return actors