from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from bm25 import search, titles_global, docs_global, bm25_index
from stance import predict_stance
from gemini import generate_summary

app = FastAPI(title="TruthScope RAG API")

# Define color mapping for stance results.
STANCE_COLORS = {
    "agree": "green",
    "disagree": "red",
    "discuss": "orange",
    "unrelated": "orange"
}

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

@app.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    # 1. BM25 Search (Section 2)
    articles = search(request.query, titles_global, docs_global, bm25_index, top_n=5)
    
    # 2. For each article, run stance detection (Section 3)
    for article in articles:
        stance = predict_stance(request.query, article["content"])
        article["stance"] = stance
        article["color"] = STANCE_COLORS.get(stance, "gray")
    
    # 3. Build a Gemini system prompt (Section 4) and get a summary
    summary = generate_summary(request.query, articles)
    
    # 4. Return the results
    # The response model expects a list of ArticleResult objects.
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
