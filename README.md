# 🤖 SchemeBot - Government Scheme AI Assistant

**SchemeBot** is an intelligent AI assistant that helps users discover and access government schemes in their own language. Built with real-time WebSocket support and optimized for low-bandwidth environments.

## ✨ Features

- 🌍 **Multi-language Support**: Hindi, Tamil, Telugu, Bengali, Marathi
- ⚡ **Real-time Chat**: WebSocket-based instant responses
- 📱 **Low-bandwidth Optimized**: Works on 2G networks
- 🎯 **Accurate Matching**: Smart scheme discovery
- 🔄 **Multiple Interfaces**: REST API, WebSocket API, Web UI, CLI
- 🧪 **Fully Tested**: 12+ passing tests
- 🚀 **Production Ready**: FastAPI + Uvicorn

---

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
pip install fastapi uvicorn pydantic websockets
```

### **2. Run the Server**
```bash
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
```

### **3. Choose Your Interface**

#### **Option A: Interactive CLI Chat**
```bash
python websocket_client.py
```

#### **Option B: Web Browser Chat**
Open `chat.html` in your browser

#### **Option C: API Calls**
```bash
curl http://127.0.0.1:8001/ping
curl "http://127.0.0.1:8001/ask?q=health%20insurance&lang=hi"
```

---

## 📋 API Documentation

### **REST Endpoints**

#### `GET /ping` - Health Check
```bash
curl http://127.0.0.1:8001/ping
# Response: {"msg":"ok"}
```

#### `GET /ask?q=query&lang=hi` - Search Schemes
```bash
curl "http://127.0.0.1:8001/ask?q=health%20insurance&lang=hi"
```

**Languages**: `hi` (Hindi), `ta` (Tamil), `te` (Telugu), `bn` (Bengali), `mr` (Marathi)

### **WebSocket Endpoint**

#### `WS /ws` - Real-time Chat
Send: `{"q": "health insurance", "lang": "hi"}`

---

## 📁 Project Structure

```
SchemeBot/
├── src/main.py                 # FastAPI app + WebSocket
├── data/schemes.json           # Schemes database
├── chat.html                   # Web interface
├── websocket_client.py         # CLI client
├── tests/                      # Test suite
└── README.md
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 📱 How Others Can Use It

### **Step 1: Clone**
```bash
git clone https://github.com/rhythmgupta19/Ai-asitant.git
cd Ai-asitant
```

### **Step 2: Setup**
```bash
pip install -r requirements.txt
```

### **Step 3: Run**
```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8001
```

### **Step 4: Connect**
- CLI: `python websocket_client.py`
- Web: Open `chat.html`
- API: Make HTTP requests

---

## 📊 Supported Schemes

10+ government schemes including:
- 🏥 Health insurance, life insurance
- 🎓 Education schemes
- 💼 Business loans, startups
- 🏠 Housing programs
- 👨‍🌾 Agricultural support
- 💰 Employment programs

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push & create PR

---

## 📄 License

MIT License

---

**Made with ❤️ for accessibility and inclusion**
