

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