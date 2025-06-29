# Twitter Web Scrapping and Analysis

### Workflow Summary
Step	Description
1. Scraping	Collected ~2100 recent tweets using Selenium from Twitter’s live feed, capturing tweet text, metadata, and engagement metrics.
2. Cleaning	Filtered non-English tweets and removed noise (links, hashtags, stop-words, etc.). Retained all core metadata.
3. Analysis	Applied sentiment scoring (VADER), topic modeling (LDA), and visualized the data for trends and patterns.

##### Steps to run the Project:
###### 1. Install dependencies in the project root:
pip install --upgrade pip
pip install -r requirements.txt

###### 2. Set up your Twitter credentials: Create a file named .env in the project root
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password

###### 3. Scrape Tweets
python scripts/scrape_tweets.py
– This will spin up Chrome, log into Twitter, scroll until tweets are collected, and save them to data/tweets_scrape_raw.csv.

###### 4. Clean & Filter Tweets:
python scripts/clean_tweets.py
– Reads data/tweets_scrape_raw.csv, drops non-English tweets, cleans text, and writes data/tweets_cleaned.csv.

###### 5. Analyze & visualize
python analysis/analysis.py
– Loads data/tweets_cleaned.csv, runs sentiment analysis, LDA topic modeling, and outputs:
 - reports/sentiment_dist.png 
 - reports/topic_dist.png 
 - reports/timeline.png 
 - reports/top_hashtags.png
<br>– Also writes the augmented table to data/tweets_final.csv.

#### Analysis & Findings
###### A. Sentiment Distribution (VADER) <br>
![sentiment_dist](https://github.com/user-attachments/assets/54d5868c-427f-44d7-9f1e-36c7b27cd8b6)

Insights:
- Positive tweets dominate: Over 50% of the tweets express optimism or encouragement—e.g., people sharing job openings or celebrating offers.
- Neutral sentiment trails slightly behind: Likely includes straightforward job postings or factual announcements.
- Negative sentiment is scarce: Indicates fewer complaints, frustrations, or job-hunting struggles in this snapshot.

Takeaway: The job conversation on Twitter—at least in this segment—is hopeful and opportunity-driven.



B. Tweet Topic Distribution <br>
![topic_dist](https://github.com/user-attachments/assets/0193e626-5d8d-45e0-b551-fe1556883ac7)

What the chart shows: An LDA-based analysis grouped tweets into five topics (0–4). The bar chart below displays how many tweets fall into each:
•	Topic 2 (apply, job, click) – ~500 tweets (highest)
•	Topic 4 (engineer, hiring, united) – ~250 tweets
•	Topic 0 (apply, manager, developer) – ~200 tweets
•	Topic 3 (utm, jobs, source) – ~150 tweets
•	Topic 1 (thread, topic, could) – ~100 tweets (lowest)
Each topic’s top three keywords appear in the legend, giving a peek at the theme behind the numbers.
Why this matters:
•	Dominant theme (Topic 2): Keywords “apply,” “job,” “click” indicate direct call-to-action posts—likely job postings or recruitment links.
•	Technical roles (Topic 4): “engineer,” “hiring,” “united” suggests a strong substream of engineering openings.
•	Managerial & dev roles (Topic 0): “manager,” “developer,” plus “apply” indicates mid-to-senior tech and management positions.
•	Marketing/meta tags (Topic 3): “utm,” “source,” “jobs” hint at auto-generated RSS/link-sharing feeds.
•	Conversational chatter (Topic 1): “thread,” “topic,” “could” suggests general discussions or comment threads about job trends.
Actionable takeaways
1.	Elevate CTAs: Since CTA-style tweets dominate, ensure your listings have clear “apply now” links and strong calls to action.
2.	Highlight engineering roles: Carve out dedicated campaigns for engineering and if that’s a core audience.
3.	Filter auto-feeds: If you want genuine engagement, consider filtering or labeling “utm/source” posts as auto-shares versus human-generated.
4.	Foster dialogue: The small but present conversational segment (Topic 1) is an opportunity for Q&A sessions, Twitter Chats, or Ask-Me-Anythings to boost community engagement.


C. Tweets Over Time <br>
![timeline](https://github.com/user-attachments/assets/a1873b34-000c-480a-a8f9-2c4358710ab6)

What the chart shows
•	Aggregated daily counts of our cleaned, English-only tweets with #naukri, #jobs, #jobseeker, #vacancy.
•	Over three days (June 27–29, 2025), volume fell steadily: • June 27: ~520 tweets • June 28: ~400 tweets • June 29: ~190 tweets
Why this matters
•	Peak engagement window: Twitter job chatter was highest on June 27, suggesting your best posting days or times might fall earlier in the week or right after a weekend.
•	Diminishing returns: By June 29, volume had dropped by ~60%. If you launch new campaigns later in this cycle, you risk lower visibility.
Actionable takeaways
1.	Front-load your announcements. Roll out new job posts or promotional content when daily tweet volume is highest.
2.	Monitor hourly patterns. Drill down beyond daily counts—if most tweets on June 27 occurred between 8 AM–12 PM, tailor your publishing schedule to that window.
3.	Re-run weekly. Compare weekly or monthly cycles to understand if this mid-week dip is consistent or driven by external events.


D. Top 10 Hashtags <br>
![top_hashtags](https://github.com/user-attachments/assets/8cafda2f-ef11-440f-8eb4-55204a611044)

What the chart shows A horizontal bar chart listing the ten most-used hashtags in our scraped tweets, with their raw counts:

Why this matters
•	“jobs” dominates: Both lowercase and capitalized variants combine for over 750 mentions—your core term.
•	Action keywords: “hiring,” “jobsearch,” “hiringnow” suggest active-seeking and recruitment messaging works.
•	Emerging signals: “layoffs” appears in the top 10, hinting at concern around job cuts.
Actionable takeaways
1.	Optimize your hashtag strategy: Include “#jobs,” “#hiring,” and “#jobsearch” to maximize reach.
2.	Experiment with uppercase: Tweets with “#Jobs” and “#Hiring” also perform strongly
3.	Address layoff concerns: Content around “#layoffs” might find engagement from users worried about job security—this could be an opportunity for supportive messaging or resources.


