DATA_FILE = "data.txt"

def add_piece(new_piece: str) -> None:
    """ Ajoute une pièce au fichier des pièces lues

    Args:
        new_piece (str): nom de la pièce
    """
    
    if not piece_exists(new_piece):    
        with open(DATA_FILE, mode='a', encoding='utf-8') as file:
            file.write(new_piece)


def print_pieces() -> None:
    """ Affiche la liste des pièces déjà lues par le système
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            print("\nListe des pièces disponibles :")
            for line in file:
                print(f"- {line}")
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
        with open(DATA_FILE, mode='w', encoding='utf-8') as fichier:
            fichier.writelines(lignes_filtrees)

    except Exception as e:
        print(f"Erreur lors de la suppression de {piece} dans le fichier '{DATA_FILE}': {e}")