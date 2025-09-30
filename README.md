## Stats Piece — Analyse de pièces de théâtre

Outil en ligne de commande pour lire des textes de pièces, extraire des statistiques (scènes, personnages, mots, répliques), et manipuler les données (ajouts, renommages, fusions) avec export CSV. Affichage tabulaire et graphiques optionnels.

### Prérequis
- Python 3.10+
- Dépendances Python:
  - `matplotlib` (graphes)
  - `prettytable` (tables)

Installation des dépendances :
```bash
pip install matplotlib prettytable
```

### Structure du projet
- `stats-piece.py`: boucle principale et interface CLI (commandes)
- `read.py`: lecture d’un fichier texte et extraction des stats
- `load.py`: chargement des CSV vers structures Python
- `analyse.py`: affichages (tables/graphes) des scènes/personnages/comédien·nes
- `modify.py`: modifications des CSV (ajout scène/perso, renommage, fusion, etc.)
- `stage.py`: liens comédien·ne ↔ personnages
- `editor.py`: éditeurs interactifs (prompts) quand arguments manquent
- `data.py`: gestion des pièces disponibles et affichage CSV bruts
- `type.py`: définitions d’entêtes CSV et types dict
- `utils.py`: chemins de fichiers, helpers
- `texts/`: fichiers sources des pièces au format texte (`<piece>.txt`)
- `<piece>/`: dossier généré contenant `scenes.csv`, `characters.csv`, `actors.csv`

### Flux de données
1) Source: `texts/<piece>.txt` (format simple: lignes de type `Nom: réplique`, didascalies = lignes sans `:`)
2) Extraction: `read.py` parcourt le texte et calcule par scène: répliques, didascalies, mots, personnages présents; par personnage: total répliques et mots
3) Écriture CSV: `read.py` → `<piece>/scenes.csv`, `<piece>/characters.csv`, et initialise `<piece>/actors.csv`
4) Chargement/Analyse: `load.py` lit les CSV; `analyse.py` affiche tableaux/graphes
5) Modifications: `modify.py` et `stage.py` mettent à jour les CSV

### Lancement
```bash
python stats-piece.py
```
Une invite s’affiche: `>`. Tapez une commande parmi celles ci-dessous.

### Commandes principales
- `h` — Afficher l’aide.

- `rd <piece>` — Lire `texts/<piece>.txt`, extraire les stats et écrire les CSV dans `<piece>/`.

- `ls` — Lister les pièces disponibles (détectées dans `data.txt`).

- `ld <dossier>` — Charger les données de la pièce (ex: `ld llg`). Nécessaire avant l’analyse/modification.

- `rm <dossier>` — Supprimer le dossier de données d’une pièce et l’entrée associée.

- `sc [gr] [ac]` — Afficher les scènes (actes, répliques, didascalies, mots, personnages/comédien·nes). `gr` pour un graphique; `ac` pour afficher côté comédien·nes.

- `nb [<nombre>]` — Afficher les scènes contenant exactement `<nombre>` personnages; sans argument, récap du nombre de scènes par effectif.

- `ch [gr] [ac]` — Afficher les personnages triés par mots (ou comédien·nes avec `ac`). `gr` pour graphique.

- `dt [ac] <nom>` — Détails pour un personnage (ou comédien·ne avec `ac`): répliques, mots, nb de scènes, coprésences.

- `tg [ac] <perso1> <perso2> <...>` — Scènes où ces personnages/comédien·nes sont ensemble. Sans arguments suffisants, ouvre un éditeur.

- `pt sc|ch|ac` — Afficher le contenu brut d’un CSV: scènes (`sc`), personnages (`ch`), comédien·nes (`ac`).

- `nw <nouvelle-scene> <repliques> <didascalies> <mots> <scene-suivante>` — Ajouter une scène avant `scene-suivante` (ou fin si omise). Sans arguments, ouvre l’éditeur.

- `rn [ac] <ancien_nom> <nouveau_nom>` — Renommer un personnage (ou comédien·ne avec `ac`). Sans arguments, ouvre l’éditeur.

- `ad <perso> <scene1> <scene2> ...` — Ajouter un personnage à des scènes (modifie `scenes.csv` et crée dans `characters.csv` si absent). Sans arguments, éditeur.

- `mg <source> <dest1> <dest2> ...` — Fusionner un personnage source dans un ou plusieurs personnages destination (transfert des stats et remplacements dans scènes).

- `sp <perso> <repliques> <mots>` — Ajouter des répliques et mots à un personnage.

- `dl [ac] <nom1> <nom2> ...` — Supprimer personnage(s) (ou comédien·ne(s) avec `ac`) des CSV. Sans arguments, éditeur.

- `lk <comedien> <perso1> <perso2> ...` — Lier un·e comédien·ne à un ou plusieurs personnages (écrit dans `actors.csv`).

- `ul <comedien> <perso>` — Retirer le lien comédien·ne ↔ personnage.

- `q` — Quitter.

Astuce : le modificateur `ac` bascule l’affichage ou l’action côté comédien·nes au lieu des personnages.

### Format des CSV
- `scenes.csv`: `SceneName,Lines,Didascalies,Words,Characters` (personnages séparés par `:`)
- `characters.csv`: `CharacterName,Lines,Words`
- `actors.csv`: `ActorName,CharactersPlayed` (personnages séparés par `:`)

### Exemple d’utilisation
1) Importer une pièce: déposer `texts/uds.txt`
2) Extraire: `rd uds`
3) Charger: `ld uds`
4) Analyser: `sc gr`, `ch`, `dt Ulysse`, `tg Ulysse Télémaque`
5) Modifier: `rn Ulysse Odysseus`, `ad NouveauPerso 1:2 1:3`, `mg PersoA PersoB`, `sp PersoB 3 45`
6) Lier comédien·ne: `lk "Jean Dupont" Odysseus Télémaque`

### Conseils & limites
- Les entêtes de scène doivent contenir « Acte » et « Scène » pour le découpage automatique.
- Une réplique est reconnue si la ligne contient `Nom : texte`.
- Les opérations modifient les CSV en place; pensez à versionner les données.

### Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.