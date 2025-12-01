# BrightPath RAG Chatbot - Complete Usage Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Running the Application](#running-the-application)
5. [Using the Application](#using-the-application)
6. [API Endpoints](#api-endpoints)
7. [Troubleshooting](#troubleshooting)
8. [Development Commands](#development-commands)

---

## 🎯 Project Overview

The BrightPath RAG Chatbot is a production-ready HR policy assistant that uses Retrieval-Augmented Generation (RAG) to answer questions about company policies. It combines:

- **Frontend**: React + Vite + Tailwind CSS (Port 3000)
- **Backend**: FastAPI (Port 8000)
- **Vector Store**: ChromaDB (Port 8001, optional)
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-small

---

## 📦 Prerequisites

Before starting, ensure you have:

1. **Python 3.11+** installed
   ```bash
   python3 --version  # Should show 3.11 or higher
   ```

2. **Node.js 18+** and npm installed
   ```bash
   node --version    # Should show v18 or higher
   npm --version
   ```

3. **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/api-keys)

4. **Docker & Docker Compose** (optional, for containerized deployment)
   ```bash
   docker --version
   docker compose version
   ```

---

## 🚀 Initial Setup

### Step 1: Clone/Navigate to Project

```bash
cd /Users/sagnikdas/brightpath-rag-chatbot
```

### Step 2: Create Environment File

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Model Configuration
MODEL_CHAT=gpt-4o-mini
MODEL_EMBEDDING=text-embedding-3-small

# Chroma Vector Store Configuration
CHROMA_PATH=./chroma_db

# RAG Configuration
TOP_K=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# Application Configuration
DEBUG=False
EOF
```

**⚠️ Important**: Replace `sk-your-actual-api-key-here` with your actual OpenAI API key!

### Step 3: Install Backend Dependencies

```bash
# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

### Step 4: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 5: Verify Documents

Ensure your HR policy documents are in the `docs/` folder:

```bash
ls docs/
# Should show files like:
# BrightPath_Data_Security_Confidentiality
# BrightPath_Employee_Handbook
# BrightPath_HR_Quick_Reference
# ... etc
```

### Step 6: Ingest Documents into Vector Store

This step processes your documents and creates embeddings:

```bash
python3 ingest_docs.py
```

**Expected Output:**
```
============================================================
🚀 BrightPath RAG - Document Ingestion Started
============================================================
🔄 Loading documents from ./docs...
📄 Loaded 9 documents
🔄 Chunking documents (size=1000, overlap=200)...
✂️  Created XXX chunks
🔄 Creating OpenAI embeddings...
💾 Ingesting XXX chunks into Chroma...
✅ Document ingestion completed successfully!
📊 Stats:
   - Total chunks: XXX
   - Vector store path: ./chroma_db
   - Embedding model: text-embedding-3-small
============================================================
🎉 Ready to start chatbot!
============================================================
```

**Note**: This step requires a valid OpenAI API key and will use API credits for embeddings.

---

## 🏃 Running the Application

You have two options: **Local Development** or **Docker Compose**.

### Option A: Local Development (Recommended for Development)

#### Terminal 1: Start Backend Server

```bash
cd /Users/sagnikdas/brightpath-rag-chatbot
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Verify Backend:**
- Open browser: http://localhost:8000/docs (Swagger UI)
- Or: http://localhost:8000/health (Health check)

#### Terminal 2: Start Frontend Server

```bash
cd /Users/sagnikdas/brightpath-rag-chatbot/frontend
npm run dev
```

**Expected Output:**
```
  VITE v4.4.5  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Access Frontend:**
- Open browser: http://localhost:3000

### Option B: Docker Compose (Recommended for Production)

```bash
cd /Users/sagnikdas/brightpath-rag-chatbot

# Build and start all services
docker compose up --build

# Or run in detached mode
docker compose up -d --build

# View logs
docker compose logs -f

# Stop services
docker compose down
```

**Services:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- ChromaDB: http://localhost:8001 (optional)

---

## 💬 Using the Application

### Web Interface

1. **Open the Chat Interface**
   - Navigate to http://localhost:3000
   - You'll see the BrightPath HR Assistant welcome screen

2. **Ask Questions**
   - Type your question in the input field
   - Press Enter or click the send button (➤)
   - Wait for the AI response (usually 2-5 seconds)

3. **Example Questions**
   ```
   "How many annual leave days do I get?"
   "What's the remote work policy?"
   "How does performance review work?"
   "What about travel reimbursement?"
   "Data security guidelines?"
   "What is the maternity leave policy?"
   "How do I request time off?"
   ```

4. **View Sources**
   - Each response includes source citations
   - Click on citations to expand and see the original document excerpts
   - Sources show which HR policy document was used

### API Usage (cURL Examples)

#### Health Check

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "rag_pipeline": true,
  "vector_store": true
}
```

#### Chat Endpoint

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How many annual leave days do I get?",
    "chat_history": []
  }'
```

**Response:**
```json
{
  "answer": "You are entitled to 18 days of annual leave per calendar year...",
  "sources": [
    "BrightPath_Employee_Handbook",
    "BrightPath_Leave_Attendance_Policy"
  ],
  "citations": [
    {
      "content": "Annual Leave: 18 days per calendar year...",
      "source": "BrightPath_Leave_Attendance_Policy",
      "chunk_id": 0
    }
  ]
}
```

#### Get Application Info

```bash
curl http://localhost:8000/api/info
```

**Response:**
```json
{
  "app": "BrightPath RAG Chatbot",
  "version": "1.0.0",
  "openai_model": "gpt-4o-mini",
  "embedding_model": "text-embedding-3-small",
  "vector_store": "./chroma_db",
  "top_k": 5
}
```

### Python Client Example

```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/chat",
    json={
        "query": "What is the remote work policy?",
        "chat_history": []
    }
)

data = response.json()
print(f"Answer: {data['answer']}")
print(f"Sources: {data['sources']}")
```

### JavaScript/React Client Example

```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'How many sick days do I get?',
    chat_history: []
  })
});

const data = await response.json();
console.log(data.answer);
console.log(data.sources);
```

---

## 🔌 API Endpoints

### Base URL
- Local: `http://localhost:8000`
- Docker: `http://localhost:8000`

### Endpoints

#### `GET /`
Root endpoint - Returns welcome message and links

#### `GET /health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "rag_pipeline": true,
  "vector_store": true
}
```

#### `POST /chat`
Main chat endpoint

**Request Body:**
```json
{
  "query": "Your question here",
  "chat_history": [
    {"role": "user", "content": "Previous question"},
    {"role": "assistant", "content": "Previous answer"}
  ]
}
```

**Response:**
```json
{
  "answer": "Generated answer...",
  "sources": ["Document1", "Document2"],
  "citations": [
    {
      "content": "Excerpt from document...",
      "source": "Document1",
      "chunk_id": 0
    }
  ]
}
```

#### `GET /api/info`
Get application configuration information

#### `GET /docs`
Interactive API documentation (Swagger UI)

---

## 🔧 Troubleshooting

### Issue: "No documents found" or Empty Vector Store

**Solution:**
```bash
# Re-run document ingestion
python3 ingest_docs.py
```

**Check:**
- Documents exist in `docs/` folder
- Files start with `BrightPath_`
- OpenAI API key is valid

### Issue: "OpenAI API Error" or "Invalid API Key"

**Solution:**
1. Check your `.env` file has the correct API key:
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

2. Verify the key is valid:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. Ensure you have sufficient OpenAI credits

### Issue: Backend Won't Start

**Check:**
```bash
# Verify Python dependencies
python3 -m pip list | grep -E "fastapi|uvicorn|langchain"

# Check for port conflicts
lsof -i :8000

# Try running with verbose logging
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level debug
```

### Issue: Frontend Can't Connect to Backend

**Check:**
1. Backend is running on port 8000
2. CORS is enabled (should be by default)
3. Check browser console for errors
4. Verify API URL in `frontend/src/components/Chatbot.jsx`:
   ```javascript
   const API_URL = 'http://localhost:8000'
   ```

### Issue: Port Already in Use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID)
kill -9 <PID>

# Or change port in docker-compose.yml or command
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Issue: Documents Not Loading

**Check:**
1. Document files exist:
   ```bash
   ls -la docs/
   ```

2. Files match the pattern `BrightPath_*`:
   ```bash
   ls docs/BrightPath_*
   ```

3. Re-run ingestion:
   ```bash
   python3 ingest_docs.py
   ```

### Issue: Slow Response Times

**Possible Causes:**
- Large number of documents
- Network latency to OpenAI API
- First request (cold start)

**Solutions:**
- Reduce `TOP_K` in `.env` (default: 5)
- Use faster embedding model
- Check OpenAI API status

---

## 🛠️ Development Commands

### Backend Development

```bash
# Run backend with auto-reload
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run backend in debug mode
DEBUG=True python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test backend health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

### Frontend Development

```bash
# Start development server
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Document Management

```bash
# Ingest documents
python3 ingest_docs.py

# Check vector store
ls -la chroma_db/

# Clear vector store (if needed)
rm -rf chroma_db/
python3 ingest_docs.py
```

### Docker Commands

```bash
# Build and start
docker compose up --build

# Start in background
docker compose up -d

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Stop services
docker compose down

# Rebuild specific service
docker compose build backend
docker compose up backend

# Access backend container
docker compose exec backend bash

# Access frontend container
docker compose exec frontend sh
```

### Testing

```bash
# Test backend health
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "chat_history": []}'

# Test frontend
curl http://localhost:3000
```

---

## 📊 Configuration Options

Edit `.env` file to customize:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | Your OpenAI API key |
| `MODEL_CHAT` | `gpt-4o-mini` | LLM model for chat |
| `MODEL_EMBEDDING` | `text-embedding-3-small` | Embedding model |
| `CHROMA_PATH` | `./chroma_db` | Vector store location |
| `TOP_K` | `5` | Number of documents to retrieve |
| `CHUNK_SIZE` | `1000` | Document chunk size |
| `CHUNK_OVERLAP` | `200` | Chunk overlap |
| `DEBUG` | `False` | Debug mode |

---

## 📝 Project Structure

```
brightpath-rag-chatbot/
├── app/                    # Backend application
│   ├── main.py            # FastAPI app entry point
│   ├── config.py          # Configuration settings
│   ├── models.py          # Pydantic models
│   ├── rag/               # RAG pipeline
│   │   ├── pipeline.py    # Main RAG pipeline
│   │   ├── retriever.py   # Document retrieval
│   │   └── llm.py         # LLM integration
│   ├── storage/           # Vector store
│   │   ├── vectorstore.py
│   │   └── document_loader.py
│   └── utils/             # Utilities
│       ├── logger.py
│       └── prompts.py
├── frontend/              # React frontend
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       └── Chatbot.jsx
│   └── package.json
├── docs/                  # HR policy documents
├── chroma_db/             # Vector store (auto-created)
├── ingest_docs.py         # Document ingestion script
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Backend Docker image
└── .env                  # Environment variables (create this)
```

---

## 🎓 Best Practices

1. **API Key Security**
   - Never commit `.env` to version control
   - Use environment variables in production
   - Rotate API keys regularly

2. **Document Management**
   - Keep documents in `docs/` folder
   - Use consistent naming: `BrightPath_*.md`
   - Re-run ingestion after document updates

3. **Performance**
   - Monitor OpenAI API usage
   - Adjust `TOP_K` based on accuracy needs
   - Use appropriate chunk sizes for your documents

4. **Development**
   - Use `--reload` flag for backend development
   - Check logs regularly: `docker compose logs -f`
   - Test API endpoints with Swagger UI

---

## 🚀 Next Steps

1. **Customize Prompts**: Edit `app/utils/prompts.py`
2. **Add More Documents**: Add files to `docs/` and re-run ingestion
3. **Deploy**: Use Docker Compose or deploy to cloud (Railway, Render, etc.)
4. **Monitor**: Set up logging and monitoring for production use

---

## 📞 Support

For issues:
1. Check the Troubleshooting section above
2. Review API documentation at http://localhost:8000/docs
3. Check application logs
4. Verify environment configuration

---

**Happy Chatting! 🎉**


