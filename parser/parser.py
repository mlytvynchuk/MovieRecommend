from bs4 import BeautifulSoup
import requests
import time
import csv
import sys
base_url = 'https://kinokrad.co/'
headers = {
    'accept': '*/*',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.380'
}


def parse_links(base_url, headers):
    session = requests.Session()
    f = open('links.txt', 'r+')
    for i in range(1,1226):
        url = base_url+"page/" + str(i) + "/"
        request = session.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(request.content, 'html.parser')
        blocks = soup.find_all('div', attrs={'class': 'postertitle'})
        for block in blocks:
            link = block.find('a')['href']
            f.write(link+"\n")
            print(link)
        request.close()
        time.sleep(0.3)
    f.close()
    session.close()


def parse_page(link, headers,session):
    
    session = requests.Session()
    request = session.get(link,headers=headers,verify=False)
    soup = BeautifulSoup(request.content, 'html.parser')
    title = soup.find('h1', attrs={'itemprop': 'name'}).text
    title = title[:title.find(" (")]
    info_block = soup.find('ul', attrs={'class': 'janrfall'})
    info_block_items = info_block.find_all('li')
    en_title = info_block_items[1].find('span', attrs={'class': 'orange'}).next_sibling
    genres_a = info_block_items[2].find_all('a',text=True)
    genres = []
    for a in genres_a:
        genres.append(a.text)
    genres = "|".join(genres)
    keywords_a = info_block_items[3].find_all('a',text=True)
    keywords = []
    for a in keywords_a:
        keywords.append(a.text)
    keywords = "|".join(keywords)
    timestamp = info_block_items[4].find('span').next_sibling
    country = info_block_items[5].find('span').next_sibling.replace('\t','').replace('\n','')
    rating = soup.find('div', attrs={'class': 'rating-more'}).find('b').text
    rating = rating[rating.find(":")+2:]
    director = info_block_items[7].find('span').next_sibling
    director = director[1:]
    img = soup.find('div', attrs={'class': 'bigposter'}).find('img')['src']
    cast_blocks = soup.find_all('div', attrs={'class': 'acttitle'})
    cast = []
    for actor in cast_blocks:
        cast.append(actor.text)
    cast = "|".join(cast)
    description = soup.find('div', attrs={'id': 'fulltext'}).text.replace('\n','').replace('\t', '')

    return title,en_title,genres,keywords, timestamp,country, rating,director,img, cast, description
def parse_all_pages(base_url, headers):
    session = requests.Session()
    links = open('links.txt')
    f = open('movies.csv', 'r+')
    not_parsed = open('not_parsed.txt', 'w')
    writer = csv.writer(f)
    counter = 1
    for link in links:
        sys.stdout.write(str(counter))
        sys.stdout.flush()
        counter+=1
        try:
            page = parse_page(
                link[:-1],
                headers, session)
    
            if page:
                writer.writerow(page)
        except:
            not_parsed.write(link)

        time.sleep(0.5)
    not_parsed.close()
    f.close()
    links.close()
parse_all_pages(base_url, headers)
    
