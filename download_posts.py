import requests
import json
import os

from bs4 import BeautifulSoup

# On commence par supprimer tout ce qu'il y a dans data/
for fname in os.listdir("data"):
    if fname.split(".")[-1] == "json":
        os.remove("data/" + fname)

for i in range(200):  # Augmenter ce nombre s'il y a plus de mensonge sur le site
    url = f"https://vigiedumensonge.fr/e/{i}"

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Mensonge {i} : status {response.status_code}")
        continue
    response.raise_for_status()  # Lève une erreur si le téléchargement échoue

    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire le titre
    titre = soup.find("h1").get_text(strip=True)

    # Extraire la citation (le bloc <blockquote>)
    citation_elem = soup.find("blockquote")
    citation = citation_elem.get_text("\n", strip=True) if citation_elem else ""

    # Extraire les faits (élément <p> sous "Les faits")
    faits_title = soup.find("span", string="Les faits :")
    faits = faits_title.find_next("p").get_text("\n", strip=True) if faits_title else ""

    # Date d'ajout
    date_elem = soup.find(
        "p", string=lambda text: text and text.startswith("Ajouté le")
    )
    date_ajout = date_elem.get_text(strip=True) if date_elem else ""
    donnees = {
        "titre": titre,
        "date_ajout": date_ajout,
        "citation": citation,
        "faits": faits,
    }
    print(f" - {i} : {titre}")

    # Sauvegarde JSON
    with open(f"data/mensonge_{i}.json", "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=4)
    if 0:
        # Affichage
        print("=== TITRE ===")
        print(titre)
        print("\n=== DATE ===")
        print(date_ajout)
        print("\n=== CITATION ===")
        print(citation)
        print("\n=== FAITS ===")
        print(faits)
