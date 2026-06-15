import os
from dotenv import load_dotenv
load_dotenv("C:/pqa/.env")

GROQ_API_KEY        = os.getenv("GROQ_API_KEY")
RAW_DATA_PATH       = "data/raw/prompts.csv"
PROCESSED_DATA_PATH = "data/processed/features.csv"
RATED_DATA_PATH     = "data/rated/rated_prompts.csv"
MODEL_PATH          = "models/quality_predictor.pkl"