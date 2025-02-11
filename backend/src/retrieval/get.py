#!/usr/bin/env python3
import requests
import datetime
import os
import re

def get_yesterday_date():
    """Return yesterday's date as a date object."""
    today = datetime.date.today()
    return today - datetime.timedelta(days=1)

def get_top_articles(date):
    """
    Fetch the top viewed articles for a given date.
    Uses Wikimedia’s Pageviews API.
    """
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{year}/{month}/{day}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ExampleBot/0.1; +https://example.com/bot)"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching top articles: HTTP {response.status_code}")
        return []
    
    data = response.json()
    # The API returns an object with an "items" list containing one element that holds "articles"
    articles = data.get("items", [{}])[0].get("articles", [])
    return articles[:10000]

def sanitize_filename(name):
    """Sanitize the filename by removing characters not allowed in file names."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_article_content(title):
    """
    Download the article content from Wikipedia.
    Uses the MediaWiki API to fetch a plain text extract.
    """
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": title,
        "format": "json",
        "explaintext": True,
        "redirects": 1,
    }
    url = "https://en.wikipedia.org/w/api.php"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ExampleBot/0.1; +https://example.com/bot)"}
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching article '{title}': HTTP {response.status_code}")
        return ""
    
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return ""
    
    # There should be only one page in the result.
    page = next(iter(pages.values()))
    return page.get("extract", "")

def main():
    output_dir = "wikipedia_top_10000"
    os.makedirs(output_dir, exist_ok=True)

    # Use yesterday's date for the pageviews query.
    date = get_yesterday_date()
    print(f"Fetching top articles for {date}")
    top_articles = get_top_articles(date)
    
    if not top_articles:
        print("No articles found. Exiting.")
        return

    for rank, article in enumerate(top_articles, start=1):
        title = article.get("article")
        views = article.get("views")
        print(f"Downloading {rank:03d}: {title} ({views} views)")
        content = get_article_content(title)
        if not content:
            print(f"Warning: No content retrieved for {title}")
            continue

        # Create a safe filename using rank and sanitized title.
        filename = sanitize_filename(f"{rank:03d}_{title}.txt")
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)
    
    print("Download complete! Articles saved in:", output_dir)

if __name__ == "__main__":
    main()
