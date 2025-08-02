# LLM Startup Report Generator

This Streamlit app uses CrewAI to simulate a team of agents who plan, research, and write a market report on LLM startups.

## Features

- 🧠 LLM-based planner, researcher, and writer agents
- 🌐 Real-time search using SerpAPI
- 📊 Generates a structured market research report
- 🖥️ Web-based interface using Streamlit

## Setup

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/llm-startup-report.git
cd llm-startup-report
```

2. **Create and activate virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Add `.env` file:**

```env
GROQ_API_KEY=your_groq_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

5. **Run the app:**

```bash
streamlit run app.py
```

## License

MIT License
