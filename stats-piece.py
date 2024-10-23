import read
import analyse

def usage() -> None:
    """ Affiche les commandes possibles
    """
    print("\nh - Afficher cette aide")
    
    print("\nrd [fichier] - Lire un fichier texte pour collecter des données et les stockers dans des fichiers csv")
    print("ld [dossier] - Charger les données présentes dans un dossier")
    
    print("\nsc - Afficher les scènes et les personnages présents")
    print("ch - Afficher les personnages avec leur nombre de répliques et de mots")
    print("ch [nom_personnage] - Afficher les informations détaillées d'un personnage spécifique")
    
    print("\nq - Quitter")
    

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
            print("\nAu revoir !")
            break
        elif command.startswith("rd "):
            file_name = command[3:]
            read.read(file_name)
        elif command.startswith("ld "):
            dir_name = command[3:]
            characters = analyse.lire_characters(f"{dir_name}/characters.csv")
            scenes = analyse.lire_scenes(f"{dir_name}/scenes.csv")
        else:
            if not characters or not scenes:
                print("Vous devez d'abord charger les données d'une pièce.")
            elif command == "sc":
                analyse.afficher_scenes(scenes)
            elif command.startswith("ch "):
                nom_personnage = command[3:].strip()
                analyse.afficher_details_personnage(characters, scenes, nom_personnage)
            elif command == "ch":
                analyse.afficher_characters(characters)
            else:
                print("\nCommande inconnue. Veuillez réessayer.")

if __name__ == "__main__":
    main()