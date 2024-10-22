import csv
from typing import List, Dict, Tuple

# Fonction pour lire les données des personnages depuis le fichier CSV
def lire_characters(fichier: str) -> List[Dict[str, int]]:
    characters = []
    with open(fichier, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            characters.append({
                'Character': row['Character'],
                'Total lines': int(row['Total lines']),
                'Total Words': int(row['Total Words'])
            })
    return characters

# Fonction pour lire les données des scènes depuis le fichier CSV
def lire_scenes(fichier: str) -> List[Dict[str, str]]:
    scenes = []
    with open(fichier, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            scenes.append({
                'Scene': row['Scene'],
                'Characters': row['Characters']
            })
    return scenes

# Fonction pour afficher les scènes et les personnages présents
def afficher_scenes(scenes: List[Dict[str, str]]) -> None:
    acte_actuel = None
    for scene in scenes:
        acte, numero_scene = scene['Scene'].split(':')
        if acte != acte_actuel:
            acte_actuel = acte
            print(f"=== Acte {acte} ===")
        personnages = scene['Characters'].split(':')
        personnages_formates = ', '.join(sorted(personnage for personnage in personnages if personnage))
        print(f"Scène {numero_scene} : {personnages_formates}")

# Fonction pour afficher les personnages triés par nombre de mots décroissant
def afficher_characters(characters: List[Dict[str, int]]) -> None:
    characters_sorted = sorted(characters, key=lambda x: x['Total Words'], reverse=True)
    for character in characters_sorted:
        print(f"- {character['Character']}, Total lines: {character['Répliques']}, Total Words: {character['Mots']}")
        
        
# Fonction pour afficher les informations détaillées d'un personnage spécifique
def afficher_details_personnage(characters: List[Dict[str, int]], scenes: List[Dict[str, str]], nom_personnage: str) -> None:
    # Rechercher le personnage dans la liste des personnages
    personnage = next((c for c in characters if c['Character'] == nom_personnage), None)
    if personnage is None:
        print(f"\nPersonnage '{nom_personnage}' non trouvé.")
        return

    # Afficher les informations de base du personnage
    print(f"\n=== {personnage['Character']}===\nRépliques : {personnage['Total lines']}\nMots : {personnage['Total Words']}")

    # Rechercher les scènes où le personnage est présent
    scenes_personnage = [scene for scene in scenes if nom_personnage in scene['Characters'].split(':')]
    if not scenes_personnage:
        print(f"Le personnage '{nom_personnage}' n'est présent dans aucune scène.")
        return

    print(f"\nScènes où {nom_personnage} est présent:")
    acte_actuel = None
    for scene in scenes_personnage:
        acte, numero_scene = scene['Scene'].split(':')
        if acte != acte_actuel:
            acte_actuel = acte
            print(f"=== Acte {acte} ===")
        acte, numero_scene = scene['Scene'].split(':')
        personnages = scene['Characters'].split(':')
        personnages_formates = ', '.join(sorted(personnage for personnage in personnages if personnage and personnage != nom_personnage))
        print(f"Scène {numero_scene} avec : {personnages_formates}")

    # Rechercher les autres personnages présents dans les scènes avec ce personnage
    autres_personnages = set()
    for scene in scenes_personnage:
        personnages = scene['Characters'].split(':')
        autres_personnages.update(personnage for personnage in personnages if personnage and personnage != nom_personnage)

    print(f"\nPersonnages sur scène avec {nom_personnage}:")
    print(', '.join(sorted(autres_personnages)))

# Fonction principale pour afficher le menu et gérer les commandes
def main() -> None:
    characters = lire_characters('test/characters.csv')
    scenes = lire_scenes('test/scenes.csv')

    while True:
        print("\nMenu:")
        print("sc - Afficher les scènes et les personnages présents")
        print("ch - Afficher les personnages avec leur nombre de répliques et de mots")
        print("ch [nom_personnage] - Afficher les informations détaillées d'un personnage spécifique")
        print("q - Quitter")
        commande = input("Entrez une commande: ").strip()

        if commande == "sc":
            afficher_scenes(scenes)
        elif commande.startswith("ch "):
            nom_personnage = commande[3:].strip()
            afficher_details_personnage(characters, scenes, nom_personnage)
        elif commande == "ch":
            afficher_characters(characters)
        elif commande == "q":
            print("\nAu revoir !")
            break
        else:
            print("\nCommande inconnue. Veuillez réessayer.")

if __name__ == "__main__":
    main()