# TruthScope

TruthScope is a Dockerized fact-checking tool that leverages a small collection of the most viewed Wikipedia articles (from February 10th, 2025) to verify claims. It uses BM25 for document retrieval, a custom-built stance detection model to assess article relevance, and the Gemini API with a custom system prompt and context to generate concise summaries for Retrieval Augmented Generation (RAG).

---

## Features

- **Dockerized Setup:** Run the entire application with a single Docker Compose command.
- **Fact Checking:** Retrieve and analyze relevant Wikipedia articles based on your query.
- **Stance Detection:** Determine if an article supports, contradicts, or is irrelevant to the claim.
- **Summarization:** Get a brief summary that consolidates the evidence.
- **Frontend & Backend:** A React frontend communicates seamlessly with a FastAPI backend.

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/hpeter11/TruthScope.git
   ```

2. **Configure the Gemini API Key**

   In the `backend` directory, create a `.env` file with your Gemini API key:

   ```dotenv
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Prepare the Database & Model**

   - **Wikipedia Articles:** Ensure that the `backend/wikipedia_top_1000` folder contains the most viewed Wikipedia articles (in `.txt` format).
   - **Stance Model:** Place your saved model file in the `backend/model` folder (the expected file is `TruthScope.pth`).

4. **Build and Run the Application**

   From the root directory, execute:

   ```bash
   docker compose up --build
   ```

   This command will build both the backend and frontend containers and start the services.

---

## Usage

- **Frontend:** Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to interact with TruthScope.
- **Backend:** The FastAPI backend runs on port `8000` and exposes the `/query` endpoint.

Simply type your question into the interface and receive a list of related Wikipedia articles along with a summary of the fact-checking results.

---

## Project Structure

```
truthscope/
├── backend
│   ├── .env             # Contains the GEMINI_API_KEY
│   ├── Dockerfile       # Dockerfile for backend service
│   ├── wikipedia_top_1000/  # Directory with Wikipedia articles (.txt files)
│   ├── model/           # Directory with the saved stance detection model
│   └── ...              # FastAPI application code
├── frontend
│   ├── Dockerfile       # Dockerfile for frontend service (React app + Nginx)
│   ├── package.json     # Node project file
│   └── ...              # React application code
└── docker-compose.yml   # Docker Compose configuration
```

---

## Notes

- The Wikipedia articles are a pre-selected dataset (the most viewed on February 10th) due to resource constraints.
- Make sure to add your Gemini API key in the backend's `.env` file before running the project.

---

Have fun! 
