from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from bm25 import search, titles_global, docs_global, bm25_index
from stance import predict_stance
from gemini import generate_summary

app = FastAPI(title="TruthScope RAG API")

# Beed ti set up cors lol
origins = [
    "http://localhost:3000",  # allow requests from front
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow http
    allow_headers=["*"],  # allow headers
)

# Define color mapping for stance results.
# STANCE_COLORS = {
#     "agree": "green",
#     "disagree": "red",
#     "discuss": "orange",
#     "unrelated": "orange"
# }

STANCE_COLORS = {
    "agree": "red",
    "disagree": "green",
    "discuss": "black",
    "unrelated": "gray"
}

# Build classes for data transfer
class QueryRequest(BaseModel):
    query: str

class ArticleResult(BaseModel):
    title: str
    content: str
    stance: str
    color: str

class QueryResponse(BaseModel):
    articles: List[ArticleResult]
    summary: str

# Post requests
@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    # Call bm25 base on wiki articles
    articles = search(request.query, titles_global, docs_global, bm25_index, top_n=5)
    
    # Run stance detection
    for article in articles:
        stance = predict_stance(request.query, article["content"])
        article["stance"] = stance
        article["color"] = STANCE_COLORS.get(stance, "gray")
    
    # Build system prompt and get response from Gemini
    summary = generate_summary(request.query, articles)
    
    # Return res
    # The response model expects article results obj
    article_results = [
        {
            "title": art["title"],
            "content": art["content"],
            "stance": art["stance"],
            "color": art["color"]
        }
        for art in articles
    ]
    return {"articles": article_results, "summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
