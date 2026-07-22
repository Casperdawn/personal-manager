# Personal Manager

A personal management system built with Vue 3 + FastAPI, including learning management, weight loss tracking, finance management, and todo tasks.

## Features

- **Learning Management**: Add learning projects, track estimated time and accumulated study duration
- **Weight Loss Tracking**: Record daily weight, view weight change trend chart
- **Finance Management**: Track income and expenses, view monthly statistics
- **Todo Tasks**: Add, complete, and manage daily tasks
- **User Authentication**: Login/Register system

## Tech Stack

### Frontend
- Vue 3 + Vite
- Element Plus
- Vue Router
- Axios

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+

---

## Running on Windows (via Trae)

### Step 1: Clone the project

```bash
git clone https://github.com/Casperdawn/personal-manager.git
cd personal-manager
```

### Step 2: Install Node.js (if not installed)

If you get "npm is not recognized", you need to install Node.js first:

1. Download Node.js from https://nodejs.org/ (LTS version recommended)
2. Run the installer and make sure to check "Add to PATH"
3. Restart Trae terminal

### Step 3: Build frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 4: Set up Python virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### Step 5: Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Initialize database

```bash
python init_sample_data.py
```

### Step 7: Start the server

```bash
python main.py
```

### Step 8: Access the application

Open browser and visit: **http://localhost:8000**

---

## Running on macOS/Linux

```bash
git clone https://github.com/Casperdawn/personal-manager.git
cd personal-manager
./build.sh
```

---

## Running on Windows (Alternative - using build.bat)

```bash
git clone https://github.com/Casperdawn/personal-manager.git
cd personal-manager
build.bat
```

---

## Project Structure

```
personal-manager/
├── backend/                  # Backend code
│   ├── app/                  # Application core
│   │   ├── core/             # Configuration and database
│   │   ├── models/           # Data models
│   │   ├── routes/           # API routes
│   │   ├── schemas/          # Data validation
│   │   └── utils/            # Utility functions
│   ├── main.py               # Entry file
│   └── requirements.txt      # Python dependencies
├── frontend/                 # Frontend code
│   ├── src/                  # Source code
│   │   ├── views/            # Page components
│   │   ├── api/              # API calls
│   │   └── router/           # Route configuration
│   └── package.json          # Node.js dependencies
├── build.bat                 # Windows build script
├── build.sh                  # macOS/Linux build script
└── README.md                 # Documentation
```

## Default Account

- Username: **hzs**
- Password: **123**

## Troubleshooting

### "npm is not recognized"

1. Install Node.js from https://nodejs.org/
2. Restart your terminal
3. Verify installation: `node --version` and `npm --version`

### Python virtual environment activation fails

```bash
# Try this if venv\Scripts\activate doesn't work
.\venv\Scripts\activate
```

### Port 8000 is already in use

```bash
# Find and kill the process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Slow npm/pip installation

```bash
# Use Chinese mirrors
npm config set registry https://registry.npmmirror.com
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## License

MIT
