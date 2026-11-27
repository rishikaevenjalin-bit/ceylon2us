# Ceylon2US 🇱🇰➡️🇺🇸

An AI-powered search assistant that answers questions about relocating from Sri Lanka to the United States, using **official US government sources only**, with citations.


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
1. Clone the repo and create a virtual environment
