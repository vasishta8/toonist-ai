# Toonist AI

Toonist AI is an end-to-end pipeline for generating educational comic books from a user-provided topic. It uses large language models (LLMs) to generate stories and image prompts, then composes comic panels and exports the final comic as a PDF. The project features a Python backend for story and image generation, and a React frontend for user interaction and PDF viewing.

## Features
- Generate comic stories from any topic using LLMs
- Automatically create image prompts and generate images for each comic panel
- Compose images and dialogues into comic page layouts
- Export the final comic as a PDF
- Simple web interface for user input and PDF viewing

## Prerequisites
- Python 3.8+
- Node.js (v16 or newer recommended)
- npm (Node package manager)

## Setup Instructions

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd toonist-ai
```

### 2. Set up the Python backend
```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

- Make sure to set up your `.env` file in the `backend/` directory with the required API keys (e.g., `GROQ_API_KEY`).

### 3. Start the Python backend server
```sh
python server.py
```

The backend will run on `http://127.0.0.1:5000` by default.

### 4. Set up the React frontend
```sh
cd ../frontend
npm install
```

### 5. Start the React development server
```sh
npm run dev
```

The frontend will run on `http://localhost:5173` by default.

## Usage
1. Open the frontend in your browser (`http://localhost:5173`).
2. Enter a topic or story idea and submit.
3. Wait for the backend to generate the comic and PDF.
4. Use the PDF viewer to fetch and view your generated comic.

## Notes
- Ensure both backend and frontend servers are running for full functionality.
- You may need to adjust CORS settings or API URLs if running on different hosts/ports.

## License
MIT License
