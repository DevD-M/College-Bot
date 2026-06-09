# CollegeBot 🤖

A RAG (Retrieval Augmented Generation) based chatbot for Bennett University students.

## Tech Stack
- FAISS — vector similarity search
- Sentence Transformers (all-MiniLM-L6-v2) — embeddings
- Groq (LLaMA 3.1) — LLM for answer generation
- Python

## Architecture
User Query → Embed → FAISS Search → Relevant Chunks → LLM → Answer

## Setup
```bash
pip install faiss-cpu sentence-transformers groq python-dotenv
```
Add GROQ_API_KEY in .env file, then:
```bash
python ingest.py   # build index
python app.py      # run chatbot
```