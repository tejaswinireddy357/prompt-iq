import os
import json
import re
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from groq import Groq
from dotenv import load_dotenv

load_dotenv("C:/pqa/.env")

try:
    import streamlit as st
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

sia    = SentimentIntensityAnalyzer()
client = Groq(api_key=GROQ_API_KEY)

def extract_features(prompt):
    words          = prompt.split()
    word_count     = len(words)
    avg_word_len   = sum(len(w) for w in words) / max(word_count, 1)
    has_role       = int(bool(re.search(r'\b(you are|act as|as a|as an)\b', prompt, re.I)))
    has_example    = int(bool(re.search(r'\b(example|e\.g\.|for instance|such as)\b', prompt, re.I)))
    has_format     = int(bool(re.search(r'\b(list|bullet|table|step|format|json|markdown)\b', prompt, re.I)))
    question_marks = prompt.count('?')
    sentiment      = sia.polarity_scores(prompt)['compound']
    flesch_score   = textstat.flesch_reading_ease(prompt)
    grade_level    = textstat.flesch_kincaid_grade(prompt)
    unique_words   = len(set(w.lower() for w in words))
    specificity    = round(unique_words / max(word_count, 1), 3)

    return {
        "word_count":     word_count,
        "sent_count":     prompt.count('.') + prompt.count('?') + prompt.count('!'),
        "avg_word_len":   round(avg_word_len, 2),
        "has_role":       has_role,
        "has_example":    has_example,
        "has_format":     has_format,
        "question_marks": question_marks,
        "sentiment":      round(sentiment, 3),
        "flesch_score":   round(flesch_score, 2),
        "grade_level":    round(grade_level, 2),
        "specificity":    specificity,
    }

def analyze_prompt(prompt):
    features = extract_features(prompt)

    system_msg = """You are an AI prompt quality evaluator.
Analyze the given prompt and return ONLY a valid JSON object with exactly these fields:
{
  "score": <float between 1.0 and 5.0>,
  "label": <"low" or "medium" or "high">,
  "tips": [<list of 2-4 specific improvement tips as strings>],
  "improved_prompt": <an improved version of the prompt as a string>
}
Rules:
- score 1.0-2.9 = low, 3.0-3.9 = medium, 4.0-5.0 = high
- tips must be specific and actionable
- improved_prompt must be a better version of the original
- Return ONLY the JSON object, no extra text"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": f"Analyze this prompt: {prompt}"}
            ],
            max_tokens=512,
            temperature=0.3
        )
        text      = response.choices[0].message.content.strip()
        text      = re.sub(r'```json|```', '', text).strip()
        ai_result = json.loads(text)

        return {
            "prompt":          prompt,
            "score":           float(ai_result.get("score", 3.0)),
            "label":           ai_result.get("label", "medium"),
            "tips":            ai_result.get("tips", ["No tips available"]),
            "improved_prompt": ai_result.get("improved_prompt", prompt),
            "features":        features,
        }

    except Exception as e:
        score = 1.0
        if features["has_role"]:         score += 1.0
        if features["has_example"]:      score += 0.5
        if features["has_format"]:       score += 0.5
        if features["word_count"] >= 10: score += 1.0
        score = round(min(max(score, 1.0), 5.0), 2)
        label = "high" if score >= 4 else ("medium" if score >= 3 else "low")
        return {
            "prompt":          prompt,
            "score":           score,
            "label":           label,
            "tips":            ["Add a role assignment", "Add output format", "Be more specific"],
            "improved_prompt": "You are an expert. " + prompt + " Respond in bullet points.",
            "features":        features,
        }

if __name__ == "__main__":
    result = analyze_prompt("tell me about python")
    print(f"Score: {result['score']} ({result['label']})")
    print("Tips:")
    for tip in result['tips']:
        print(f"  - {tip}")
    print(f"Improved: {result['improved_prompt']}")