# Ceylon2US 🇱🇰➡️🇺🇸

An AI-powered search assistant that answers questions about relocating from Sri Lanka to the United States, using **official US government sources only**, with citations.

![Ceylon2US demo](screenshots/demo.png)

## ✨ Features
- 💬 Chat interface built with Streamlit
- 📚 Answers grounded in official sources (USCIS, SSA, U.S. Department of State)
- 🔖 Every answer cites its sources with page numbers and "last checked" dates
- 🛡️ Confidence threshold: says "I don't know" instead of guessing when no relevant source is found
- 🕷️ Web scraper + PDF loader to build the knowledge base

## 🧠 How it works (RAG)
1. **Ingest:** official PDFs and web pages are split into 200-word overlapping chunks
2. **Embed:** each chunk is turned into a 384-dimension vector with `all-MiniLM-L6-v2`
3. **Store:** vectors and metadata are saved in ChromaDB
4. **Retrieve:** the user's question is embedded and the top 4 most similar chunks are found (cosine similarity)
5. **Filter:** chunks below a 0.45 similarity threshold are dropped
6. **Generate:** an LLM (`gpt-oss-120b` via Groq) answers using only those chunks, with citations

## 🛠️ Tech stack
Python · sentence-transformers · ChromaDB · Groq API · Streamlit · BeautifulSoup · pypdf

## 🚀 Run it locally
1. Clone the repo and create a virtual environment:
   ```
   git clone https://github.com/rishikaevenjalin-bit/ceylon2us.git
   cd ceylon2us
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Get a free API key at [console.groq.com](https://console.groq.com) and create a `.env` file:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. Build the search index and start the app:
   ```
   python src/build_index.py
   streamlit run src/app.py
   ```

## 📁 Project structure
```
data/               Official source documents
src/scrape.py       Downloads official web pages
src/ingest.py       Loads and chunks documents
src/build_index.py  Creates embeddings and stores them in ChromaDB
src/answer.py       RAG pipeline (retrieve, filter, generate)
src/app.py          Streamlit chat interface
src/config.py       Shared settings
```

## 🗺️ Roadmap
- [x] **v1:** Visa & documents RAG chatbot
- [ ] **v2:** Degree equivalency check
- [ ] **v3:** Live job finder (Adzuna and USAJOBS APIs)
- [ ] **v4:** Skill gap analysis + free certification suggestions
- [ ] **v5:** Who to contact (local offices, embassy, community groups)
- [ ] **v6:** Deploy online

## 🐛 Lessons learned
- Found and fixed 5 silent data bugs (a 404 page saved as a source, image-only PDFs, duplicate files) by adding a per-source validation summary
- Government sites often block scrapers (403), so the pipeline supports manually saved PDFs and text
- Similarity scores reveal coverage gaps: low scores mean the knowledge base lacks that topic

## ⚠️ Disclaimer
For general guidance only. Always verify visa and legal information on official government websites.
