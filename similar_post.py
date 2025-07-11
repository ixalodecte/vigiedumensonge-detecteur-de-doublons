import os
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#import spacy
import re
import time
from utils import preprocess, load_post



def find_similar_posts(posts, index, top_n=5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(posts)

    target_vector = tfidf_matrix[index]
    similarities = cosine_similarity(target_vector, tfidf_matrix)[0]

    similar_indices = similarities.argsort()[::-1]  # ordre décroissant
    # Exclure le post lui-même (même index)
    similar_indices = [i for i in similar_indices if i != index]

    results = [(i, similarities[i]) for i in similar_indices[:top_n]]
    return results


def main():
    parser = argparse.ArgumentParser(description="Trouver les posts similaires")
    parser.add_argument("index", type=int, help="Index du post de référence (ex: 1)")
    parser.add_argument("--folder", type=str, default="data", help="Dossier contenant les fichiers JSON")
    parser.add_argument("--top", type=int, default=5, help="Nombre de posts similaires à afficher")
    parser.add_argument("--stem", action="store_true", help="Activer le stemming avec FrenchStemmer de nltk")

    args = parser.parse_args()
    folder = args.folder
    index = args.index
    top = args.top
    stem = args.stem

    # Charge toutes les données depuis folder.
    start = time.time()
    posts = []
    filenames = []
    titles = []
    idxs = []
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".json"):
            idx_path = int(fname[:-5].split("_")[1])
            path = os.path.join(folder, fname)
            post_text, titre = load_post(path, stem)
            posts.append(post_text)
            filenames.append(fname)
            titles.append(titre)
            idxs.append(idx_path)

    # Prend l'index dans la liste du post de reference
    index = idxs.index(index)

    # Trouve le top n des posts similaires
    results = find_similar_posts(posts, index, top)
    end = time.time()

    print(f"Post de référence : \n # {filenames[index]}\t| \"{titles[index]}\"")
    print()
    print("Posts similaires :")
    for i, score in results:
        print(f" - {filenames[i]}\t| similarité={score:.4f}    | \"{titles[i]}\"")
    print()
    print(f"Temps d'exécution : {(end-start):.4f}")


if __name__ == "__main__":
    main()
