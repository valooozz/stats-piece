from typing import List
import csv

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
            print(line, new_line)
            file.write(new_line)


def rename_character(piece: str, old_name: str, new_name: str) -> None:
    """ Renomme un personnage dans les fichiers csv

    Args:
        piece (str): nom de la pièce
        old_name (str): ancien nom du personnage
        new_name (str): nouveau nom du personnage
    """
    
    scenes_file = f"{piece}/scenes.csv"
    characters_file = f"{piece}/characters.csv"
    
    replace_string(scenes_file, old_name, new_name)
    replace_string(characters_file, old_name, new_name)


def add_character(piece: str, new_character: str, list_scenes: List[str]) -> None:
    """ Ajoute un personnage à une liste de scènes, et au fichier des personnages s'il n'existe pas déjà

    Args:
        piece (str): nom de la pièce
        new_character (str): nom du personnage à ajouter
        list_scenes (List[str]): liste des scènes dans lesquelles ajouter le personnage
    """
    
    scenes_file = f"{piece}/scenes.csv"
    characters_file = f"{piece}/characters.csv"
    
    with open(scenes_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        lines = list(reader)
    
    with open(scenes_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in lines:
            if row[0] in list_scenes:
                if new_character not in row[4].split(":"):
                    row[4] = row[4] + ":" + new_character
            writer.writerow(row)
    
    with open(characters_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        lines = list(reader)

    for row in lines:
        if new_character == row[0]:
            return
    
    with open(characters_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        for row in lines:
            writer.writerow(row)
        
        writer.writerow([new_character, 0, 0])
