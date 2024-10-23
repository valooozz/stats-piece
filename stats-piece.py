import os
import shutil

import read
import analyse
import data


def usage() -> None:
    """ Affiche les commandes possibles
    """
    print("\nh - Afficher cette aide")
    
    print("\nrd <fichier> - Lire un fichier texte pour collecter des données et les stockers dans des fichiers csv")
    
    print("\nls - Afficher la liste des pièces disponibles, dont on peut analyser les données")
    print("ld <dossier> - Charger les données présentes dans un dossier")
    print("dl <dossier> - Supprimer les données présentes dans un dossier")
    
    print("\nsc - Afficher les scènes et les personnages présents")
    print("ch [gr] - Afficher les personnages avec leur nombre de répliques et de mots (gr pour afficher un graphique)")
    print("dt [gr] <nom_personnage> - Afficher les informations détaillées d'un personnage spécifique (gr pour afficher un graphique)")
    print("tg <perso1> <perso2> <...> - Afficher les scènes en commun pour des personnages")
    print("pt sc|ch - Afficher le contenu du fichier csv pour les scènes (sc) ou les personnages (ch)")
    
    print("\nq - Quitter")


def delete_piece(piece: str) -> None:
    """ Supprime toutes les données associées à une pièce lue

    Args:
        piece (str): nom de la pièce
    """
    
    if os.path.exists(piece) and os.path.isdir(piece):
        shutil.rmtree(piece)
        data.remove_piece(piece)
        print(f"Les données associées à la pièce '{piece}' ont été supprimées avec succès")
    else:
        print(f"Le dossier '{piece}' n'existe pas")


def print_csv(piece: str, file_type: str) -> None:
    """ Affiche le fichier csv en dur

    Args:
        piece (str): nom de la pièce
        file_type (str): type du fichier (sc ou ch)
    """
    
    file_name = f"{piece}/"
    if file_type == "sc":
        file_name += "scenes.csv"
    elif file_type == "ch":
        file_name += "characters.csv"
    else:
        print("Veuillez entrer 'sc' ou 'ch' pour spécifier quel fichier afficher")
        return
        
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            print(line, end="")
    

def main(piece, characters, scenes) -> None:
    """ Fonction principale qui gère les commandes
    """
    
    try:
        while True:
            graphic = False
            
            command = input("\n > ").split()

            if command[0] == "h":
                usage()
                
            elif command[0] == "q":
                print("Au revoir !\n")
                break
            
            elif command[0] == "rd":
                file_name = command[1]
                read.read(file_name)
            
            elif command[0] == "ls":
                data.print_pieces()
                
            elif command[0] == "ld":
                piece = command[1]
                if data.piece_exists(piece):
                    characters = analyse.get_characters(f"{piece}/characters.csv")
                    scenes = analyse.get_scenes(f"{piece}/scenes.csv")
                    print(f"Les données de '{piece}' ont été chargées avec succès")
                else:
                    print(f"Aucune donnée ne correspond à la pièce '{piece}'")
            
            elif command[0] == "dl":
                piece_to_delete = command[1]
                delete_piece(piece_to_delete)
                
            else:
                if not characters or not scenes:
                    print("Vous devez d'abord charger les données d'une pièce")
                    
                elif command[0] == "sc":
                    if len(command) > 1:
                        if command[1] == "gr":
                            graphic = True
                    analyse.print_scenes(scenes, graphic)
                    
                elif command[0] == "ch":                
                    if len(command) > 1:
                        if command[1] == "gr":
                            graphic = True
                    analyse.print_characters(characters, graphic)
                
                elif command[0] == "dt":
                    if command[1] == "gr":
                        graphic = True
                        nom_personnage = command[2]
                    else:
                        nom_personnage = command[1]
                    analyse.print_character_detail(characters, scenes, nom_personnage, graphic)
                
                elif command[0] == "tg":
                    list_characters = command[1:]
                    analyse.print_characters_together(scenes, list_characters)
                
                elif command[0] == "pt":
                    file_type = command[1]
                    if data.piece_exists(piece):
                        print_csv(piece, file_type)
                    else:
                        print(f"Aucune donnée n'est associée à la pièce '{piece}'")
                        
                else:
                    print("Commande inconnue. Veuillez réessayer")
    except:
        print("Commande mal formée. Veuillez réessayer")
        main(piece, characters, scenes)

if __name__ == "__main__":
    main(None, None, None)