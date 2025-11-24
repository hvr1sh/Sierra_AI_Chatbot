# Development Setup Guide

This guide explains how to run the Sierra AI Chatbot locally with serverless functions.

## Architecture Overview

The app uses **Vercel Dev** for local development - a unified server that runs both frontend and API:

**Single Process** (Port 3000):
- Frontend (React/Vite)
- Serverless API Functions (Python)

```
Browser → http://localhost:3000
           ↓
    [Vercel Dev Server]
           ├─→ Static Files (Frontend)
           └─→ /api/* (Serverless Functions)
```

## Prerequisites

- Node.js 18+
- Python 3.9+
- OpenAI API key
- npm or yarn

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend

# Install Node.js packages
npm install

# Install Vercel CLI globally (if not already installed)
npm install -g vercel
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-proj-your-key-here
```

### 3. Run Development Server

Start everything with **one command**:

```bash
npm run dev
```

This will:
- Start Vercel dev server on port 3000
- Build and serve the frontend (Vite)
- Make serverless functions available at `/api/*`
- Watch for changes in both `src/` and `api/` directories
- Hot reload on file changes

You should see:
```
Vercel CLI X.X.X
> Ready! Available at http://localhost:3000
```

### 4. Open the App

Navigate to: **http://localhost:3000**

## Quick Start Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (port 3000) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |

## Development Workflow

### Making Changes

**Frontend Changes** (React components, CSS):
- Edit files in `src/`
- Vercel dev will hot reload automatically
- No need to restart server

**API Changes** (Python functions):
- Edit files in `api/`
- Vercel dev will detect changes
- May need to make a new request to see changes

**Environment Variable Changes**:
- Restart the dev server after changing `.env`

### Testing API Endpoints

**Chat Endpoint**:
```bash
curl -X POST http://localhost:3000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Sierra AI?"}'
```

**Health Check**:
```bash
curl http://localhost:3000/api/health
```

## Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```bash
# Use a different port
vercel dev --listen 3001
```

Or kill the process using port 3000:
```bash
# Mac/Linux
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### API Not Responding

1. **Check Vercel dev is running**: Look for "Ready! Available at" message
2. **Check environment variables**: Ensure `.env` has `OPENAI_API_KEY`
3. **Check Python dependencies**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```
4. **Check browser console**: Look for error messages

### CORS Errors

The serverless functions include CORS headers. If you see CORS errors:

1. Make sure `vercel dev` is running
2. Access app via `http://localhost:3000` (the port shown by vercel)
3. Check browser console for specific errors

### "Module not found" Errors

Install Python dependencies:
```bash
cd api
pip install -r requirements.txt
```

### ChromaDB Not Found

Make sure ChromaDB data exists:
```bash
ls api/lib/chroma_db/
```

If empty, copy from backend:
```bash
cp -r ../backend/rag/chroma_db api/lib/
```

## Production Build

Build for production:
```bash
npm run build
```

The `dist/` folder will contain the optimized frontend. Serverless functions in `api/` are automatically deployed by Vercel.

## Deployment

See [SERVERLESS-SETUP.md](SERVERLESS-SETUP.md) for detailed deployment instructions.

Quick deploy:
```bash
vercel
```

## Tips

- Use browser DevTools Network tab to debug API calls
- Check console output for Python errors from serverless functions
- Frontend errors appear in browser console
- Hot reload works for both frontend and API changes

## Common Development Tasks

### Adding a New API Endpoint

1. Create `api/your-endpoint.py`
2. Follow the handler pattern from `api/chat.py`
3. Add to `src/services/api.js` if needed
4. Restart Vercel dev server

### Updating Dependencies

**Frontend**:
```bash
npm install package-name
```

**API (Python)**:
```bash
cd api
echo "package-name==version" >> requirements.txt
pip install -r requirements.txt
```

### Debugging

**Frontend**: Use browser DevTools

**API**: Add print statements, they'll appear in Vercel dev terminal

**Network**: Check Network tab in DevTools for API calls

## Need Help?

- Check [SERVERLESS-SETUP.md](SERVERLESS-SETUP.md) for deployment issues
- Check Vercel docs: https://vercel.com/docs
- Check Vite docs: https://vitejs.dev

---

Happy coding! 🚀
