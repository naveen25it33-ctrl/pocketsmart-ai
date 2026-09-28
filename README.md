# PocketSmart AI

PocketSmart AI is a web-based smart budget and recommendation assistant. It lets a user enter monthly income and expenses, visualizes category spending, calculates remaining balance, and generates personalized recommendations with the Gemini API.

## Features
- Monthly income input
- Expense tracker with categories
- Automatic total expense and remaining-balance calculation
- Category spending doughnut chart
- Gemini-powered budget recommendations
- Local fallback analysis if Gemini is not configured
- Responsive UI
- API key stored in `.env`

## Requirements
- Python 3.10+
- A Gemini API key for AI recommendations

## Windows setup

1. Extract the ZIP.
2. Open Command Prompt / PowerShell inside the project folder.
3. Create a virtual environment:

   `python -m venv .venv`

4. Activate it:

   PowerShell:
   `.venv\Scripts\Activate.ps1`

   Command Prompt:
   `.venv\Scripts\activate`

5. Install packages:

   `pip install -r requirements.txt`

6. Copy `.env.example` to `.env`.
7. Put your Gemini API key into `.env`:

   `GEMINI_API_KEY=your_key_here`

8. Run:

   `python app.py`

9. Open:

   `http://127.0.0.1:5000`

## macOS / Linux

`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
`cp .env.example .env`
`python app.py`

Then open http://127.0.0.1:5000

## Gemini API

This project uses Google's current `google-genai` Python SDK and the `client.models.generate_content(...)` pattern documented by Google AI for Developers.

If the API key is missing or the AI request fails, PocketSmart automatically uses a local budget analysis so the application still works.

## Project structure

PocketSmart_AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css

## Notes

This is an educational/demo budgeting assistant, not financial advice. Keep API keys private.
