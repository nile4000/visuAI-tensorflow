# visuAI Backend - Quick Test Guide

## 📝 Testing the Backend

### Option 1: Automated Setup (Recommended)

```bash
cd c:\dev\self-reinforcement\visuAI-tensorflow\backend
.\setup.bat
.\start.bat
```

### Option 2: Manual Setup

```bash
cd c:\dev\self-reinforcement\visuAI-tensorflow\backend

# Create venv
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

## 🧪 Testing Endpoints

Once server is running at `http://localhost:8000`:

### 1. Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0",
  "uptime": 12.34
}
```

### 2. Generate Description
```bash
curl -X POST http://localhost:8000/api/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"predictions\": [{\"className\": \"laptop\", \"probability\": 0.9}, {\"className\": \"desk\", \"probability\": 0.3}]}"
```

Expected response:
```json
{
  "text": "A laptop computer is visible in the image.",
  "confidence": 0.85,
  "processing_time": 0.023,
  "used_predictions": ["laptop", "desk"],
  "timestamp": "2026-02-01T21:10:00"
}
```

### 3. Ask Question
```bash
curl -X POST http://localhost:8000/api/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"predictions\": [{\"className\": \"cat\", \"probability\": 0.95}], \"question\": \"What animal is in the image?\"}"
```

Expected response:
```json
{
  "text": "The animal appears to be a cat.",
  "confidence": 0.9,
  "processing_time": 0.045,
  "question": "What animal is in the image?",
  "timestamp": "2026-02-01T21:10:00"
}
```

## 🌐 Browser Testing

1. **Open API Docs:**
   - Navigate to: `http://localhost:8000/docs`
   - Try the interactive Swagger UI

2. **Test Endpoints:**
   - Click "Try it out"
   - Enter sample data
   - Execute and see results

## ✅ Verification Checklist

- [ ] Server starts without errors
- [ ] Health check returns "healthy"
- [ ] `/api/describe` generates descriptions
- [ ] `/api/ask` answers questions
- [ ] No CORS errors (when called from Angular)
- [ ] Responses include confidence scores
- [ ] Processing times < 2 seconds

## 🐛 Common Issues

**Port 8000 in use:**
```
Edit .env: PORT=8001
```

**Module not found:**
```bash
pip install -r requirements.txt --upgrade
```

**Import errors:**
```bash
# Make sure you're in backend directory
cd visuAI-tensorflow\backend
python main.py
```
