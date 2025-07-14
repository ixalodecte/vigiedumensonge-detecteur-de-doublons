import os
import json
import argparse
import time
import numpy as np
from utils import preprocess, load_post

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from sklearn.cluster import DBSCAN


def cluster_posts(posts, stem=False, eps=0.5, min_samples=1):
    texts = [p["content"] for p in posts]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    # Clustering DBSCAN en utilisant la similarité cosinus
    model = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine")
    labels = model.fit_predict(X)

    # On compte le nombre de clusters (uniquement ceux qui contienne au moins deux elt)
    u, c = np.unique(labels, return_counts=True)
    n_clusters = np.sum(c > 1)
    print(f"Nombre de clusters détectés : {n_clusters}")

    clusters = {}
    for idx, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(posts[idx])

    return clusters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--folder", default="data", help="Dossier contenant les fichiers JSON"
    )
    parser.add_argument(
        "--sim",
        type=float,
        default=0.5,
        help="similarité minimal pour l'ajout d'un post dans un cluster. Compris entre 0 et 1",
    )
    parser.add_argument("--stem", action="store_true")
    args = parser.parse_args()

    # Charge les données
    start = time.time()
    posts = []
    filenames = []
    titles = []
    idxs = []
    for fname in sorted(os.listdir(args.folder)):
        if fname.endswith(".json"):
            idx_path = int(fname[:-5].split("_")[1])
            path = os.path.join(args.folder, fname)
            post_text, titre = load_post(path, args.stem)
            posts.append(
                {"title": titre, "fname": fname, "content": post_text, "idx": idx_path}
            )

    # Clustering, puis affichage
    clusters = cluster_posts(posts, stem=args.stem, eps=1 - args.sim)
    end = time.time()
    i = 1
    for label, posts in clusters.items():
        if len(posts) > 1 and label != -1:
            cluster_name = f"Cluster {i}"
            print(f"\n--- {cluster_name} ---")
            for post in posts:
                print(f"- Mensonge {post['idx']} \t|  {post['title']}")
            i += 1
    print(f"Temps de calcul : {(end-start):.4f}")


if __name__ == "__main__":
    main()
