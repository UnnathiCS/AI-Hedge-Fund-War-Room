# AI Hedge Fund War Room - check it out : https://ai-hedge-fund-war-room--unnathics.replit.app/

An intelligent multi-agent debate system where three AI personas (Aggressive, Balanced, Safe) analyze stocks in real-time, providing personalized investment recommendations based on your trading expertise level.

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/React-19.0+-cyan)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue)

---

## 🎯 What is This?

Imagine having three expert traders debating a stock in real-time:
- **Aggressive** 🔥 - The optimistic risk-taker who sees opportunities
- **Balanced** 📊 - The analytical middle-ground who weighs pros and cons
- **Safe** 🛡️ - The conservative voice who prioritizes capital preservation

Each agent adapts their advice based on **your trading expertise level** (beginner/intermediate/advanced) and addresses you by **your name and preferred terms** (girl/bro/boss).

Perfect for learning how professional traders think, getting diverse perspectives, and making informed investment decisions.

---

## ✨ Key Features

✅ **3-Agent Debate System** - Three AI personas with different perspectives on stocks
✅ **User Personalization** - Uses your name, gender-based terms, expertise level
✅ **Expertise-Based Responses** - Different complexity levels for beginners/intermediate/advanced traders
✅ **Real-Time Analysis** - Pulls market data, fundamentals, and institutional sentiment
✅ **Clear Verdict** - Final BUY/HOLD/SELL recommendation with reasoning tailored to your level
✅ **Beautiful UI** - Modern glassmorphic design with smooth animations
✅ Casual, professional tone with light slang ("bro", "girl", "boss")

---

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.10+** installed ([download here](https://www.python.org/downloads/))
- **Node.js 18+** and **npm** or **Bun** ([download here](https://nodejs.org/))
- **Git** for cloning the repo
- A **Groq API Key** (free tier available at [console.groq.com](https://console.groq.com))
- Internet connection for API calls

### Check Your Versions

```bash
python --version      # Should be 3.10 or higher
node --version        # Should be 18 or higher
npm --version         # Should be 8 or higher
```

---

## 🛠️ Quick Start (5 Minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/UnnathiCS/ai-trading-debate.git
cd ai-trading-debate
```

### Step 2: Set Up the Backend

```bash
# Navigate to backend folder
cd debate_engine

# Create a Python virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file and add your Groq API key
echo "GROQ_API_KEY=your_actual_api_key_here" > .env
```

**Get a Groq API Key:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create an API key
4. Copy it and paste in the `.env` file

### Step 3: Start the Backend

```bash
# Make sure you're in the debate_engine folder with venv activated
python -m uvicorn api:app --reload --port 8501

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8501
# INFO:     Application startup complete
```

**Keep this terminal open!**

### Step 4: Set Up the Frontend

Open **a new terminal** and run:

```bash
# Navigate to frontend folder
cd Frontend_UI

# Install dependencies
npm install
# or if you prefer Bun:
# bun install

# Start the development server
npm run dev
# or with Bun:
# bun run dev
```

You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 5: Open the App

Open your browser and go to: **http://localhost:5173/**

✨ **You're done!** Start debating!

---

## 🚀 Deploy & Share

Ready to share with others? Get a public link in minutes!

### Quick Deploy Options

| Option | Time | Difficulty | Link |
|--------|------|-----------|------|
| **Replit** | 5 min | ⭐ Easy | [Guide](./DEPLOY_REPLIT.md) |
| **Vercel + Railway** | 15 min | ⭐⭐ Medium | [Guide](./DEPLOY_VERCEL_RAILWAY.md) |
| **Docker** | 20 min | ⭐⭐⭐ Hard | [Setup](./Dockerfile) |

**TL;DR - Deploy to Replit in 3 steps:**
1. Go to [replit.com/new](https://replit.com/new)
2. Import GitHub repo
3. Add `GROQ_API_KEY` secret → Click "Run"

Done! You'll get a public link in 5 minutes.

[See full deployment options →](./DEPLOYMENT_OPTIONS.md)

---

## 🎮 How to Use

### 1. **Set Your Profile**
   - Enter your **name**
   - Select your **gender** (Male/Female/Other)
   - Choose your **expertise level** (Beginner/Intermediate/Advanced)

### 2. **Pick a Stock**
   - Search for a company from the 604 available Indian stocks
   - Click on a stock to start the debate

### 3. **Watch the Debate**
   - Three agents will analyze the stock in real-time
   - Each brings their perspective
   - They address you personally by name

### 4. **Get Your Verdict**
   - See each agent's vote (BUY/HOLD/AVOID)
   - Get the final consensus verdict
   - Read personalized recommendation based on YOUR expertise level

---

## 📁 Project Structure

```
ai-trading-debate/
├── debate_engine/              # Python Backend
│   ├── api.py                  # FastAPI server
│   ├── engines/
│   │   ├── debate_engine.py    # 3-agent debate logic
│   │   ├── market_data_engine.py
│   │   └── llm_service.py
│   ├── dataset/
│   │   └── final_dataset_cleaned.csv  # 604 Indian companies
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Your Groq API key (create this)
│
├── Frontend_UI/                # React + TypeScript Frontend
│   ├── src/
│   │   ├── pages/Index.tsx     # Main app page
│   │   ├── components/
│   │   │   ├── warroom/        # Debate components
│   │   │   ├── UserProfile.tsx # User profile form
│   │   │   └── Footer.tsx      # Footer
│   │   └── services/
│   │       └── backendApi.ts   # API client
│   ├── package.json            # Node dependencies
│   ├── vite.config.ts          # Build config
│   └── tsconfig.json           # TypeScript config
│
└── README.md                   # This file!
```

---

## 🔧 Troubleshooting

### Port Already in Use?

If port 8501 is busy:
```bash
# Run on a different port
python -m uvicorn api:app --reload --port 8502
```

Then update the frontend API URL in `Frontend_UI/src/services/backendApi.ts`:
```typescript
const API_URL = "http://localhost:8502";
```

### ModuleNotFoundError: No module named 'groq'

```bash
# Make sure you're in the venv:
source debate_engine/venv/bin/activate
# Then reinstall:
pip install -r debate_engine/requirements.txt
```

### Module 'yfinance' not found

```bash
pip install yfinance
```

### Groq API Key Error

- Check your `.env` file is in the `debate_engine/` folder
- Make sure format is: `GROQ_API_KEY=your_key_here` (no quotes)
- Verify the key is valid at [console.groq.com](https://console.groq.com)

### Frontend shows blank page

1. Check browser console for errors (F12)
2. Verify backend is running: `curl http://localhost:8501/health`
3. Try: `npm run build` to check for build errors

---

## 🚀 Advanced: Production Deployment

### Build Frontend for Production

```bash
cd Frontend_UI
npm run build
# Creates optimized build in dist/
```

### Deploy Backend

```bash
cd debate_engine
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8501 api:app
```

### Using with a Custom Domain

Update `Frontend_UI/src/services/backendApi.ts`:
```typescript
const API_URL = "https://your-domain.com/api";
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────┐
│     React Frontend (Vite)           │
│  - User Profile (Name/Gender/Exp)   │
│  - Stock Selector                   │
│  - Debate Room (Real-time)          │
│  - Final Verdict                    │
└────────────┬────────────────────────┘
             │ HTTP
             ↓
┌─────────────────────────────────────┐
│     FastAPI Backend                 │
│  - Multi-Agent Debate Engine        │
│  - Market Data Fetcher              │
│  - Groq LLM Integration             │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    ↓                 ↓
  Groq LLM      Market Data (yfinance)
  (Free API)    & Stock Dataset (CSV)
```

---

## 🎓 Learning Path

**New to trading?** Start with:
1. Pick a stock you know (Apple, Tesla, HDFC Bank)
2. Select "Beginner" expertise level
3. Read Simple Explanation in the FinalVerdict
4. Understand why each agent has a different perspective

**Intermediate?** Try:
1. Enable "Intermediate" expertise to see technical metrics
2. Compare agent perspectives
3. Make your own decision

**Advanced?** Enjoy:
1. Deep contrarian analysis from the Aggressive agent
2. Risk analysis from the Safe agent
3. Use as a sounding board for your own thesis

---

## 🤝 Contributing

Found a bug? Have an idea? Fork the repo and submit a PR!

```bash
git clone <your-fork>
cd ai-trading-debate
# Create a feature branch
git checkout -b feature/amazing-feature
# Make changes, commit, and push
git push origin feature/amazing-feature
```

---

## 📝 API Reference

### Start a Debate
```bash
POST http://localhost:8501/api/debate
Content-Type: application/json

{
  "company": "HDFC Bank",
  "ticker": "HDFCBANK",
  "user_name": "Arjun",
  "user_gender": "male",
  "user_expertise": "intermediate"
}
```

### Get Health Status
```bash
GET http://localhost:8501/health
```

---

## 📄 License

This project is open source and available under the MIT License.

---

## ❤️ Built with Love

Built with ❤️ by **[UnnathiCS](https://github.com/UnnathiCS)**

Contributions, stars, and feedback are always welcome! ⭐

---

## 🙏 Acknowledgments

- **Groq** for free LLM API
- **FastAPI** for excellent backend framework
- **React + Vite** for fast frontend development
- **Shadcn/UI** for beautiful components
- **yfinance** for market data

---

## 📞 Support

If you run into issues:

1. **Check the Troubleshooting section** above
2. **Look at existing issues** on GitHub
3. **Create a new issue** with:
   - Error message
   - Your OS and Python/Node versions
   - Steps to reproduce

---

**Happy Debating! 🎯📈**
