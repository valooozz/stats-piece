from typing import List, Tuple

def rename(characters: List[str]) -> Tuple[str, str]:
    """ Éditeur de renommage de personnage

    Args:
        characters (List[str]): liste des personnages avec leurs informations

    Returns:
        Tuple[str, str]: ancien et nouveau nom
    """
    
    list_characters = [c["Character"] for c in characters]
    
    print("\n  >>>>> Éditeur de renommage <<<<<")
    print("\n  Liste des personnages :")
    for i in range(len(list_characters)):
        print(f"   {i} - {list_characters[i]}")
    
    print("\n  Personnage à renommer")
    old_name = list_characters[int(input("   >>> "))]
    
    print(f"\n  Nouveau nom pour {old_name}")
    new_name = input("   >>> ").strip()
    
    return old_name, new_name