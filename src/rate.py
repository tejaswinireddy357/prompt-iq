import sys
sys.path.append("C:/pqa")

import pandas as pd
import re
from config import PROCESSED_DATA_PATH, RATED_DATA_PATH

def rate_prompt(row):
    prompt   = str(row['prompt_text'])
    response = str(row['response_text'])
    score    = 0

    # Rule 1 — word count
    wc = len(prompt.split())
    if 10 <= wc <= 40:
        score += 2
    elif 5 <= wc < 10:
        score += 1
    else:
        score += 0.5

    # Rule 2 — has role
    if re.search(r'\b(you are|act as|as a|as an)\b', prompt, re.I):
        score += 1

    # Rule 3 — has example
    if re.search(r'\b(example|e\.g\.|for instance|such as)\b', prompt, re.I):
        score += 0.5

    # Rule 4 — has format instruction
    if re.search(r'\b(list|bullet|table|step|format|json|markdown)\b', prompt, re.I):
        score += 0.5

    # Rule 5 — response length
    if len(response.split()) > 30:
        score += 1

    # Normalize to 1-5 scale
    quality_score = round(min(max(score, 1.0), 5.0), 2)

    # Label
    if quality_score >= 4:
        label = 'high'
    elif quality_score >= 3:
        label = 'medium'
    else:
        label = 'low'

    return pd.Series({
        'relevance':     round(min(score * 1.1, 5), 2),
        'coherence':     round(min(score * 0.9, 5), 2),
        'completeness':  round(min(score, 5), 2),
        'quality_score': quality_score,
        'quality_label': label
    })

def rate_dataset(input_path, output_path):
    df = pd.read_csv(input_path)
    print(f"Rating {len(df)} records...")

    ratings = df.apply(rate_prompt, axis=1)
    df      = pd.concat([df, ratings], axis=1)

    df.to_csv(output_path, index=False)
    print(f"Saved rated data to {output_path}")
    print(df[['prompt_text', 'quality_score', 'quality_label']].to_string())

if __name__ == "__main__":
    rate_dataset(PROCESSED_DATA_PATH, RATED_DATA_PATH)