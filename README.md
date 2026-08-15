# CollegeBot 🤖

A RAG (Retrieval Augmented Generation) based chatbot for Bennett University students.

## Tech Stack
- FAISS — vector similarity search
- Sentence Transformers (all-MiniLM-L6-v2) — embeddings
- Groq (`openai/gpt-oss-20b`) — LLM for answer generation
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
## 🚀 Live Demo
- **Frontend:** https://campuscompass-bu.lovable.app 
- **Backend API:** https://college-bot-production-9230.up.railway.app
- **API Docs:** https://college-bot-production-9230.up.railway.app/docs

## 🛠️ Tech Stack
- **LLM:** Groq `openai/gpt-oss-20b`
- **Embeddings:** all-MiniLM-L6-v2
- **Vector DB:** FAISS
- **Backend:** FastAPI (Railway)
- **Frontend:** React (Lovable)
- **Scraping:** BeautifulSoup

## Note
Originally built on `llama-3.1-8b-instant`, migrated to `openai/gpt-oss-20b` ahead of Groq's August 16, 2026 deprecation of the former. Same API endpoint, no other changes required. See `NOTES.md` for the full migration writeup.