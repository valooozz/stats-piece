import os
import shutil

import read
import analyse
import data


def usage() -> None:
    """ Affiche les commandes possibles
    """
    print("\nh - Afficher cette aide")
    
    print("\nrd [fichier] - Lire un fichier texte pour collecter des données et les stockers dans des fichiers csv")
    print("ls - Afficher la liste des pièces disponibles, dont on peut analyser les données")
    print("ld [dossier] - Charger les données présentes dans un dossier")
    print("dl [dossier] - Supprimer les données présentes dans un dossier")
    
    print("\nsc - Afficher les scènes et les personnages présents")
    print("ch - Afficher les personnages avec leur nombre de répliques et de mots")
    print("ch [nom_personnage] - Afficher les informations détaillées d'un personnage spécifique")
    
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
    

def main() -> None:
    """ Fonction principale qui gère les commandes
    """
    
    characters = None
    scenes = None
    
    while True:        
        command = input("\n > ").strip()

        if command == "h":
            usage()
            
        elif command == "q":
            print("Au revoir !\n")
            break
        
        elif command.startswith("rd "):
            file_name = command[3:]
            read.read(file_name)
        
        elif command == "ls":
            data.print_pieces()
            
        elif command.startswith("ld "):
            piece = command[3:]
            if data.piece_exists(piece):
                characters = analyse.read_characters(f"{piece}/characters.csv")
                scenes = analyse.read_scenes(f"{piece}/scenes.csv")
                print(f"Les données de '{piece}' ont été chargées avec succès")
            else:
                print(f"Aucune donnée ne correspond à la pièce '{piece}'")
        
        elif command.startswith("dl "):
            piece = command[3:]
            delete_piece(piece)
            
        else:
            if not characters or not scenes:
                print("Vous devez d'abord charger les données d'une pièce")
                
            elif command == "sc":
                analyse.print_scenes(scenes)
                
            elif command.startswith("ch "):
                nom_personnage = command[3:].strip()
                analyse.print_character_detail(characters, scenes, nom_personnage)
                
            elif command == "ch":
                analyse.print_characters(characters)
                
            else:
                print("Commande inconnue. Veuillez réessayer.")


if __name__ == "__main__":
    main()