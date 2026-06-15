import sys
sys.path.append("C:/pqa")

import pandas as pd
import re
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import PROCESSED_DATA_PATH, RAW_DATA_PATH

sia = SentimentIntensityAnalyzer()

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

def preprocess(input_path, output_path):
    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} records")

    features = df['prompt_text'].apply(extract_features).apply(pd.Series)
    df       = pd.concat([df, features], axis=1)

    df.to_csv(output_path, index=False)
    print(f"Saved processed data to {output_path}")
    print(df[['prompt_text', 'word_count', 'has_role', 'specificity']].to_string())

if __name__ == "__main__":
    preprocess(RAW_DATA_PATH, PROCESSED_DATA_PATH)