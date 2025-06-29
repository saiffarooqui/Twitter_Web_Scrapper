import os
import time
import re
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# ─── CONFIG ──────────────────────────
SEARCH_QUERY = "%23naukri%20OR%20%23jobs%20OR%20%23jobseeker%20OR%20%23vacancy"
MAX_TWEETS = 2100
SCROLL_PAUSE = 1.5
OUTPUT_CSV = "data/tweets_scrape_raw.csv"
# ─────────────────────────────────────

load_dotenv()
USERNAME = os.getenv("TWITTER_USERNAME")
PASSWORD = os.getenv("TWITTER_PASSWORD")


def init_driver():
    chrome_options = Options()

    # Creating a dedicated test profile
    chrome_options.add_argument(
        f"--user-data-dir={os.path.expanduser('~')}/.twitter_scraper_profile"
    )
    chrome_options.add_argument("--profile-directory=TwitterProfile")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


def login(driver):
    driver.get("https://twitter.com/login")
    time.sleep(3)

    email_input = driver.find_element(By.NAME, "text")
    email_input.send_keys(USERNAME)
    email_input.send_keys(Keys.RETURN)
    time.sleep(3)

    try:
        pw_input = driver.find_element(By.NAME, "password")
    except:
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(USERNAME)
        username_input.send_keys(Keys.RETURN)
        time.sleep(2)
        pw_input = driver.find_element(By.NAME, "password")

    pw_input.send_keys(PASSWORD)
    pw_input.send_keys(Keys.RETURN)
    time.sleep(5)


def extract_card_data(card):
    from datetime import datetime
    import re

    try:
        # Extracting Tweet Text
        try:
            tweet_container = card.find_element(
                By.XPATH, ".//div[@data-testid='tweetText']"
            )
            spans = tweet_container.find_elements(By.XPATH, ".//span")
            text = " ".join(span.text.strip() for span in spans if span.text.strip())
        except:
            return None

        # Extracting Username
        try:
            username_el = card.find_element(
                By.XPATH, ".//div[@dir='ltr']//span[contains(text(), '@')]"
            )
            username = username_el.text.strip("@")
        except:
            username = "unknown"

        # extract timestamp
        try:
            time_tag = card.find_element(By.XPATH, ".//time")
            dt = datetime.fromisoformat(
                time_tag.get_attribute("datetime").replace("Z", "+00:00")
            )
            date, time_ = dt.date().isoformat(), dt.time().isoformat()
        except:
            return None

        # Extract mentions and hashtags
        mentions = ",".join(re.findall(r"@(\w+)", text))
        hashtags = ",".join(re.findall(r"#(\w+)", text))

        # Extract other metrics likes, views, retweets, comments
        likes = retweets = comments = replies = views = 0
        try:
            metric_div = card.find_element(
                By.XPATH, ".//div[@aria-label and contains(@aria-label, 'view')]"
            )
            label = metric_div.get_attribute("aria-label").lower()

            def extract(label, keyword):
                match = re.search(r"(\d+)\s+" + keyword, label)
                return int(match.group(1)) if match else 0

            retweets = extract(label, "repost")
            likes = extract(label, "like")
            views = extract(label, "view")
            comments = extract(label, "repl")
            replies = extract(label, "quote")

        except Exception as e:
            print(f"Could not extract metrics: {e}")

        return {
            "username": username,
            "tweet": text,
            "date": date,
            "time": time_,
            "mentions": mentions,
            "hashtags": hashtags,
            "likes": likes,
            "retweets": retweets,
            "comments": comments,
            "replies": replies,
            "views": views,
        }

    except Exception as e:
        print(f"Error extracting tweet: {e}")
        return None


def scrape_tweets(driver):
    tweet_data = {}
    url = f"https://twitter.com/search?q={SEARCH_QUERY}&src=typed_query&f=live"
    driver.get(url)
    time.sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while len(tweet_data) < MAX_TWEETS and scrolls < 9000:
        cards = driver.find_elements(By.XPATH, "//article[@role='article']")
        for card in cards:
            entry = extract_card_data(card)
            print(entry)
            if entry:
                key = hash(entry["tweet"] + entry["date"] + entry["time"])
                tweet_data[key] = entry

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scrolls += 1

    return list(tweet_data.values())


def save_csv(data):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Saved {len(df)} tweets → {OUTPUT_CSV}")


def main():
    driver = init_driver()
    driver.get("https://twitter.com/home")
    time.sleep(3)

    # Check if logged in by inspecting presence of tweet composer or login prompt
    if "login" in driver.current_url.lower():
        print("No active session. Logging into Twitter...")
        login(driver)
    else:
        print(" Active session detected. Skipping login.")

    print("Fetching tweets after login or session restore...")
    tweets = scrape_tweets(driver)
    driver.quit()
    save_csv(tweets)


if __name__ == "__main__":
    main()
