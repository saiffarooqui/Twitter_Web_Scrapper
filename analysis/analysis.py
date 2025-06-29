import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from gensim import corpora, models

# CONFIG
CLEANED_CSV = os.path.join("data", "tweets_cleaned.csv")
REPORT_DIR = "reports"
NUM_TOPICS = 5


def load_data(path=CLEANED_CSV):
    df = pd.read_csv(path, parse_dates=[["date", "time"]])
    df.rename(columns={"date_time": "timestamp"}, inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def sentiment_analysis(df):
    df["tweet"] = df["tweet"].fillna("").astype(str)
    analyzer = SentimentIntensityAnalyzer()
    df["compound"] = df["tweet"].apply(
        lambda t: analyzer.polarity_scores(t)["compound"]
    )
    bins = [-1.0, -0.05, 0.05, 1.0]
    labels = ["negative", "neutral", "positive"]
    df["sentiment"] = pd.cut(df["compound"], bins=bins, labels=labels)
    return df


def topic_modeling(df, num_topics=NUM_TOPICS):
    texts = [re.findall(r"\w+", t.lower()) for t in df["tweet"]]
    dictionary = corpora.Dictionary(texts)
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        random_state=42,
        passes=10,
        alpha="auto",
        eta="auto",
    )
    # dominant topic per doc
    topics_per_doc = []
    for bow in corpus:
        tmp = lda.get_document_topics(bow)
        topics_per_doc.append(max(tmp, key=lambda x: x[1])[0] if tmp else -1)
    df["topic"] = topics_per_doc

    # build a dict of top-3 keywords for each topic
    topics = {t: [w for w, _ in lda.show_topic(t, topn=3)] for t in range(num_topics)}

    print("\n=== LDA Topics (top-3 words) ===")
    for t, words in topics.items():
        print(f"Topic {t}: {', '.join(words)}")
    print("================================\n")

    return df, topics


def plot_and_save(df, topics):
    os.makedirs(REPORT_DIR, exist_ok=True)
    sns.set(style="whitegrid")

    # Sentiment Distribution
    plt.figure(figsize=(6, 4))
    ax1 = sns.countplot(
        x="sentiment", data=df, order=["positive", "neutral", "negative"]
    )
    ax1.set_title("Tweet Sentiment Distribution")
    ax1.set_xlabel("Sentiment")
    ax1.set_ylabel("Number of Tweets")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "sentiment_dist.png"))
    plt.close()

    # Topic Distribution with legend
    plt.figure(figsize=(6, 4))
    palette = sns.color_palette("tab10", n_colors=len(topics))
    ax2 = sns.countplot(x="topic", data=df, palette=palette)
    ax2.set_title("Tweet Topic Distribution")
    ax2.set_xlabel("Topic ID")
    ax2.set_ylabel("Number of Tweets")

    patches = [
        Patch(color=palette[i], label=f"Topic {i}: {', '.join(topics[i])}")
        for i in range(len(topics))
    ]
    ax2.legend(
        handles=patches,
        title="Topics (top 3 words)",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
    )
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "topic_dist.png"))
    plt.close()

    # Tweets Over Time
    df_time = df.set_index("timestamp")
    ts = df_time.resample("1D").size()
    plt.figure(figsize=(8, 4))
    ts.plot(color="tab:blue")
    plt.title("Tweets Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Tweets")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "timeline.png"))
    plt.close()

    # Top 10 Hashtags
    df_reset = df.reset_index(drop=True)
    all_tags = df_reset["hashtags"].str.split(",", expand=True).stack()
    top_tags = all_tags.value_counts().head(10)
    plt.figure(figsize=(6, 4))
    ax4 = sns.barplot(x=top_tags.values, y=top_tags.index, palette="magma")
    ax4.set_title("Top 10 Hashtags")
    ax4.set_xlabel("Count")
    ax4.set_ylabel("Hashtag")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "top_hashtags.png"))
    plt.close()


def main():
    import nltk

    nltk.download("stopwords", quiet=True)

    df = load_data()
    df = sentiment_analysis(df)
    df, topics = topic_modeling(df)
    plot_and_save(df, topics)
    df.to_csv(os.path.join("data", "tweets_final.csv"), index=False)
    print("Analysis complete. Charts in /reports and data/tweets_final.csv")


if __name__ == "__main__":
    main()
