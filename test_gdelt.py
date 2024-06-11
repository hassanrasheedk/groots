import pytest
from gdelt import get_gdelt_news, get_top_article_urls

def test_get_top_article_urls():
    import pandas as pd
    data = {'url': ['http://example.com/1', 'http://example.com/2', 'http://example.com/3', 'http://example.com/4', 'http://example.com/5', 'http://example.com/6']}
    articles_df = pd.DataFrame(data)
    top_urls = get_top_article_urls(articles_df)
    assert len(top_urls) == 5
    assert top_urls == data['url'][:5]

def test_get_gdelt_news(mocker):
    keywords = "AI"
    country = "USA"
    mock_articles_df = mocker.Mock()
    mock_timeline_data = {
        "timeline": [
            {"data": [
                {"Average Tone": -5},
                {"Average Tone": 10}
            ]}
        ]
    }
    mocker.patch("gdelt.GdeltDoc.article_search", return_value=mock_articles_df)
    mocker.patch("gdelt.GdeltDoc.timeline_search", return_value=mock_timeline_data)
    top_articles, negative_score, positive_score = get_gdelt_news(keywords, country)
    assert top_articles is not None
    assert negative_score is not None
    assert positive_score is not None