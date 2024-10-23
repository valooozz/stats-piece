import sys
import os
import csv
from typing import Dict, List, Tuple

import data

CharacterName = str
SceneName = Tuple[str, str]

def change_scene(old_act: str, old_scene: str, line: str) -> Tuple[bool, SceneName, str]:
    """ Change le numéro de l'acte ou de la scène si la ligne est le titre d'acte ou de scène

    Args:
        old_act (str): ancien numéro d'acte
        old_scene (str): ancien numéro de scène
        line (str): ligne lue dans le fichier

    Returns:
        Tuple[bool, SceneName]: True si la scène a changé, et la nouvelle scène ainsi que son nom
    """
    
    new_act = old_act
    new_scene = old_scene
    change = False
    
    if "Acte" in line:
        new_act = line[5:]
        change = True
    elif "Scène" in line:
        new_scene = line[6:]
        change = True
        
    last_scene_name = f"{old_act}:{old_scene}"

    return (change, new_act, new_scene, last_scene_name)


def get_stats_line(line: str) -> Tuple[str, int]:
    """ Récupère des informations sur la ligne lorsque c'est une réplique d'un personnage

    Args:
        line (str): ligne lue dans le fichier

    Returns:
        tuple[str, int]: nom du personnage et nombre de mots dans la réplique
    """
    
    parts = line.split(":", 1)
    
    if len(parts) != 2: # Didascalie
        return None, None
    
    character = parts[0].strip()
    nb_words = len(parts[1].split())
    
    return character, nb_words


def add_character_in_scene(list_of_character: List[CharacterName], new_character: CharacterName) -> List[CharacterName]:
    """ Ajoute un personnage à la liste des personnages d'une scène, si celui-ci n'y est pas déjà présent

    Args:
        list_of_character (List[CharacterName]): liste des personnages de la scène
        new_character (CharacterName): personnage rencontré à la ligne lue dans le fichier

    Returns:
        List[CharacterName]: nouvelle liste des personnages de la scène
    """
    
    if new_character not in list_of_character:
        list_of_character.append(new_character)
    
    return list_of_character


def update_character_info(dico_characters: Dict[CharacterName, Tuple[int, int]], character: CharacterName, nb_words_in_new_line: int) -> Dict[CharacterName, Tuple[int, int]]:
    """ Met à jour les informations sur un personnage
    
    Args:
        dico_characters (Dict[CharacterName: Tuple[int, int]]): dictionnaire des informations sur les personnages
        character (CharacterName): personnage à mettre à jour
        nb_words_in_new_line (int): nombre de mots dans la réplique du personnage

    Returns:
        Dict[CharacterName: Tuple[int, int]]: nouveau dictionnaire des informations sur les personnages
    """
    
    try:
        nb_lines = dico_characters[character][0]
        nb_words = dico_characters[character][1]
    except:
        nb_lines = 0
        nb_words = 0
    
    nb_lines += 1
    nb_words += nb_words_in_new_line
    
    dico_characters[character] = (nb_lines, nb_words)
    
    return dico_characters


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


def write_info(dir_name: str, dico_scenes: Dict[str, List[CharacterName]], dico_characters: Dict[str, Tuple[int, int]]) -> bool:
    """ Écris les statistiques collectées dans des fichiers csv

    Args:
        dir_name (str): nom du dossier dans lequel créer les fichiers
        dico_scenes (Dict[str, List[CharacterName]]): dictionnaire contenant des infos sur les scènes
        dico_characters (Dict[str, Tuple[int, int]]): dictionnaire contenant des infos sur les personnages
        
    Returns:
        bool: retourn True si les informations ont bien été écrites
    """
    
    directory_created = create_directory(dir_name)
    if not directory_created:
        return False
    
    file_scenes = f"{dir_name}/scenes.csv"
    file_characters = f"{dir_name}/characters.csv"
    
    with open(file_scenes, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["SceneName", "CharacterNames"])
        
        for scene, list_characters in dico_scenes.items():
            str_characters = ":".join(list_characters)
            writer.writerow([scene, str_characters])
    
    with open(file_characters, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CharacterName", "Total lines", "Total Words"])
        
        for character, (total_lines, total_words) in dico_characters.items():
            writer.writerow([character, total_lines, total_words])
    
    data.add_piece(dir_name)
    
    return True


def read_file(file_name: str) -> Tuple[Dict[str, List[CharacterName]], Dict[CharacterName, Tuple[int, int]]]:
    """ Analyse un fichier texte contenant une pièce de théâtre

    Args:
        file_name (str): nom du fichier à analyser
    
    Returns:
        Tuple[Dict[str, List[CharacterName]], Dict[CharacterName, Tuple[int, int]]]: dictionnaires des infos sur les scènes et les personnages
    """
    
    current_act: str = "0"
    current_scene: str = "0"
    
    dico_scenes: Dict[str, List[CharacterName]] = {}
    dico_characters: Dict[CharacterName, Tuple[int, int]] = {}
    
    list_of_characters_in_scene: List[CharacterName] = []
    
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # strip() enlève les caractères de fin de ligne (comme \n)
                
                scene_has_changed, current_act, current_scene, last_scene_name = change_scene(current_act, current_scene, line)
                
                if scene_has_changed and list_of_characters_in_scene:
                    dico_scenes[last_scene_name] = list_of_characters_in_scene
                    list_of_characters_in_scene = []
                    continue
                
                character, nb_words = get_stats_line(line)
                if character and nb_words:
                    list_of_characters_in_scene = add_character_in_scene(list_of_characters_in_scene, character)
                    dico_characters = update_character_info(dico_characters, character, nb_words)
            
            dico_scenes[f"{current_act}:{current_scene}"] = list_of_characters_in_scene # pour la dernière scène
        
        return dico_scenes, dico_characters
                
    except FileNotFoundError:
        print(f"Le fichier {file_name} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    
    return None, None


def read(file_name: str) -> None:
    """ Lit le fichier texte d'une pièce de théâtre pour collecter des données et les écrire dans des fichiers csv

    Args:
        file_name (str): Nom du fichier à lire
    """
    
    dir_name = file_name[:-4]
    dico_scenes, dico_characters = read_file(file_name)
    
    if dico_scenes and dico_characters:
        written = write_info(dir_name, dico_scenes, dico_characters)
    
        if written:
            print(f"Les statistiques ont bien été collectées et ont été enregistrées dans le dossier '{dir_name}'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python3 stats_piece.py [fichier txt à analyser]")
    else:
        file_name = sys.argv[1]
        read(file_name)