import os
import shutil

DATA_FILE = "data.txt"

def add_piece(new_piece: str) -> None:
    """ Ajoute une pièce au fichier des pièces lues

    Args:
        new_piece (str): nom de la pièce
    """
    
    if not piece_exists(new_piece):    
        with open(DATA_FILE, mode='a', newline="", encoding='utf-8') as file:
            file.write(new_piece + "\n")


def print_pieces() -> None:
    """ Affiche la liste des pièces déjà lues par le système
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            print("\nListe des pièces disponibles :")
            for line in file:
                print(f"- {line}", end="")
        print()
    except:
        print("\nAucune pièce n'a encore été lue par le système")
        

def piece_exists(piece: str) -> bool:
    """ Vérifie que des données associées à une pièce sont disponibles

    Args:
        piece (str): nom de la pièce

    Returns:
        bool: retourne True si la pièce a été trouvée
    """
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if piece == line.strip():
                    return True
    except:
        print("\nAucune pièce n'a encore été lue par le système")
    
    return False
                
                
def remove_piece(piece: str) -> None:
    """ Retirer une pièce de la liste des pièces disponibles

    Args:
        piece (str): nom de la pièce
    """
    try:
        # Lit le contenu du fichier
        with open(DATA_FILE, mode='r', encoding='utf-8') as fichier:
            lignes = fichier.readlines()

        # Filtre les lignes pour exclure celle qui correspond à la pièce à retirer
        lignes_filtrees = [ligne for ligne in lignes if ligne.strip() != piece]

        # Écrit les lignes restantes dans le fichier
        with open(DATA_FILE, mode='w', newline="", encoding='utf-8') as fichier:
            fichier.writelines(lignes_filtrees)

    except Exception as e:
        print(f"Erreur lors de la suppression de {piece} dans le fichier '{DATA_FILE}': {e}")


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
    elif file_type == "ac":
        file_name += "actors.csv"
    else:
        print("Veuillez entrer 'sc', 'ch', ou 'ac' pour spécifier quel fichier afficher")
        return
    
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            print(line, end="")


def delete_piece(piece: str) -> None:
    """ Supprime toutes les données associées à une pièce lue

    Args:
        piece (str): nom de la pièce
    """
    
    if os.path.exists(piece) and os.path.isdir(piece):
        shutil.rmtree(piece)
        remove_piece(piece)
        print(f"Les données associées à la pièce '{piece}' ont été supprimées avec succès")
    else:
        print(f"Le dossier '{piece}' n'existe pas")