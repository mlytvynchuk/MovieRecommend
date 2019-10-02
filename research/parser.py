from bs4 import BeautifulSoup
import requests
import time
import csv

headers = {
    'accept': '*/*',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.380'
}
base_url = 'https://rezka.ag/series/best/'
def parse_page_links(base_url, headers):
    links = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')
    main_content = soup.find('div', attrs={'class': 'b-content__inline_items'})
    movie_blocks = main_content.find_all('div', attrs={'class': 'b-content__inline_item'})
    for block in movie_blocks:
        link = block['data-url']
        links.append(link)
        print(link)

    return links

def parse_pages(base_url, headers):
    links = []
    f = open('movie_links.txt', 'r+')
    
    for i in range(1,148):
        page_links = parse_page_links(base_url+"/page/"+str(i)+"/", headers)
        for line in page_links:
            f.write(line+"\n")

        time.sleep(0.3)
    f.close()
    return links

def parse_movie_page(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    soup = BeautifulSoup(request.content, 'html.parser')

    title = soup.find('h1', attrs={'itemprop': 'name'}).text

    rating_span = soup.find('span', attrs={'class': 'b-post__info_rates imdb'})
    rating = rating_span.find('span', attrs={'class': 'bold'}).text
    info_block = soup.find('table',attrs={'class':'b-post__info'})
    
    info_block_data=info_block.find_all('tr')
    info_date_block = info_block_data[2]
    date = info_date_block.find('a').text.split(' ')[0]

    info_director_block =info_block_data[4]
    director = info_director_block.find('span',attrs ={'itemprop': 'name'}).text

    info_category_block =info_block_data[5]
    info_category_block = info_category_block.find_all('td')[1]
   
    genres_block=info_category_block.find_all('span',attrs ={'itemprop':'genre'})
    genres = []
    for genre in genres_block:
        genres.append(genre.text)

    info_actors_block=info_block_data[10]
    info_actors_block=info_actors_block.find('div',attrs={'class':'persons-list-holder'})  
    actor_block=info_actors_block.find_all('span',attrs={'class':'item'})[:-1]  
    actors=[]
    for actor in actor_block:
        actors.append(actor.text.replace(',',''))

    dede=soup.find('div',attrs={'class':'b-post__description_text'}).text

    image='https://rezka.ag'+soup.find('img',attrs={'itemprop':'image'})['src']

    return [title, rating, date,director,"|".join(genres),"||".join(actors),dede,image]
    
# parse_movie_page('http://rezka.ag/series/drama/13729-podvodnaya-lodka.html', headers)
# parse_pages(base_url, headers)

def parse_movie_page_and_write_to_file():
    f = open('movie_links.txt', 'r')
    movies = open('page_movies.csv','r+', encoding='utf-8')
    writer = csv.writer(movies)
    counter = 1
    for link in f:
        print(counter)
        counter+=1
        try:
            movie_data = parse_movie_page(link.replace('\n', ''),headers)
            writer.writerow(movie_data)
        except:
            continue
        
    f.close()
    movies.close()
parse_movie_page_and_write_to_file()
# parse_movie_page('https://rezka.ag/series/drama/16722-v-ozhidanii-solnca.html', headers)
