# TruthScope
## Summarization & Fact-Checking Tool (Monorepo)

TruthScope is an early-stage project aimed at providing retrieval-augmented text summarization and fact-checking. The goal is to let users submit text or claims, retrieve relevant sources, summarize them, and determine whether the claim is supported or contradicted.

Status: Pre-Alpha / Under Development. No major functionality is implemented yet. Check back soon for updates!

### Table of Contents
1. Project Vision
2. Features (Planned)
3. Tech Stack
4. License

## Project Vision
- User-Focused: Provide a web interface where users can paste an article or claim and quickly see a concise summary and fact-verification result.
- Retrieval-Augmented: Integrate advanced retrieval systems (e.g., DeepSeek or BM25) to fetch relevant supporting or contradicting evidence.
- Modular Pipeline: Combine summarization with stance detection to offer a clear verdict (supports/refutes/uncertain).
- Scalable: Eventually handle larger datasets or multiple domains with minimal reconfiguration.

## Features (Planned)
- Article Summarization: Summaries from state-of-the-art models (T5, BART, or similar).
- Fact-Checking: Stance detection (supports/refutes) against relevant references.
- Toggleable Retrieval: Switch between DeepSeek-based retrieval or a simpler local method (BM25/Sentence-BERT).
- User-Friendly React Front End: Clean interface for uploading/pasting text and viewing results.
- Docker Integration: Simple setup with Docker Compose to run both the back end and front end.

## Tech Stack
- Backend: Python, PyTorch, Hugging Face Transformers, FastAPI or Flask (TBD).
- Frontend: React (JavaScript/TypeScript).
- Deployment: Docker & Docker Compose (planned).
- Licensing: Apache 2.0 (see License).

## License
This project is licensed under the terms of the Apache License 2.0. You are free to use, modify, and distribute this project in compliance with the license.