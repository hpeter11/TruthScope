from datasets import load_dataset
import nltk
from nltk.tokenize import word_tokenize
from rank_bm25 import BM25Okapi

# Download NLTK's tokenizer models
nltk.download('punkt')
nltk.download('punkt_tab')

# Step 1: Load a subset of the Wikipedia dataset for testing.
dataset = load_dataset("wikipedia", "20220301.en", split="train[:1000]")

# Step 2: Extract the 'text' field from each document.
docs = [example["text"] for example in dataset]

# Step 3: Tokenize each document (lowercasing for consistency).
tokenized_docs = [word_tokenize(doc.lower()) for doc in docs]

# Step 4: Create a BM25 index.
bm25 = BM25Okapi(tokenized_docs)

# Step 5: Define and tokenize a query.
query = "Did the father of economics like apples?"
tokenized_query = word_tokenize(query.lower())

# Retrieve the top 5 documents.
top_n_docs = bm25.get_top_n(tokenized_query, docs, n=5)

# Display the results.
print("Top 5 documents:")
for i, doc in enumerate(top_n_docs):
    print(f"Rank {i+1}: {doc[:500]}...\n")