import requests
from requests.exceptions import SSLError
from datetime import datetime, timedelta
from gdeltdoc import GdeltDoc, Filters

def get_top_article_urls(articles_df):
    # Check if the DataFrame is empty
    if articles_df is None or articles_df.empty:
        return None
    
    # Extract the 'url' column and get the top 5 URLs
    top_urls = articles_df['url'].head(5).tolist()

    return top_urls

# Function to get news from the past three months based on a keyword
def get_gdelt_news(keywords, country):

    print(keywords)

    # Dates for the past three months
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Parameters for the API request
    filters = Filters(
        keyword = keywords,
        start_date = start_date_str,
        end_date = end_date_str,
        country = country
        )

    gd = GdeltDoc()

    def safe_article_search(filters):
        try:
            return gd.article_search(filters)
        except SSLError as ssl_error:
            print(f"An SSL error occurred: {ssl_error}")
            # Handle the SSL error as needed, e.g., retry, log, or return a default value
            return None

    def safe_timeline_search(filters):
        try:
            return gd.timeline_search("timelinetone", filters)
        except SSLError as ssl_error:
            print(f"An SSL error occurred: {ssl_error}")
            # Handle the SSL error as needed, e.g., retry, log, or return a default value
            return None

    #Search for articles matching the filters
    articles = safe_article_search(filters)
    top_articles = get_top_article_urls(articles)
    
    #Get a timeline of the number of articles matching the filters
    try:
        timelinetone = safe_timeline_search(filters)
        print(timelinetone)
        # Check if the timeline data is in the expected format
        if timelinetone is not None and "timeline" in timelinetone and len(timelinetone["timeline"]) > 0 and "data" in timelinetone["timeline"][0]:
            # Separate and sum negative and positive values
            sum_negative = timelinetone[timelinetone['Average Tone'] < 0]['Average Tone'].sum()
            sum_positive = timelinetone[timelinetone['Average Tone'] > 0]['Average Tone'].sum()

            # Normalize the sums to a 0-10 scale
            # For negative values, we use -100 as the min range, for positive values, we use +100
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