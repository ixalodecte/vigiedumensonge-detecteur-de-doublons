# Détecteur de doublons pour le site vigiedumensonge.fr

Script conçu pour détecter les doublons sur le site Vigie du Mensonge. Il utilise un algorithme simple qui repère les mots clés importants d’un texte (TF-IDF), puis compare ce texte aux autres à l’aide d’une mesure de similarité.

## Installation
Installer les packages nécessaires:
```bash
git clone https://github.com/ixalodecte/vigiedumensonge-detecteur-de-doublons
cd vigiedumensonge-detecteur-de-doublons
pip install -r requirements.txt
```
il faut ensuite télécharger les packages suivants pour nltk. Pour cela, dans un terminal python:
 
```python
import nltk
nltk.download('stopwords')  # Contient les stopwords français (taille : 36 ko)
nltk.download('punkt_tab')  # Permet la tokenisation du texte (extraction des mots) (taille : 4 Mo)
```

## Utilisation

### Télécharger les données
Pour télécharger les posts depuis le site vigiedumensonge :
```bash
python3 download_posts.py
```
le script va charger les posts, les parser et les stocker dans le dossier "data/".

### Trouver les posts similaires
Le script ```similar_post.py``` va chercher les n posts les plus similaires à un post donné parmi les posts présents dans le dossier "data". Il faut donner l'id du mensonge, qui correspond au nombre dans l'url sur le site vigiedumensonge. Exemple d'utilisation:
```
$ python3 similar_post.py 6 --top 7

Post de référence : 
 # mensonge_6.json      | "Macron et le Chlordécone"

Posts similaires :
 - mensonge_100.json    | similarité=0.6956    | "[Doublon] Chlordécone : l’Elysée plaide le « malentendu » après la déclaration polémique de Macron"
 - mensonge_61.json     | similarité=0.6418    | "L'Elysée ment sur la déclaration d'Emmanuel Macron sur le chlordécone"
 - mensonge_87.json     | similarité=0.5986    | "Macron n'a jamais dit que le chlordécone n'est pas cancérigène."
 - mensonge_10.json     | similarité=0.5773    | "[DOUBLON] Macron : le chlordécone n'est pas cancérigène"
 - mensonge_9.json      | similarité=0.5656    | "L'élysée ment sur les propos de Emmanuel Macron sur le chlordécone"
 - mensonge_80.json     | similarité=0.1081    | "20 décembre 2023 - “Ce n’est pas vrai que le texte comporte des dispositions qui sont de nature Rassemblement national.”"
 - mensonge_127.json    | similarité=0.0932    | "Macron et la presse, des voeux bien vite oubliés"

Temps d'exécution : 0.1507
```

### Créer des groupes de post similaire (clustering)
Le script ```cluster_posts.py``` réalise un clustering des posts, pour regrouper les posts similaires grace à l'algorithme DBSCAN. Un paramètre ```--sim``` contrôle la similarité minimale entre deux posts pour qu'ils soient considérés comme des doublons. Exemple:

```
$ python3 cluster_posts.py --stem --sim 0.5

Nombre de clusters détectés : 13

--- Cluster 1 ---
- Mensonge 10   |  [DOUBLON] Macron : le chlordécone n'est pas cancérigène
- Mensonge 100  |  [Doublon] Chlordécone : l’Elysée plaide le « malentendu » après la déclaration polémique de Macron
- Mensonge 6    |  Macron et le Chlordécone
- Mensonge 61   |  L'Elysée ment sur la déclaration d'Emmanuel Macron sur le chlordécone
- Mensonge 87   |  Macron n'a jamais dit que le chlordécone n'est pas cancérigène.
- Mensonge 9    |  L'élysée ment sur les propos de Emmanuel Macron sur le chlordécone

--- Cluster 2 ---
- Mensonge 103  |  Stanislas Guerini et l'affaire Jérome Peyrat
- Mensonge 105  |  (EDIT : MENSONGE DISCUTABLE  + DOUBLON) Stanislas Guérini défend un agresseur sexuel reconnu par la justice

--- Cluster 3 ---
- Mensonge 111  |  Amélie Oudéa-Castéra et Stanislas
- Mensonge 42   |  Amélie Oudéa-Castéra sur le choix de scolarisation de ses enfants à Stanislas
- Mensonge 60   |  Amélie Oudéa-Castera - Société - Absence des professeurs de ses enfants dans le public - 13/01/2024
...
```
