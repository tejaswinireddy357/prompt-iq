import sys
sys.path.append("C:/pqa")

import csv
import time
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv("C:/pqa/.env")

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
RAW_DATA_PATH = "data/raw/prompts.csv"

print(f"API Key loaded: {GROQ_API_KEY[:10]}..." if GROQ_API_KEY else "NO API KEY FOUND")

client = Groq(api_key=GROQ_API_KEY)

SAMPLE_PROMPTS = [
    "tell me stuff about python",
    "explain AI",
    "write something",
    "help me with code",
    "What are the key differences between Python lists and tuples?",
    "Explain the concept of recursion with a simple example.",
    "Write a function to reverse a string in Python.",
    "You are a Python expert. Explain the difference between generators and iterators in Python 3, including memory implications. Provide a code example for each.",
    "As a data scientist, describe 3 common preprocessing steps before training a machine learning model. For each step explain why it matters and show a pandas code snippet.",
    "Write a Python class implementing a stack data structure with push, pop, peek, and is_empty methods. Include docstrings and handle edge cases.",
]

def collect_prompt_response(prompt):
    start = time.time()
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        text    = response.choices[0].message.content
        latency = round(time.time() - start, 2)
        tokens  = response.usage.total_tokens
        return {
            "prompt_text":   prompt,
            "response_text": text,
            "latency_sec":   latency,
            "token_count":   tokens,
            "model":         "llama-3.3-70b-versatile",
            "prompt_length": len(prompt.split()),
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def collect_dataset(prompts, output_path):
    results = []
    for i, prompt in enumerate(prompts):
        print(f"Collecting {i+1}/{len(prompts)}: {prompt[:50]}...")
        record = collect_prompt_response(prompt)
        if record:
            results.append(record)
        time.sleep(1)

    if not results:
        print("No results collected. Check your API key.")
        return

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} records to {output_path}")

if __name__ == "__main__":
    collect_dataset(SAMPLE_PROMPTS, RAW_DATA_PATH)