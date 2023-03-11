from serpapi import GoogleSearch

def searchGoogleScholar(topic):
    params = {
        "engine": "google_scholar",
        "q": topic,
        "api_key": "f5cdf7322844984e5e32f69e32e7b20c94ca65d6471c8a9390262ee28e22ff44"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    
    titles = []
    links = []
    for result in organic_results:
        titles.append(result["title"])
        links.append(result["link"])
    
    print(titles)
    print(links)
    
    return titles, links