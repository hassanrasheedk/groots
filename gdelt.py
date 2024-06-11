import requests
from requests.exceptions import SSLError
from datetime import datetime, timedelta
from gdeltdoc import GdeltDoc, Filters

def get_top_article_urls(articles_df):
    """
    Retrieves the top article URLs from a DataFrame of articles.

    Args:
        articles_df (DataFrame): DataFrame containing article data.

    Returns:
        List[str]: A list of the top 5 article URLs, or None if the DataFrame is empty.
    """
    if articles_df is None or articles_df.empty:
        return None
    return articles_df['url'].head(5).tolist()

def get_gdelt_news(keywords: str, country: str):
    """
    Fetches news articles and sentiment scores from GDELT based on keywords and country.

    Args:
        keywords (str): Keywords to search for in articles.
        country (str): Country to filter the articles by.

    Returns:
        Tuple: A tuple containing a list of top article URLs, negative sentiment score, and positive sentiment score.
    """
    print(keywords)

    # Dates for the past three months
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    filters = Filters(
        keyword=keywords,
        start_date=start_date_str,
        end_date=end_date_str,
        country=country
    )

    gd = GdeltDoc()

    def safe_article_search(filters):
        try:
            return gd.article_search(filters)
        except SSLError as ssl_error:
            print(f"An SSL error occurred: {ssl_error}")
            return None

    def safe_timeline_search(filters):
        try:
            return gd.timeline_search("timelinetone", filters)
        except SSLError as ssl_error:
            print(f"An SSL error occurred: {ssl_error}")
            return None

    articles = safe_article_search(filters)
    top_articles = get_top_article_urls(articles)
    
    try:
        timelinetone = safe_timeline_search(filters)
        if timelinetone is not None and "timeline" in timelinetone and len(timelinetone["timeline"]) > 0 and "data" in timelinetone["timeline"][0]:
            sum_negative = timelinetone[timelinetone['Average Tone'] < 0]['Average Tone'].sum()
            sum_positive = timelinetone[timelinetone['Average Tone'] > 0]['Average Tone'].sum()

            normalized_negative = ((sum_negative - (-100 * len(timelinetone))) / (100 * len(timelinetone))) * 10
            normalized_positive = (sum_positive / (100 * len(timelinetone))) * 10

            print("Normalized Negative Score (0-10 scale):", normalized_negative)
            print("Normalized Positive Score (0-10 scale):", normalized_positive)

            return top_articles, normalized_negative, normalized_positive
        else:
            print("Timeline data is not in the expected format")
            return None, None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None
