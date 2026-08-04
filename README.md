# Portfolio Manager Dashboard

A full-stack web application used to track and analyze your stock portfolio. This project features a **Next.js** frontend for an interactive dashboard and a **Flask** backend for data processing, financial analysis, and portfolio management.

## Technologies

### Frontend
- **Next.js 16**: React framework for production.
- **React 19**: UI library.
- **Tailwind CSS v4**: Utility-first CSS framework.
- **TypeScript**: Static typing for JavaScript.
- **Plotly.js**: Interactive charting.

### Backend
- **Flask**: Lightweight WSGI web application framework.
- **Python 3.14+**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **yfinance**: Yahoo Finance API for stock data.
- **Matplotlib/Plotly**: Data visualization.
- **Redis**: Server-side session management.
- **SQLite**: Local database for portfolio storage.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Redis**: Required for backend session management.
  - *Mac (Homebrew)*: `brew install redis`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ravadashreyas/Portfolio-Manager.git
cd Portfolio-Manager
```

### 2. Backend Setup

Navigate to the `server` directory and set up the Python environment.

```bash
cd server

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# OR if you use uv
# uv sync

# Return to root
cd ..
```

### 3. Frontend Setup

Navigate to the `my-stock-portfolio` directory and install dependencies.

```bash
cd my-stock-portfolio
npm install
```

### 4. Environment Configuration

The backend requires environment variables defined in a `.env` file. You must create this file in the `server/` directory to ensure variables are loaded correctly.

Create a file named `.env` inside `server/` with the following content:

```env
SECRET_KEY=your_secret_key_here
REDIS_URL=redis://localhost:6379
```

## Running the Application

To run the full stack, you will need **three** terminal windows.

### Terminal 1: Redis

Start the Redis server if it is not already running.

```bash
redis-server
```

### Terminal 2: Backend (Flask)

```bash
cd server
source .venv/bin/activate  # Ensure venv is active
python app.py
```
The backend will start on `http://localhost:5000`.

### Terminal 3: Frontend (Next.js)

```bash
cd my-stock-portfolio
npm run dev
```
The frontend will start on `http://localhost:3000`.

##  Project Structure

- **`my-stock-portfolio/`**: Next.js frontend application.
  - `app/`: Next.js App Router pages and layouts.
  - `components/`: Reusable React components.
- **`server/`**: Flask backend application.
  - `app.py`: Entry point for the Flask app.
  - `routes/`: API endpoints (`/api` and `/api/auth`).
  - `methods/`: Business logic for stock analysis and data fetching.
  - `data/`: SQLite database file (generated).

## Troubleshooting

### API Requests Failing (404)
If frontend requests to `/api/...` are failing with 404 errors:
1. Ensure the Flask backend is running on port 5000.
2. Check if **`next.config.ts`** exists in `my-stock-portfolio/`. If it is empty, it may be overriding `next.config.js` (which contains the proxy rules). You may need to migrate the configuration to `.ts` or delete the empty file.

### Environment Variables Not Loading
- Ensure `.env` is in the `server/` directory, not just the root.
- Ensure you are activating the virtual environment before running the backend.
