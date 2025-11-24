# Sierra AI Chatbot - Serverless Setup Guide

This application now uses **serverless functions** instead of a separate backend server. All API endpoints are deployed as serverless functions that run on-demand.

## Architecture

```
frontend/
├── api/                    # Serverless functions (Python)
│   ├── chat.py            # Main chat endpoint
│   ├── health.py          # Health check endpoint
│   ├── requirements.txt   # Python dependencies
│   └── lib/               # Shared RAG modules
│       ├── openai_client.py
│       ├── retrieval.py
│       └── chroma_db/     # Vector database
├── src/                   # React frontend
└── vercel.json           # Vercel configuration
```

## Prerequisites

- Node.js 18+
- Python 3.9+ (for local development)
- OpenAI API key
- Vercel account (for deployment)

## Local Development

### 1. Install Dependencies

```bash
cd frontend

# Install Node.js dependencies
npm install

# Install Vercel CLI globally (if not already installed)
npm install -g vercel
```

### 2. Set Environment Variables

Create a `.env` file in the `frontend` directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run Development Server

```bash
npm run dev
```

This will:
- Start Vercel's local development server
- Run your React app on `http://localhost:3000`
- Make serverless functions available at `/api/*`
- Auto-reload on code changes

### Alternative: Run Vite Only (without API)

If you just want to work on the frontend:

```bash
npm run dev:vite
```

## Deployment to Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_REPO_URL)

### Manual Deploy

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

4. **Set Environment Variables** in Vercel Dashboard:
   - Go to your project → Settings → Environment Variables
   - Add: `OPENAI_API_KEY` with your OpenAI API key

5. **Redeploy** (if env vars changed):
   ```bash
   vercel --prod
   ```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## API Endpoints

### POST `/api/chat`

Send a message to the chatbot.

**Request**:
```json
{
  "message": "What is Sierra AI?",
  "top_k": 5
}
```

**Response**:
```json
{
  "answer": "Sierra is a conversational AI platform...",
  "sources": ["https://sierra.ai/about"],
  "usage": {
    "input_tokens": 1234,
    "output_tokens": 456
  }
}
```

### GET `/api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "ready",
  "message": "Sierra AI Chatbot API (Serverless)"
}
```

## How It Works

1. **User sends message** → React frontend
2. **Frontend calls** → `/api/chat` serverless function
3. **Serverless function**:
   - Retrieves relevant documents from ChromaDB
   - Sends context + question to OpenAI
   - Returns generated answer
4. **Frontend displays** → Response with sources

## Cold Starts

Serverless functions may experience "cold starts" (1-3 seconds delay) when:
- First request after inactivity
- After a new deployment
- During high traffic (new instances spinning up)

To minimize cold starts:
- Keep functions lightweight
- Use global variables for initialization (done)
- Consider Vercel Pro for better cold start performance

## Cost Estimates

### Vercel (Serverless Hosting)
- **Free Tier**: 100GB bandwidth, 100 hours serverless execution
- **Pro Tier** ($20/mo): 1TB bandwidth, unlimited serverless execution

### OpenAI API
- **GPT-3.5 Turbo**: ~$0.10-0.50/day with moderate usage
  - Input: $0.50/million tokens
  - Output: $1.50/million tokens

**Total**: Can run on free tier for development/low traffic

## Troubleshooting

### "Module not found" errors

Install Python dependencies:
```bash
cd frontend/api
pip install -r requirements.txt
```

### Cold start timeouts

Increase function timeout in `vercel.json`:
```json
{
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9",
      "maxDuration": 60
    }
  }
}
```

### CORS errors

Serverless functions include CORS headers. If issues persist, check:
- Browser console for specific errors
- Vercel logs for function errors

### ChromaDB initialization errors

The ChromaDB database is included in `api/lib/chroma_db/`. If it's missing:
1. Run the ingestion script from the original backend
2. Copy `backend/rag/chroma_db/` to `frontend/api/lib/chroma_db/`

## Migration from Flask Backend

The original Flask backend (`backend/`) is **no longer needed**. All functionality has been moved to serverless functions:

| Flask Backend | Serverless Function |
|---------------|-------------------|
| `backend/app.py` | `api/chat.py`, `api/health.py` |
| `backend/rag/` | `api/lib/` |
| `backend/.env` | `frontend/.env` |
| `flask run` | `vercel dev` |

You can safely archive or delete the `backend/` directory.

## Further Optimization

- **Bundle ChromaDB data separately**: Store in S3/R2 and download on cold start
- **Cache responses**: Add Redis/KV cache for common queries
- **Use Edge Functions**: Move lightweight operations to edge for lower latency
- **Add rate limiting**: Prevent API abuse

## Support

For issues specific to:
- **Vercel deployment**: Check [Vercel Docs](https://vercel.com/docs)
- **Python runtime**: See [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python)
- **This app**: Open an issue in the repository
