import os
import nltk
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

ARTICLES_DIR = "wikipedia_top_1000"

def load_articles():
    """
    Load the Wikipedia articles from articles dir
    """
    titles = []
    docs = []
    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if filename.endswith(".txt"):
            parts = filename.split("_", 1)
            if len(parts) == 2:
                title = parts[1].rsplit(".", 1)[0]
            else:
                title = filename.rsplit(".", 1)[0]
            titles.append(title)
            filepath = os.path.join(ARTICLES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                docs.append(content)
    return titles, docs

def build_index(docs):
    """
    Tokenize docs and build bm25 index (basic)
    """
    tokenized_docs = [word_tokenize(doc.lower()) for doc in docs]
    bm25 = BM25Okapi(tokenized_docs)
    return bm25

def search(query, titles, docs, bm25, top_n=5):
    """
    Use query with bm25 to return top n docs
    For now, n=5
    Returns list of dicts
    """
    tokenized_query = word_tokenize(query.lower())
    scores = bm25.get_scores(tokenized_query)
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    results = []
    for idx in sorted_indices[:top_n]:
        results.append({
            "title": titles[idx],
            "content": docs[idx]
        })
    return results

# On module load, build index
titles_global, docs_global = load_articles()
if not docs_global:
    raise ValueError("No articles found in the 'wikipedia_top_1000' directory. Please ensure it contains .txt files.")
bm25_index = build_index(docs_global)
