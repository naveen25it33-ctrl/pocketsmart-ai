import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

try:
    from google import genai
except ImportError:
    genai = None

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

def local_recommendation(data):
    income = float(data.get("income", 0) or 0)
    expenses = data.get("expenses", [])
    total = sum(float(x.get("amount", 0) or 0) for x in expenses)
    balance = income - total
    by_cat = {}
    for x in expenses:
        c = x.get("category", "Other")
        by_cat[c] = by_cat.get(c, 0) + float(x.get("amount", 0) or 0)
    largest = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)[:3]
    lines = [
        f"Monthly income: ₹{income:,.2f}",
        f"Total expenses: ₹{total:,.2f}",
        f"Remaining balance: ₹{balance:,.2f}",
    ]
    if largest:
        lines.append("Largest spending categories: " + ", ".join(f"{c} (₹{v:,.0f})" for c,v in largest))
    if balance < 0:
        lines.append("Your expenses are above income. Review non-essential spending first.")
    elif income > 0 and balance < income * 0.1:
        lines.append("Your remaining balance is below 10% of income. Consider setting a small savings target.")
    else:
        lines.append("You have positive cash flow. Consider assigning part of the balance to savings.")
    return "\n".join(lines)

def ai_recommendation(data):
    if not GEMINI_API_KEY or genai is None:
        return local_recommendation(data), False
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""
You are PocketSmart AI, a friendly personal budgeting assistant.
Analyze the user's monthly budget data below and give practical, non-judgmental recommendations.
Do not make investment, loan, tax, or other regulated financial recommendations.
Use Indian rupees and concise headings.
Include:
1. Budget snapshot
2. Spending observations
3. 3 practical actions
4. A simple savings target
5. One caution if spending is high
Data:
{data}
"""
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return (response.text or local_recommendation(data)), True
    except Exception as e:
        return local_recommendation(data) + f"\n\nAI service unavailable right now; local analysis was used.", False

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/recommend")
def recommend():
    data = request.get_json(silent=True) or {}
    result, used_ai = ai_recommendation(data)
    return jsonify({"recommendation": result, "ai": used_ai})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
