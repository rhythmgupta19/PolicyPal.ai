# 🚀 SchemeBot Deployment Guide

Quick deployment instructions so others can use SchemeBot instantly!

## ⚡ 5-Minute Setup

### **Local Setup (Recommended for Testing)**

```bash
# 1. Clone
git clone https://github.com/rhythmgupta19/Ai-asitant.git
cd Ai-asitant

# 2. Install Python 3.9+
# Download from python.org if needed

# 3. Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# 4. Install dependencies
pip install fastapi uvicorn pydantic websockets

# 5. Run server
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001

# 6. In another terminal, run chat
python websocket_client.py

# 7. Or open chat.html in your browser!
```

✅ **Done!** SchemeBot is running locally.

---

## 🌐 Deployment to Cloud (Free Options)

### **Option 1: Railway (Easiest)**

```bash
# 1. Sign up: railway.app
# 2. Install Railway CLI: npm install -g @railway/cli
# 3. Deploy:

railway login
railway init
railway deploy

# Access at railway-provided URL
```

### **Option 2: Render**

```bash
# 1. Sign up: render.com
# 2. Connect GitHub repo
# 3. Create Web Service
# 4. Build command: pip install -r requirements.txt
# 5. Start command: 
#    gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
# 6. Deploy!
```

### **Option 3: Replit**

```
1. Go to replit.com
2. Create new→Import from GitHub
3. Paste: github.com/rhythmgupta19/Ai-asitant
4. Select Python
5. Run button appears - click it!
```

### **Option 4: Google Cloud Run**

```bash
# 1. Install gcloud CLI
# 2. Login: gcloud auth login
# 3. Deploy:

gcloud run deploy schemebot \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --allow-unauthenticated
```

### **Option 5: Docker (Universal)**

```bash
# 1. Install Docker: docker.com/download
# 2. Create Dockerfile (save as "Dockerfile"):

FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn pydantic websockets
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 3. Build & run:
docker build -t schemebot .
docker run -p 8000:8000 schemebot

# With Docker Compose (create docker-compose.yml):

version: '3'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1

# Run:
docker-compose up
```

---

## 🔗 Using Deployed SchemeBot

### **From Anywhere**

```bash
# 1. CLI Client
python websocket_client.py
# Then when prompted for server, change to: ws://your-deployed-url/ws

# 2. Web Browser
# 1. Download chat.html
# 2. Edit first line of JavaScript:
#    const ws = new WebSocket('ws://your-deployed-url/ws');
# 3. Open in browser

# 3. API Calls
curl "https://your-deployed-url/ask?q=health%20insurance&lang=hi"
```

---

## 📦 Requirements.txt

Create `requirements.txt` for easy installation:

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
websockets==12.0
gunicorn==21.2.0
```

Install with: `pip install -r requirements.txt`

---

## 🔧 Environment Configuration

For production, set environment variables:

```bash
# .env file
DEPLOY_ENV=production
LOG_LEVEL=info
HOST=0.0.0.0
PORT=8000
MAX_RESPONSE_BYTES=10240
```

---

## ✅ Verification Checklist

After deployment:

- [ ] Server is running (check logs)
- [ ] `/ping` endpoint works
- [ ] `/ask` endpoint returns schemes
- [ ] WebSocket connection established
- [ ] Chat interface loads
- [ ] Schemes match queries
- [ ] Multiple languages work

Test with:
```bash
curl https://your-url/ping
curl "https://your-url/ask?q=test&lang=hi"
```

---

## 🐛 Troubleshooting

### **"Port already in use"**
```bash
# Use different port:
python -m uvicorn src.main:app --port 9000
```

### **"Module not found"**
```bash
# Install missing packages:
pip install fastapi uvicorn pydantic websockets
```

### **"Connection refused"**
```bash
# Check server is running:
# 1. Is /ping endpoint responding?
# 2. Is correct URL in chat client?
# 3. Are CORS headers set?
```

### **"WebSocket error"**
```bash
# Update chat client with correct server URL:
# ws://localhost:8001/ws  (local)
# ws://your-deploy.app/ws (cloud)
```

---

## 📊 Performance Tips

- ✅ Use production server (Gunicorn)
- ✅ Enable gzip compression
- ✅ Use CDN for static files
- ✅ Add caching headers
- ✅ Monitor memory usage
- ✅ Scale with load balancer

---

## 🆘 Getting Help

1. Check existing GitHub Issues
2. Create new Issue with:
   - Error message
   - Deployment platform
   - Steps to reproduce
3. Include logs: `docker logs schemebot`

---

**Everything set up? Share SchemeBot on LinkedIn! 🚀**
