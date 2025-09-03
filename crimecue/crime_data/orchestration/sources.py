SOURCES = {
    "delhi_police": {
        "type": "html",
        "url": "https://delhipolice.gov.in/press-releases",
        "selector": "li"
    },
    "mumbai_police": {
        "type": "html",
        "url": "https://mumbaipolice.gov.in/PressRelease",
        "selector": "li"
    },
    "bengaluru_police": {
        "type": "html",
        "url": "https://bcp.karnataka.gov.in/info-2/Press-Releases/en",
        "selector": "li"
    },
    "chennai_police": {
        "type": "html",
        "url": "https://chennaipolice.gov.in/pressrelease.html",
        "selector": "li"
    },
    "kolkata_police": {
        "type": "html",
        "url": "https://kolkatapolice.gov.in/PressRelease.aspx",
        "selector": "li"
    },
    "hyderabad_police": {
        "type": "html",
        "url": "https://hyderabadpolice.gov.in/PressReleases",
        "selector": "li"
    },
    "toi_crime": {
        "type": "rss",
        "url": "https://timesofindia.indiatimes.com/rssfeeds/784865811.cms"
    },
    "indiatoday_crime": {
        "type": "rss",
        "url": "https://www.indiatoday.in/rss/1206578"
    },
    "ndtv_crime": {
        "type": "rss",
        "url": "https://feeds.feedburner.com/ndtvnews-crime"
    },
    "thehindu_national": {
        "type": "rss",
        "url": "https://www.thehindu.com/news/national/feeder/default.rss"
    },
    "hindustantimes_crime": {
        "type": "rss",
        "url": "https://www.hindustantimes.com/feeds/rss/crime-news/rssfeed.xml"
    },
    "indianexpress_india": {
        "type": "rss",
        "url": "https://indianexpress.com/section/india/feed/"
    },
    "dna_india_crime": {
        "type": "rss",
        "url": "https://www.dnaindia.com/feeds/crime"
    },
    "deccanherald_national": {
        "type": "rss",
        "url": "https://www.deccanherald.com/rss-feed/31"
    },
    "gnews": {
        "type": "api",
        "url": "https://gnews.io/api/v4/search",
        "params": {
            "q": "crime India",
            "lang": "en",
            "country": "in",
            "token": "74d75afff1e1980d43f76c4bad42e5b6"
        }
    },
    "newsdata": {
        "type": "api",
        "url": "https://newsdata.io/api/1/news",
        "params": {
            "q": "crime",
            "country": "in",
            "language": "en",
            "apiKey": "pub_d4460cf8de9a4177b1229cf6cf8c5146"
        }
    },
    "worldnewsapi": {
        "type": "api",
        "url": "https://api.worldnewsapi.com/search-news",
        "params": {
            "source-country": "in",
            "categories": "crime",
            "apiKey": "2d16dfaa405e47618a3c66ae797e54c3"
        }
    },
    "mediastack": {
        "type": "api",
        "url": "http://api.mediastack.com/v1/news",
        "params": {
            "access_key": "184bffd6d48f91c3e7fbc27f5bac7b46",
            "country": "in",
            "categories": "crime"
        }
    }
}