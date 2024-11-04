from typing import List
import csv

import utils

def replace_string(file_name: str, old_string: str, new_string: str) -> None:
    """ Remplace une chaîne de caractères par une autre dans un fichier

    Args:
        file_name (str): nom du fichier
        old_string (str): ancienne chaîne de caractères
        new_string (str): nouvelle chaîne de caractères
    """
    
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()

    with open(file_name, "w", encoding="utf-8") as file:
        for line in lines:
            new_line = line.replace(old_string, new_string)
            file.write(new_line)


def rename_character(piece: str, old_name: str, new_name: str, ac: bool) -> None:
    """ Renomme un personnage dans les fichiers csv

    Args:
        piece (str): nom de la pièce
        old_name (str): ancien nom du personnage
        new_name (str): nouveau nom du personnage
        ac (bool): on renomme un·e comédien·ne si ce paramètre est True
    """
    
    scenes_file = utils.get_scenes_file(piece)
    if ac:
        people_file = utils.get_actors_file(piece)
    else:
        people_file = utils.get_characters_file(piece)
    
    replace_string(scenes_file, old_name, new_name)
    replace_string(people_file, old_name, new_name)


def add_character(piece: str, new_character: str, list_scenes: List[str]) -> None:
    """ Ajoute un personnage à une liste de scènes, et au fichier des personnages s'il n'existe pas déjà

    Args:
        piece (str): nom de la pièce
        new_character (str): nom du personnage à ajouter
        list_scenes (List[str]): liste des scènes dans lesquelles ajouter le personnage
    """
    
    scenes_file = utils.get_scenes_file(piece)
    characters_file = utils.get_characters_file(piece)
    
    with open(scenes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open(scenes_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            if row[0] in list_scenes:
                if new_character not in row[4].split(":"):
                    row[4] = row[4] + ":" + new_character
            writer.writerow(row)
    
    with open(characters_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row in rows:
        if new_character == row[0]:
            return
    
    with open(characters_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            writer.writerow(row)
        
        writer.writerow([new_character, 0, 0])


def merge_characters(piece: str, source_character: str, destination_characters: str) -> None:
    """ Fusionne deux personnages dans les fichiers csv

    Args:
        piece (str): nom de la pièce
        source_character (str): nom du personnage qui va disparaître en fusionnant
        destination_character (str): nom du personnage qui reçoit les informations de l'autre personnage
    """
    
    scenes_file = utils.get_scenes_file(piece)
    characters_file = utils.get_characters_file(piece)
    
    with open(scenes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open(scenes_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            list_characters = row[4].split(":")
            if source_character in list_characters:
                list_characters.remove(source_character)
                for destination_character in destination_characters:
                    if destination_character not in list_characters:
                        list_characters.append(destination_character)
            
            row[4] = ":".join(list_characters)
            writer.writerow(row)

    with open(characters_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    for row in rows:
        if row[0] == source_character:
            lines_of_source_character = int(row[1])
            words_of_source_character = int(row[2])
            break
    
    with open(characters_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            if row[0] in destination_characters:
                row[1] = int(row[1]) + lines_of_source_character
                row[2] = int(row[2]) + words_of_source_character
            if row[0] != source_character:
                writer.writerow(row)


def add_lines_and_words(piece: str, character_name: str, nb_lines_to_add: int, nb_words_to_add: int) -> None:
    """ Ajoute un certain nombre de répliques et de mots à un personnage

    Args:
        piece (str): nom de la pièce
        character_name (str): nom du personnage
        nb_lines_to_add (int): nombre de répliques à ajouter
        nb_words_to_add (int): nombre de mots à ajouter
    """
    
    characters_file = utils.get_characters_file(piece)

    with open(characters_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open(characters_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            if row[0] == character_name:
                row[1] = int(row[1]) + nb_lines_to_add
                row[2] = int(row[2]) + nb_words_to_add
            writer.writerow(row)


def delete_character(piece: str, characters_to_delete: str, ac: bool) -> None:
    """ Supprime un personnage

    Args:
        piece (str): nom de la pièce concernée
        character_name (str): nom du personnage à supprimer
        ac (bool): on supprime un·e comédien·ne si ce paramètre est True
    """
    
    scenes_file = utils.get_scenes_file(piece)
    if ac:
        people_file = utils.get_actors_file(piece)
    else:
        people_file = utils.get_characters_file(piece)
    
    with open(scenes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open(scenes_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            list_characters = row[4].split(":")
            for present_character in list_characters:
                if present_character in characters_to_delete:
                    list_characters.remove(present_character)
            
            row[4] = ":".join(list_characters)
            writer.writerow(row)
    
    with open(people_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

    with open(people_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in rows:
            if row[0] not in characters_to_delete:
                writer.writerow(row)