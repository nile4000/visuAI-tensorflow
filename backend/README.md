# OmniRL Backend API

FastAPI backend for visuAI image understanding with OmniRL vision-language model.

## 🚀 Quick Start

### Setup

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
```

2. **Activate environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your settings
```

5. **Run the server:**
```bash
python main.py
```

Server will start at `http://localhost:8000`

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔌 Endpoints

### Health Check
```http
GET /api/health
```

### Generate Description
```http
POST /api/describe
Content-Type: application/json

{
  "predictions": [
    {"className": "laptop", "probability": 0.9},
    {"className": "desk", "probability": 0.3}
  ]
}
```

### Ask Question
```http
POST /api/ask
Content-Type: application/json

{
  "predictions": [
    {"className": "cat", "probability": 0.95}
  ],
  "question": "What animal is in the image?"
}
```

## 🧪 Testing

### Using curl:

```bash
# Health check
curl http://localhost:8000/api/health

# Describe image
curl -X POST http://localhost:8000/api/describe \
  -H "Content-Type: application/json" \
  -d "{\"predictions\": [{\"className\": \"laptop\", \"probability\": 0.9}]}"

# Ask question
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"predictions\": [{\"className\": \"cat\", \"probability\": 0.95}], \"question\": \"What animal is this?\"}"
```

## 🔧 Configuration

Edit `.env` file:

```env
# Server
PORT=8000
HOST=0.0.0.0

# CORS (add your frontend URL)
ALLOWED_ORIGINS=http://localhost:4200

# Model (set to false when OmniRL is trained)
USE_MOCK_RESPONSES=true
```

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application
├── requirements.txt        # Dependencies
├── .env                    # Configuration
├── models/
│   └── schemas.py         # Pydantic models
├── services/
│   └── omni_service.py    # OmniRL service
└── training/
    ├── prepare_data.py    # Data preparation
    └── train_omni.py      # Model training
```

## 🎯 Current Status

✅ **Phase 1 Complete:**
- FastAPI structure created
- Mock responses for testing
- CORS configured
- API documentation

⏳ **Next Steps:**
- Train OmniRL model
- Replace mock responses
- Optimize inference speed

## 🐛 Troubleshooting

**Port already in use:**
```bash
# Change PORT in .env file
PORT=8001
```

**CORS errors:**
```bash
# Add your frontend URL to .env
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:4201
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```
