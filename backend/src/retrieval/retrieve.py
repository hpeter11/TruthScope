#!/usr/bin/env python3
import os
import nltk
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi

# Download NLTK's tokenizer data if not already present.
nltk.download('punkt')

# Directory where your local Wikipedia articles are stored.
ARTICLES_DIR = "wikipedia_top_1000"

# Lists to hold document contents and corresponding titles.
docs = []
titles = []

# Iterate over each text file in the directory.
for filename in sorted(os.listdir(ARTICLES_DIR)):
    if filename.endswith(".txt"):
        # Assume filenames are in the format: "001_Title.txt"
        parts = filename.split("_", 1)
        if len(parts) == 2:
            # Remove file extension from the title part.
            title = parts[1].rsplit(".", 1)[0]
        else:
            title = filename.rsplit(".", 1)[0]
        titles.append(title)
        
        filepath = os.path.join(ARTICLES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            docs.append(content)

# Tokenize each document (lowercase for consistency)
tokenized_docs = [word_tokenize(doc.lower()) for doc in docs]

# Create a BM25 index over the tokenized documents.
bm25 = BM25Okapi(tokenized_docs)

# Example query: change this to your desired search text.
query = "Who won super bowl LIX?"
tokenized_query = word_tokenize(query.lower())

# Get BM25 scores for every document.
scores = bm25.get_scores(tokenized_query)

# Sort the document indices by their BM25 scores in descending order.
sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

# Display the top 5 matching documents.
print("Top 5 matching documents:")
for rank, idx in enumerate(sorted_indices[:5], start=1):
    print(f"Rank {rank}: {titles[idx]} (Score: {scores[idx]:.2f})")
    print("Excerpt:")
    print(docs[idx][:500])  # Print the first 500 characters as an excerpt.
    print("-" * 80)
