from typing import List, Tuple

import read
import analyse
import data
import modify
import editor
import stage
import type
import load


def usage() -> None:
    """ Affiche les commandes possibles
    """
    print("\n  h - Afficher cette aide")
    
    print("\n  rd <piece> - Lire un fichier texte pour collecter des données et les stocker dans des fichiers csv")
    
    print("\n  ls - Afficher la liste des pièces disponibles, dont on peut analyser les données")
    print("  ld <dossier> - Charger les données présentes dans un dossier")
    print("  rm <dossier> - Supprimer les données présentes dans un dossier")
    
    print("\n  sc [gr] [ac] - Afficher les scènes et les personnages présents (gr pour afficher un graphique)")
    print("  nb [<nombre>] - Afficher les scènes avec un certain nombre de personnages")
    print("  ch [gr] [ac] - Afficher les personnages avec leur nombre de répliques et de mots (gr pour afficher un graphique)")
    print("  dt [ac] <nom> - Afficher les informations détaillées d'un personnage spécifique")
    print("  tg [ac] <perso1> <perso2> <...> - Afficher les scènes en commun pour des personnages")
    print("  pt sc|ch|ac - Afficher le contenu du fichier csv pour les scènes (sc), les personnages (ch), ou les comédien·es (ac)")
        
    print("\n  rn [ac] <perso> <nouveau_nom> - Renommer un personnage")
    print("  ad <perso> <scene1> <scene2> <...> - Ajouter un personnage dans des scènes")
    print("  mg <perso> <perso1> <perso2> <...> - Fusionner un personnage dans un ou plusieurs personnages")
    print("  sp <perso> <repliques> <mot> - Ajouter un certain nombre de répliques et de mots à un personnage")
    print("  dl [ac] <perso> - Supprimer un personnage")
    
    print("\n  Le paramètre 'ac' sur les commandes précédentes permet d'afficher ou de modifier des informations concernant les comédien·es plutôt que les personnages")
    
    print("\n  lk <comedien> <perso1> <perso2> <...> - Lier un comédien à un ou plusieurs personnages")
    print("  ul <comedien> <perso> - Supprimer le lien entre un comédien et un personnage")
    
    print("\n  Entrer une commande sans argument alors qu'elle nécessite un personnage et/ou une scène ouvrira un éditeur pour choisir les arguments")
    
    print("\n  q - Quitter")


def update(piece: str) -> Tuple[List[type.Character], List[type.Scene], List[type.Actor]]:
    """ Met à jour les informations collectées dans les fichiers CSV

    Args:
        piece (str): nom de la pièce

    Returns:
        Tuple[List[type.Character], List[type.Scene], List[type.Actor], List[type.Stage]]: informations sur la pièce
    """
    
    characters = load.get_characters(piece)
    scenes = load.get_scenes(piece)
    actors = load.get_actors(piece, characters)
    
    return characters, scenes, actors
    
    
def main(piece, characters, scenes, actors) -> None:
    """ Fonction principale qui gère les commandes
    """
    
    try:
        while True:
            graphic = False
            ac = False
            
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
                        characters, scenes, actors = update(piece)                    
                        print(f"Les données de '{piece}' ont été chargées avec succès")
                    else:
                        print(f"Aucune donnée ne correspond à la pièce '{piece}'")
                        
                case ["rm", piece_to_delete]:
                    data.delete_piece(piece_to_delete)
                    
                case _:
                    if not characters or not scenes:
                        print("Vous devez d'abord charger les données d'une pièce")
                    else:
                        match command:
                            
                            case ["sc", *args]:
                                if "gr" in args:
                                    graphic = True
                                if "ac" in args:
                                    ac = True
                                analyse.print_scenes(scenes, graphic, ac)
                            
                            case ["nb", *args]:
                                if args:
                                    analyse.print_scenes_with_nb(scenes, int(args[0]))
                                else:
                                    analyse.print_nb_of_characters_in_scenes(scenes, len(characters))
                            
                            case ["ch", *args]:
                                to_show = characters
                                if "gr" in args:
                                    graphic = True
                                if "ac" in args:
                                    to_show = actors
                                analyse.print_characters(to_show, graphic)
                            
                            case ["dt", *args]:
                                if args:
                                    if args[0] == "ac":
                                        to_show = actors
                                        ac = True
                                        name = " ".join(args[1:])
                                    else:
                                        to_show = characters
                                        name = " ".join(args)
                                else:
                                    name = editor.dt(characters)                
                                analyse.print_character_detail(to_show, scenes, name, ac)
                                
                            case ["tg", *args]:
                                if args:
                                    if args[0] == "ac":
                                        ac = True
                                        list_characters = args[1:]
                                    else:
                                        list_characters = args
                                else:
                                    list_characters = editor.tg(characters)
                                analyse.print_characters_together(scenes, list_characters, ac)
                                
                            case ["pt", file_type]:
                                if data.piece_exists(piece):
                                    data.print_csv(piece, file_type)
                                else:
                                    print(f"Aucune donnée n'est associée à la pièce '{piece}'")
                            
                            case ["rn", *args]:
                                if args:
                                    if args[0] == "ac":
                                        ac = True
                                        old_name = args[1]
                                        new_name = args[2]
                                    else:
                                        old_name = args[0]
                                        new_name = args[1]
                                else:
                                    old_name, new_name = editor.rn(characters)
                                    
                                modify.rename_character(piece, old_name, new_name, ac)
                                characters, scenes, actors = update(piece)
                                
                                print("Le changement de nom a été opéré avec succès")
                            
                            case ["ad", *args]:
                                if args:
                                    new_character = args[0]
                                    list_scenes = args[1:]
                                else:
                                    new_character, list_scenes = editor.ad(scenes, characters)
                    
                                modify.add_character(piece, new_character, list_scenes)
                                characters, scenes, actors = update(piece)
                                
                                print("Le personnage a bien été ajouté")
                            
                            case ["mg", *args]:
                                if args:
                                    source_character = args[0]
                                    destination_characters = args[1:]
                                else:
                                    source_character, destination_characters = editor.mg(characters)
                        
                                modify.merge_characters(piece, source_character, destination_characters)
                                
                                characters, scenes, actors = update(piece)
                                
                                print("Les personnages ont bien été fusionnés")
                            
                            case ["sp", *args]:
                                if args:
                                    character_name = args[0]
                                    nb_lines_to_add = int(args[1])
                                    nb_words_to_add = int(args[2])
                                else:
                                    character_name, nb_lines_to_add, nb_words_to_add = editor.sp(characters)
                                
                                modify.add_lines_and_words(piece, character_name, nb_lines_to_add, nb_words_to_add)
                                
                                characters, scenes, actors = update(piece)
                                
                                print("Les modifications ont été réalisées avec succès")
                            
                            case ["dl", *args]:
                                if args:
                                    if args[0] == "ac":
                                        ac = True
                                        character_names = list(args[1:])
                                    else:
                                        character_names = list(args)
                                else:
                                    character_names = editor.dl(characters)
                                
                                modify.delete_character(piece, character_names, ac)
                                
                                characters, scenes, actors = update(piece)
                                
                                print("Le·s personnage·s a/ont bien été supprimé·s")
                                        
                            case ["lk", *args]:
                                if args:
                                    actor_name = args[0]
                                    character_names = args[1:]
                                else:
                                    editor.lk()
                                
                                stage.link(piece, actor_name, character_names)
                                
                                characters, scenes, actors = update(piece)
                                
                                print("Le·a comédien·ne a bien été lié·e au·x personnage·s")
                            
                            case ["ul", *args]:
                                if args:
                                    actor_name = args[0]
                                    character_name = args[1]
                                else:
                                    editor.ul()
                                
                                stage.unlink(piece, actor_name, character_name)
                                
                                characters, scenes, actors = update(piece)
                                
                                print("Le lien entre le·a comédien·ne et le personnage a bien été retiré")
                    
                            case _:
                                print("Commande inconnue")
    except:
        print("Commande mal formée")
        main(piece, characters, scenes, actors)

if __name__ == "__main__":
    main(None, None, None, None)