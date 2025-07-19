import json
import unicodedata
import string
import re

from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

# nltk.download('punkt_tab')
# nltk.download('stopwords')

stop_words = set(stopwords.words('french'))
stop_words.add("mensonge")
stop_words.add("edit")
stop_words.add("doublon")


punct_set = set(string.punctuation)
stop_words = set.union(punct_set, stop_words)

def preprocess(text, stem=False):
    text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    )  # Supprimer tout les accents pour réduire l'impact des fautes sur les accents
    text = text.lower()  # Passer tout en minuscule
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)  # Tokenization

    # Suppressions des stops words, et des token composé uniquement de punctuation
    tokens = [t for t in tokens if t not in stop_words]


    if stem:
        stemmer = FrenchStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    return " ".join(tokens)


def load_post(path, stem):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        # Utiliser "text" ou autre champ pertinent
        post_text = " ".join(
            [data.get("titre", ""), data.get("citation", ""), data.get("faits", "")]
        )
        post_text = preprocess(post_text, stem)
        return post_text, data.get("titre")
