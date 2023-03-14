from serpapi import GoogleSearch

def searchGoogleScholar(topic):
    params = {
        "engine": "google_scholar",
        "q": topic,
        "api_key": "scholar_key",
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    print(organic_results)
    
    titles = []
    links = []
    authors = []
    
    for result in organic_results:
        if "title" in result:
            titles.append(result["title"])
        else:
            titles.append("Null")
        
        if "link" in result:
            links.append(result["link"])
        else:
            titles.append("Null")
        
        if "publication_info" in result:
            authors.append(result["publication_info"]["summary"])
        else:
            authors.append("Null")
    
    print(authors)
    print(titles)
    print(links)
    
    return authors, titles, links