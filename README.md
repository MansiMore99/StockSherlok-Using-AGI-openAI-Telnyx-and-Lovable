
<img width="1536" height="1024" alt="project_!" src="https://github.com/user-attachments/assets/a6716a05-7f03-4c8d-97b1-4d368f749c88" />

## 🚀 What Is StockSherlok?

**StockSherlok** is an autonomous AI research agent designed to uncover fast-growing, under-the-radar companies that traditional stock dashboards overlook. While everyone invests in the same 10–20 famous companies, thousands of mid-cap and emerging tech players (AI, robotics, biotech, cybersecurity, hardware) are quietly scaling — and often impossible to discover manually.

StockSherlok works like a financial detective.
It fetches market data, analyzes patterns, and summarizes growth signals so users can track early opportunities without needing expert knowledge.

**This is not financial advice — it’s an intelligence tool for exploration and discovery.**
---

## 🔍 Why We Built It

- Most retail investors only track big-tech stocks.  
- High-growth, underrated companies are hard to discover.  
- Manual research is time-consuming and requires domain knowledge.  
- Our agent automates the discovery process and returns easy-to-read insights.  
- Voice-enabled via Telnyx makes the experience hands-free and futuristic.  

---

## 🧰 Key Features

- 🔧 **AGI Agent** – Multi-step automation on the AGI SDK  
- 📈 **Stock Data Intelligence** – Fetches and analyzes real market data  
- 📊 **Growth Analysis** – Computes momentum, volatility, and a “growth score”  
- 💬 **Insight Generation** – OpenAI transforms raw data into actionable summaries  
- 🖥️ **Lovable UI** – Clean, interactive frontend  
- 🎙️ **Voice Interaction** – Ask questions through Telnyx

---

## 🧭 How It Works

1. **User Query**  
   User asks about a company or ticker.

2. **Agent Tools**  
   The AGI agent calls a stock lookup tool to pull real price history.

3. **Metric Calculation**  
   Computes trends, volatility, percent changes, etc.

4. **LLM Reasoning**  
   OpenAI analyzes data and generates rankings + explanations.

5. **UI + Voice Output**  
   The Lovable frontend visualizes insights.  
   Telnyx can speak insights back to the user.

---

## 🧪 Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | AGI SDK |
| LLM Reasoning | OpenAI API |
| UI | Lovable |
| Voice | Telnyx |
| Data Source | Alpha Vantage or Finnhub |

---

## 🎯 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/stocksherlok.git
cd stocksherlok
```
### 2. Environment Variables

Create .env:
```
OPENAI_API_KEY=your_key
ALPHA_VANTAGE_KEY=your_key
TELNYX_API_KEY=optional
```

### 3. Install Dependencies
```
uv sync
```

### 4. Run Benchmark
```bash
uv run ./scripts/bench.py
```

### 5. Run Lovable Frontend
```bash
cd frontend
lovable dev
```

## 🔮 Demo Flow
1. “Analyze CRWD.”
2. Agent fetches the last 30 days of CRWD data.
3. Computes growth indicators.
4. OpenAI generates a growth score + reasoning.
5. UI displays charts + insights.
6. Voice output optional.

## ⚠️ Disclaimer
This project is for education and hackathon demonstration only.
Not financial advice.

## 📚 Contributing

PRs welcome! Improve tools, UI, or reasoning logic.

## 📄 License

MIT License.

