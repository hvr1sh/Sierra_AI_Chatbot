# Sierra AI Chatbot (Serverless)

A serverless RAG-powered chatbot that answers questions about Sierra AI using OpenAI GPT-3.5 Turbo.

## 🚀 Quick Start

### Local Development (Single Terminal)

```bash
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run everything (frontend + API)
npm run dev
```

**Open browser**: `http://localhost:3000`

> **Note**: `vercel dev` runs both the frontend and serverless API functions together on port 3000.

### Deploy to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Add environment variables** in Vercel Dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key

## 📁 Project Structure

```
frontend/
├── api/                      # Serverless Functions (Python)
│   ├── chat.py              # Chat endpoint
│   ├── health.py            # Health check
│   ├── requirements.txt     # Python dependencies
│   └── lib/                 # RAG modules
│       ├── openai_client.py # OpenAI integration
│       ├── retrieval.py     # Vector search
│       └── chroma_db/       # Embedded database
├── src/                     # React Frontend
│   ├── components/          # UI components
│   ├── services/            # API client
│   └── assets/              # Images, fonts
├── public/                  # Static files
├── vercel.json             # Vercel config
└── package.json            # Dependencies
```

## 🛠️ Tech Stack

- **Frontend**: React 18 + Vite
- **Styling**: Custom CSS (Sierra AI theme)
- **Backend**: Vercel Serverless Functions (Python 3.9)
- **LLM**: OpenAI GPT-3.5 Turbo
- **Vector DB**: ChromaDB (embedded)
- **Embeddings**: Sentence Transformers (local)

## 📚 Documentation

- **[Serverless Setup Guide](SERVERLESS-SETUP.md)**: Complete deployment guide
- **[Font Setup](FONT-SETUP.md)**: GT America font configuration

## 🎨 Customization

### Colors

Sierra's brand colors are defined in CSS files:
- Primary green: `#006838`
- Background: `#F6F5F3`
- Buttons: `#05351D`

### Fonts

The app uses **GT America** with system font fallbacks. See [FONT-SETUP.md](FONT-SETUP.md) for details.

### Branding

The Sierra.ai logo is located at `src/assets/sierra-logo.svg`.

## 🔧 Available Scripts

- `npm run dev` - Run with Vercel CLI (includes API)
- `npm run dev:vite` - Run Vite only (frontend)
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## 🌐 API Endpoints

### POST `/api/chat`
Send a message to the chatbot.

### GET `/api/health`
Check API status.

See [SERVERLESS-SETUP.md](SERVERLESS-SETUP.md) for detailed API documentation.

## 💰 Cost Estimates

- **Vercel**: Free tier (100GB bandwidth, 100hrs serverless)
- **OpenAI API**: ~$0.10-0.50/day (moderate usage)

**Total**: Can run entirely on free tiers for development

## 🐛 Troubleshooting

**"Module not found" errors**:
```bash
cd api
pip install -r requirements.txt
```

**API not working locally**:
- Make sure you're using `npm run dev` (not `npm run dev:vite`)
- Check `.env` file has `OPENAI_API_KEY`

**Cold starts on Vercel**:
- First request may take 2-3 seconds
- Subsequent requests are fast
- Consider Vercel Pro for better performance

## 📝 Notes

- The `backend/` directory is **no longer needed** - all logic is in `api/`
- ChromaDB is embedded in the deployment (no external database needed)
- Embeddings are generated locally (no OpenAI embedding costs)

## 🚀 Next Steps

- [ ] Add streaming responses
- [ ] Implement chat history
- [ ] Add user authentication
- [ ] Deploy to edge functions for lower latency
- [ ] Add caching layer (Redis/KV)

---

Built for Sierra AI with ❤️
