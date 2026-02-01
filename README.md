# visuAI-tensorflow

**Intelligent Image Recognition with OmniRL Vision-Language Understanding**

![visuAI Screenshot](./src/assets/img/screenshot.png "visuAI")

## 📋 Overview

visuAI is an advanced image recognition system that combines:
- **Frontend:** Angular app with TensorFlow.js (MobileNet) for fast classification
- **Backend:** FastAPI + OmniRL for intelligent descriptions and Q&A

## 🚀 Quick Start

### Frontend Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Run development server:**
```bash
ng serve
```

Visit `http://localhost:4200`

### Backend Setup

1. **Navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
copy .env.example .env
```

5. **Run server:**
```bash
python main.py
```

API available at `http://localhost:8000`

## 🏗️ Architecture

```
Image Upload → MobileNet (Browser) → Predictions
                                          ↓
                                    FastAPI Backend
                                          ↓
                                    OmniRL Model
                                          ↓
                              Description + Q&A ← User
```

## ✨ Features

### Frontend
- **Fast Classification:** TensorFlow.js runs in browser (no server needed)
- **Real-time Results:** Instant prediction probabilities
- **Modern UI:** Angular Material design

### Backend
- **Smart Descriptions:** Converts predictions to natural language
- **Visual Q&A:** Answer questions about images
- **Caching:** Fast responses for repeated queries

## 📖 Documentation

- **Frontend:** See Angular docs
- **Backend API:** `http://localhost:8000/docs` (when running)
- **Implementation Plan:** See project artifacts

## 🔧 Tech Stack

- **Frontend:** Angular 18, TensorFlow.js, Material UI
- **Backend:** Python, FastAPI, PyTorch (OmniRL)
- **ML Models:** MobileNet (classification), Qwen2.5-VL-3B (VQA)

## 📂 Project Structure

```
visuAI-tensorflow/
├── src/                    # Angular frontend
│   ├── app/
│   │   ├── components/
│   │   └── services/
│   └── assets/
├── backend/               # FastAPI backend
│   ├── main.py
│   ├── models/
│   ├── services/
│   └── training/
└── ...
```

## 🎯 Current Status

✅ **Phase 1:** Backend structure complete (mock mode)  
⏳ **Phase 2:** OmniRL training in progress  
⏳ **Phase 3:** Frontend integration  

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! This is an experimental project for vision-language integration.
