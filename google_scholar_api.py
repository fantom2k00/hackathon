import requests
from bs4 import BeautifulSoup

def searchGoogleScholar(topic):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    topic = topic.replace(" ", "+")
    url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=' + topic + '+&btnG=&oq=ob'
    response=requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')
    doc = BeautifulSoup(response.text,'html.parser')
  
    paper_names = []
    paper_tag = doc.select('[data-lid]')
    for tag in paper_tag:
        paper_names.append(tag.select('h3')[0].get_text())
        
    links = []
    link_tag = doc.find_all('h3',{"class" : "gs_rt"})
    for i in range(len(link_tag)) :
        links.append(link_tag[i].a['href']) 

    return paper_names, links