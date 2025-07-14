import json
import unicodedata
import string

from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords

# nltk.download('punkt_tab')
# nltk.download('stopwords')


def preprocess(text, stem=False):
    text = (
        unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    )  # Supprimer tout les accents pour réduire l'impact des fautes sur les accents
    tokens = word_tokenize(text, language="french")  # Tokenization
    tokens = [token.lower() for token in tokens]  # Passer tout en minuscule

    # Suppressions des stops words, et des token composé uniquement de punctuation
    stop_words = set(stopwords.words("french"))
    stop_words.add("mensonge")
    stop_words.add("edit")
    stop_words.add("doublon")
    tokens = [
        t
        for t in tokens
        if t not in stop_words and not all(c in string.punctuation for c in t)
    ]

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
