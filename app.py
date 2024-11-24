from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    keyword = request.form['keyword']
    user_location = request.form['location']
    distance = request.form['distance']

    preloved_results = PrelovedScraper(keyword, user_location, distance).find_listings_in_all_pages()
    freecycle_results = get_freecycle_results(keyword, user_location, distance)

    return render_template('results.html', preloved_results=preloved_results, freecycle_results=freecycle_results)


######

class PrelovedScraper:
    def __init__(self, keywords="", user_location="", distance=""):
        self.keywords = keywords
        self.user_location = user_location
        self.distance = distance
        self.soup = None
        self.page_n = 1

    def parse_page(self):
        url = f"https://www.preloved.co.uk/search?keyword={self.keywords}&location={self.user_location}&distance={self.distance}&promotionType=free&page={self.page_n}"
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
   

    def find_listings_in_a_page(self):
        listing_names = self.soup.find_all("span",itemprop = "name")
        locations = self.soup.find_all("span",{'data-test-element': 'advert-location'})
        images = self.soup.find_all("img", {"data-defer":"src"})
        links = self.soup.find_all("a",class_='search-result__title is-title')

        listings_in_a_page = []

        for item in range(len(images)):
            listing_details = dict()
            listing_details['name'] = listing_names[item].text
            listing_details['location'] = locations[item].text
            listing_details['image'] = images[item].get('data-src')
            listing_details['link'] = links[item].get('href')
            listings_in_a_page.append(listing_details)

        return listings_in_a_page

    def num_of_pages(self):
        # Check if there are multiple pages
        has_next = self.soup.find("span", {"data-test-element" :"has-next"})

        if has_next:
            page_n = has_next.text.split(' ')[-1]
        else:
            page_n  = "1"
            
        self.page_n  = page_n 

    def find_listings_in_all_pages(self):
        self.parse_page()
        self.num_of_pages()
        
        all_listings = []

        for page in range(int(self.page_n)+1):
            
            if page !=0:
                all_listings = all_listings + self.find_listings_in_a_page()
            
        return all_listings
    

###

# def get_preloved_results(keyword, location, distance):
#     url = f"https://www.preloved.co.uk/search?keyword={keyword}&location={location}&distance={distance}&promotionType=free&page={page_num}"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     has_next = soup.find("span", {"data-test-element" :"has-next"})
#     if has_next:
#         num_of_pages = int(has_next.text.split(' ')[-1])
#     listings = []
#     for item in soup.find_all('a', class_='search-result__title is-title'):
#         title = item.find('span', itemprop='name').text
#         link = item['href']
#         location = item.find_next('span', {'data-test-element': 'advert-location'}).text
#         listings.append({'title': title, 'link': link, 'location': location})

#     return listings

def get_freecycle_results(keyword, location, distance):
    # Implement similar logic to scrape Freecycle
    return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

