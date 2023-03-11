from pytrends.request import TrendReq

def getTrendingTopics(keyword):
    topic_titles = [] 
    pytrend = TrendReq(hl='en-US', tz=360) 
    topics = pytrend.suggestions(keyword=keyword)
    for topic in topics:
        topic_titles.append(topic["title"])
    return topic_titles