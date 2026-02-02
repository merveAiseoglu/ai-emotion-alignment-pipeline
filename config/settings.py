import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

AI_MODEL = "gpt-3.5-turbo" # veya gpt-4-turbo (Evaluator için GPT-4 önerilir ama 3.5 da çalışır)

# Hedeflenen Duygu Seti (Sınırlı ve Net)
TARGET_EMOTIONS = [
    "Happy (Mutlu/Umutlu)",
    "Tragic (Trajik/Yıkıcı)",
    "Melancholic (Hüzünlü/Buruk)",
    "Suspenseful (Gerilimli/Belirsiz)"
]