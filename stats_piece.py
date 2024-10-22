import sys
from typing import Dict, List, Tuple

Character = str
Scene = Tuple[str, str]

def change_scene(old_act: str, old_scene: str, line: str) -> Tuple[bool, Scene, str]:
    """ Change le numéro de l'acte ou de la scène si la ligne est le titre d'acte ou de scène

    Args:
        old_act (str): ancien numéro d'acte
        old_scene (str): ancien numéro de scène
        line (str): ligne lue dans le fichier

    Returns:
        Tuple[bool, Scene]: True si la scène a changé, et la nouvelle scène ainsi que son nom
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

def add_character_in_scene(list_of_character: List[Character], new_character: Character) -> List[Character]:
    """ Ajoute un personnage à la liste des personnages d'une scène, si celui-ci n'y est pas déjà présent

    Args:
        list_of_character (List[Character]): liste des personnages de la scène
        new_character (Character): personnage rencontré à la ligne lue dans le fichier

    Returns:
        List[Character]: nouvelle liste des personnages de la scène
    """
    
    if new_character not in list_of_character:
        list_of_character.append(new_character)
    
    return list_of_character

def update_character_info(dico_characters: Dict[Character, Tuple[int, int]], character: Character, nb_words_in_new_line: int) -> Dict[Character, Tuple[int, int]]:
    """ Met à jour les informations sur un personnage
    
    Args:
        dico_characters (Dict[Character: Tuple[int, int]]): dictionnaire des informations sur les personnages
        character (Character): personnage à mettre à jour
        nb_words_in_new_line (int): nombre de mots dans la réplique du personnage

    Returns:
        Dict[Character: Tuple[int, int]]: nouveau dictionnaire des informations sur les personnages
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

def analyse_file(file_name: str):
    """ Analyse un fichier texte contenant une pièce de théâtre

    Args:
        file_name (str): nom du fichier à analyser
    """
    
    current_act: str = "0"
    current_scene: str = "0"
    
    dico_scenes: Dict[str, List[Character]] = {}
    dico_characters: Dict[Character, Tuple[int, int]] = {}
    
    list_of_characters_in_scene: List[Character] = []
    
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
        
        print(dico_scenes)
        print()
        print(dico_characters)
                
    except FileNotFoundError:
        print(f"Le fichier {file_name} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def main():
    # Vérifie si le nombre d'arguments est supérieur à 1 (le premier argument est toujours le nom du script)
    if len(sys.argv) < 2:
        print("python3 stats_piece.py [fichier txt à analyser]")
    else:
        # Affiche l'argument passé
        analyse_file(sys.argv[1])

if __name__ == "__main__":
    main()