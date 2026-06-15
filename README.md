# ⚡ Prompt Quality Analyzer

A Data Science and NLP powered web application that analyzes the quality of AI prompts, scores them from 1 to 5, and provides actionable improvement tips using live AI analysis.

## 🔗 Links

| Resource | Link |
|---|---|
| Live App | https://prompt-iq-app.streamlit.app |
| GitHub | https://github.com/tejaswinireddy357/prompt-iq |

---

## 📋 Overview

When people use AI tools like ChatGPT or Claude, they often get poor results because their prompts are weak. This tool acts like a grammar checker but for AI prompts — it tells you exactly what is wrong and how to fix it.

### Example

| Prompt Type | Example | Score |
|---|---|---|
| ❌ Bad | `tell me about python` | 1-2 (LOW) |
| ✅ Good | `You are a Python expert. Explain lists vs tuples with code examples in bullet points.` | 4-5 (HIGH) |

---

## ✅ Key Features

| Feature | Description |
|---|---|
| Instant Scoring | Scores any prompt from 1 to 5 in real time |
| AI Powered Tips | Live improvement suggestions using Groq LLaMA 3 |
| Improved Prompt | Auto-generates a better version of your prompt |
| History Tab | Saves all analyzed prompts with scores |
| Compare Mode | Analyze two prompts side by side |
| Templates | 6 pre-built high quality prompt templates |

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python | Main programming language |
| Groq API (LLaMA 3) | Live AI prompt analysis and rating |
| Streamlit | Web dashboard and UI |
| Pandas | Data handling and CSV processing |
| Scikit-learn | Random Forest ML model training |
| textstat | Readability score extraction |
| vaderSentiment | Sentiment analysis of prompts |
| Joblib | Saving and loading trained ML model |
| python-dotenv | Secure API key management |
| GitHub | Version control and code storage |
| Streamlit Cloud | Free deployment and hosting |

---

## 🏗 Architecture

```
collect.py       →   Collects prompt-response pairs from Groq API
      ↓
preprocess.py    →   Extracts 11 NLP features from each prompt
      ↓
rate.py          →   Scores each prompt 1-5 with quality labels
      ↓
analyze.py       →   Trains Random Forest ML model on scored data
      ↓
insights.py      →   Live AI analysis using Groq API
      ↓
dashboard.py     →   Beautiful Streamlit web dashboard
```

---

## 📂 Repository Structure

```
pqa/
├── data/
│   ├── raw/               ← Raw prompt-response pairs from Groq API
│   ├── processed/         ← Cleaned data with NLP features extracted
│   └── rated/             ← Data with quality scores and labels
├── models/                ← Saved trained ML model (.pkl file)
├── src/
│   ├── collect.py         ← Phase 1: Collect data from Groq API
│   ├── preprocess.py      ← Phase 2: Clean data and extract NLP features
│   ├── rate.py            ← Phase 3: Score each prompt 1-5
│   ├── analyze.py         ← Phase 4: Train ML model
│   ├── insights.py        ← Phase 5: Generate AI powered improvement tips
│   └── api.py             ← FastAPI backend
├── config.py              ← Settings file with all paths
├── .env                   ← Secret API key (never uploaded to GitHub)
├── dashboard.py           ← Phase 6: Streamlit web dashboard
└── requirements.txt       ← All required libraries
```

---

## 🚀 Pipeline Phases

| Phase | File | What It Does |
|---|---|---|
| Phase 1 | collect.py | Sends prompts to Groq AI and saves responses to CSV |
| Phase 2 | preprocess.py | Extracts 11 NLP features from each prompt |
| Phase 3 | rate.py | Scores prompts 1-5 and labels them low/medium/high |
| Phase 4 | analyze.py | Trains Random Forest model on scored data |
| Phase 5 | insights.py | Uses Groq AI live to generate improvement tips |
| Phase 6 | dashboard.py | Beautiful 4-tab Streamlit web interface |

---

## 📊 NLP Features Extracted

| Feature | What It Measures |
|---|---|
| word_count | Number of words in prompt |
| sent_count | Number of sentences |
| avg_word_len | Average length of words |
| has_role | Does prompt have "You are an expert"? (1/0) |
| has_example | Does prompt have "for example"? (1/0) |
| has_format | Does prompt specify output format? (1/0) |
| question_marks | Number of question marks |
| sentiment | Positive/negative tone (-1 to 1) |
| flesch_score | Readability score (0-100) |
| grade_level | Reading grade level |
| specificity | Ratio of unique words |

---

## ⚡ Quick Start

### Prerequisites

```bash
# Python 3.10+ required
python --version
```

### Setup

```bash
# Clone repository
git clone https://github.com/tejaswinireddy357/prompt-iq.git
cd prompt-iq

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Add API Key

Create a `.env` file in the root folder:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Get your free Groq API key at: https://console.groq.com

### Run All Phases

```bash
# Phase 1 — Collect data
python src/collect.py

# Phase 2 — Preprocess
python src/preprocess.py

# Phase 3 — Rate prompts
python src/rate.py

# Phase 4 — Train model
python src/analyze.py

# Phase 5 — Test insights
python src/insights.py

# Phase 6 — Launch dashboard
streamlit run dashboard.py
```

---

## 📱 Dashboard Features

| Tab | What It Does |
|---|---|
| ⚡ Analyze | Score any prompt instantly with AI tips and improved version |
| 📊 History | View all previously analyzed prompts with scores |
| ⚖️ Compare | Enter two prompts and see which one wins |
| 📋 Templates | 6 ready-made high quality prompt templates |

---

## 🚀 Deployment

This project is deployed on **Streamlit Cloud** — free hosting for Python web apps.

### Steps

1. Push code to GitHub (without `.env`, `venv`, `models`, `data` folders)
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Set `dashboard.py` as main file
5. Add `GROQ_API_KEY` in Advanced Settings → Secrets
6. Click Deploy — live in 2-3 minutes!

---

## 🔑 Required Secrets

| Secret | Purpose |
|---|---|
| GROQ_API_KEY | Groq API key for live AI prompt analysis |

---

## 🧠 ML Model Details

| Property | Value |
|---|---|
| Model Type | Random Forest Regressor |
| Features Used | 11 NLP features |
| Training Data | 10 prompt-response pairs |
| Output | Quality score (1.0 to 5.0) |
| Top Features | word_count, has_role, sent_count |

---

## 📈 Scoring System

| Score Range | Label | Meaning |
|---|---|---|
| 1.0 — 2.9 | 🔴 LOW | Weak prompt — needs major improvement |
| 3.0 — 3.9 | 🟡 MEDIUM | Average prompt — can be improved |
| 4.0 — 5.0 | 🟢 HIGH | Strong prompt — well structured |

---

## 👩‍💻 Author

**Tejaswini Katipally**

- Live App: https://prompt-iq-app.streamlit.app
- GitHub: https://github.com/tejaswinireddy357/prompt-iq
