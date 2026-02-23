# 🚀 Amretha's AI Job Hunt Command Centre

A full-stack AI-powered job application assistant built with Flask + Google Gemini, hosted on Render.

## Stack
- **Backend:** Python / Flask
- **AI:** Google Gemini 1.5 Flash (free tier)
- **Hosting:** Render (same as Stock Monitor)
- **Frontend:** HTML/CSS/JS

## Deploy to Render (exactly like Stock Monitor)

### Step 1 — Push to GitHub
```bash
# On your Mac, open Terminal in this folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-hunt-app.git
git push -u origin main
```

### Step 2 — Create Render Web Service
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repo
3. Render auto-detects the `render.yaml` — just click **Deploy**

### Step 3 — Add your Gemini API Key
1. In Render dashboard → your service → **Environment**
2. Add variable: `GEMINI_API_KEY` = your key from [aistudio.google.com](https://aistudio.google.com)
3. Click **Save** → Render auto-redeploys

### Step 4 — Done!
Your app is live at `https://job-hunt-app.onrender.com` ✅

## Local Development (Mac)
```bash
# Install dependencies
pip3 install -r requirements.txt

# Set your API key
export GEMINI_API_KEY="AIza..."

# Run locally
python3 web_main.py
# Open http://localhost:5000
```
