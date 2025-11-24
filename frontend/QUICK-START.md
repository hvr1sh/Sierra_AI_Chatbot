# Sierra AI Chatbot - Quick Start

## 🚀 Local Development (Single Terminal)

```bash
cd frontend
npm run dev
```

Wait for: `✓  Ready! Available at http://localhost:3000`

### Access App
Open: **http://localhost:3000**

---

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (frontend + API on port 3000) |
| `npm run build` | Build for production |
| `vercel` | Deploy to Vercel |

---

## 🔧 First Time Setup

```bash
cd frontend

# Install dependencies
npm install
npm install -g vercel

# Setup environment
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here
```

---

## ✅ Verification Checklist

- [ ] `npm run dev` running without errors
- [ ] `.env` file exists with `OPENAI_API_KEY`
- [ ] Can access http://localhost:3000
- [ ] Can send a message in the chat
- [ ] API responds with answer

---

## 🐛 Quick Troubleshooting

**Server not starting?**
- Make sure Vercel CLI is installed: `npm install -g vercel`
- Verify `.env` has `OPENAI_API_KEY`
- Check for port conflicts (port 3000)

**API not responding?**
- Check browser console for errors
- Try: `curl http://localhost:3000/api/health`
- Verify Python dependencies installed

**Port conflict?**
- Kill process on port 3000: `lsof -ti:3000 | xargs kill -9` (Mac/Linux)
- Or use `vercel dev --listen 3001`

---

## 📚 Documentation

- **[DEV-SETUP.md](DEV-SETUP.md)** - Complete development guide
- **[SERVERLESS-SETUP.md](SERVERLESS-SETUP.md)** - Deployment guide
- **[README.md](README.md)** - Project overview

---

## 🚢 Deploy

```bash
vercel
```

Then add `OPENAI_API_KEY` in Vercel Dashboard → Settings → Environment Variables

---

**Need help?** Check [DEV-SETUP.md](DEV-SETUP.md) for detailed instructions.
