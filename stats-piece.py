import os
import shutil

import read
import analyse
import data
import modify
import editor


def usage() -> None:
    """ Affiche les commandes possibles
    """
    print("\n  h - Afficher cette aide")
    
    print("\n  rd <piece> - Lire un fichier texte pour collecter des données et les stocker dans des fichiers csv")
    
    print("\n  ls - Afficher la liste des pièces disponibles, dont on peut analyser les données")
    print("  ld <dossier> - Charger les données présentes dans un dossier")
    print("  rm <dossier> - Supprimer les données présentes dans un dossier")
    
    print("\n  sc [gr] - Afficher les scènes et les personnages présents (gr pour afficher un graphique)")
    print("  nb <nombre> - Afficher les scènes avec un certain nombre de personnages")
    print("  ch [gr] - Afficher les personnages avec leur nombre de répliques et de mots (gr pour afficher un graphique)")
    print("  dt <nom_personnage> - Afficher les informations détaillées d'un personnage spécifique")
    print("  tg <perso1> <perso2> <...> - Afficher les scènes en commun pour des personnages")
    print("  pt sc|ch - Afficher le contenu du fichier csv pour les scènes (sc) ou les personnages (ch)")
    
    print("\n  rn <perso> <nouveau_nom> - Renommer un personnage")
    print("  ad <perso> <scene1> <scene2> <...> - Ajouter un personnage dans des scènes")
    print("  mg <perso1> <perso2> - Fusionner le perso1 dans le perso2")
    
    print("\n  Entrer une commande sans argument alors qu'elle nécessite un personnage et/ou une scène ouvrira un éditeur pour choisir les arguments")
    
    print("\n  q - Quitter")


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
            
            match command:
                
                case ["h"]:
                    usage()
                                        
                case ["q"]:
                    print("Au revoir !\n")
                    break
                
                case ["rd", piece_name]:
                    read.read(piece_name)
                    
                case ["ls"]:
                    data.print_pieces()
                    
                case ["ld", piece]:
                    piece = command[1]
                    if data.piece_exists(piece):
                        characters = analyse.get_characters(f"{piece}/characters.csv")
                        scenes = analyse.get_scenes(f"{piece}/scenes.csv")
                        print(f"Les données de '{piece}' ont été chargées avec succès")
                    else:
                        print(f"Aucune donnée ne correspond à la pièce '{piece}'")
                        
                case ["rm", piece_to_delete]:
                    delete_piece(piece_to_delete)
                    
                case _:
                    if not characters or not scenes:
                        print("Vous devez d'abord charger les données d'une pièce")
                    else:
                        match command:
                            
                            case ["sc", *args]:
                                if args == ["gr"]:
                                    graphic = True
                                analyse.print_scenes(scenes, graphic)
                            
                            case ["nb", *args]:
                                if args:
                                    analyse.print_scenes_with_nb(scenes, int(args[0]))
                                else:
                                    analyse.print_nb_of_characters_in_scenes(scenes, len(characters))
                            
                            case ["ch", *args]:
                                if args == ["gr"]:
                                    graphic = True
                                analyse.print_characters(characters, graphic)
                            
                            case ["dt", *args]:
                                if args:
                                    character_name = " ".join(args)
                                else:
                                    character_name = editor.dt(characters)                
                                analyse.print_character_detail(characters, scenes, character_name)
                                
                            case ["tg", *args]:
                                if args:
                                    list_characters = args
                                else:
                                    list_characters = editor.tg(characters)
                                analyse.print_characters_together(scenes, list_characters)
                                
                            case ["pt", file_type]:
                                if data.piece_exists(piece):
                                    print_csv(piece, file_type)
                                else:
                                    print(f"Aucune donnée n'est associée à la pièce '{piece}'")
                            
                            case ["rn", *args]:
                                if args:
                                    old_name = args[0]
                                    new_name = args[1]
                                else:
                                    old_name, new_name = editor.rn(characters)
                                    
                                modify.rename_character(piece, old_name, new_name)
                                characters = analyse.get_characters(f"{piece}/characters.csv")
                                scenes = analyse.get_scenes(f"{piece}/scenes.csv")
                                
                                print("Le changement de nom a été opéré avec succès")
                            
                            case ["ad", *args]:
                                if args:
                                    new_character = args[0]
                                    list_scenes = args[1:]
                                else:
                                    new_character, list_scenes = editor.ad(scenes, characters)
                    
                                modify.add_character(piece, new_character, list_scenes)
                                characters = analyse.get_characters(f"{piece}/characters.csv")
                                scenes = analyse.get_scenes(f"{piece}/scenes.csv")
                                
                                print("Le personnage a bien été ajouté")
                            
                            case ["mg", *args]:
                                if args:
                                    source_character = args[0]
                                    destination_character = args[1]
                                else:
                                    source_character, destination_character = editor.mg(characters)
                        
                                modify.merge_characters(piece, source_character, destination_character)
                                
                                characters = analyse.get_characters(f"{piece}/characters.csv")
                                scenes = analyse.get_scenes(f"{piece}/scenes.csv")
                                
                                print("Les personnages ont bien été fusionnés")

                            case _:
                                print("Commande inconnue")
    except:
        print("Commande mal formée")
        main(piece, characters, scenes)

if __name__ == "__main__":
    main(None, None, None)