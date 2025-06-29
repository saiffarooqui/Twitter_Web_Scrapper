import re
import pandas as pd
from langdetect import detect, DetectorFactory
import nltk
from nltk.corpus import stopwords

# Config
RAW_CSV = "data/tweets_scrape_raw.csv"
CLEAN_CSV = "data/tweets_cleaned.csv"

DetectorFactory.seed = 0

nltk.download("stopwords")

STOP_WORDS = set(stopwords.words("english"))


def is_english(text: str) -> bool:
    """Return True if langdetect thinks this is an English text."""
    try:
        return detect(text) == "en"
    except:
        return False


def clean_text(text: str) -> str:
    """Lowercase, strip URLs, mentions/hashtags, non-alpha, remove stop-words."""
    if not isinstance(text, str):
        return ""
    s = text.lower()
    # remove URLs
    s = re.sub(r"http\S+|www\.\S+", "", s)
    # remove mentions and hashtags
    s = re.sub(r"@\w+", "", s)
    s = re.sub(r"#\w+", "", s)
    # keep only letters and spaces
    s = re.sub(r"[^a-z\s]", " ", s)
    # collapse whitespace
    tokens = s.split()
    # remove stop words and one-letter tokens
    tokens = [w for w in tokens if w not in STOP_WORDS and len(w) > 1]
    return " ".join(tokens)


def main():
    # Load raw data
    df = pd.read_csv(RAW_CSV, dtype=str)

    # Filter to English tweets only
    df["is_english"] = df["tweet"].fillna("").apply(is_english)
    df = df[df["is_english"]].drop(columns=["is_english"])

    # Clean the tweet text in-place
    df["tweet"] = df["tweet"].apply(clean_text)

    # Write out cleaned CSV with identical columns
    df.to_csv(CLEAN_CSV, index=False, encoding="utf-8")
    print(f"Cleaned {len(df)} English tweets → {CLEAN_CSV}")


if __name__ == "__main__":
    main()
