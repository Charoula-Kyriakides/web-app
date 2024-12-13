import requests
from bs4 import BeautifulSoup


class PrelovedScraper:
    """
    A class to scrape listings from Preloved based on keywords, location, and distance.
    """

    def __init__(self, keywords="", user_location="", distance=""):
        """
        Initialize the PrelovedScraper with search parameters.

        Args:
            keywords (str): The search keywords.
            user_location (str): The location for the search.
            distance (str): The search radius in miles.
        """
        self.keywords = keywords
        self.user_location = user_location
        self.distance = distance
        self.soup = None
        self.page_n = 1

    def parse_page(self):
        """
        Parse the HTML content of a search results page.

        Sets:
            self.soup (BeautifulSoup): Parsed HTML content of the page.
        """
        url = f"https://www.preloved.co.uk/search?keyword={self.keywords}&location={self.user_location}&distance={self.distance}&promotionType=free&page={self.page_n}"
        response = requests.get(url)
      
        self.soup = BeautifulSoup(response.text, 'html.parser')
        

    def find_listings_in_a_page(self):
        """
        Find listings on the current page.

        Returns:
            list: A list of dictionaries containing listing details.
        """
        listing_names = self.soup.find_all("span", itemprop="name")
        locations = self.soup.find_all("span", {'data-test-element': 'advert-location'})
        images = self.soup.find_all("img", {"data-defer": "src"})
        links = self.soup.find_all("a", class_='search-result__title is-title')

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
        """
        Determine the number of pages in the search results.

        Sets:
            self.page_n (int): The number of pages in the search results.
        """
        # Check if there are multiple pages
        has_next = self.soup.find("span", {"data-test-element": "has-next"})

        if has_next:
            page_n = has_next.text.split(' ')[-1]
        else:
            page_n = "1"
            
        self.page_n = page_n

    def find_listings_in_all_pages(self):
        """
        Find listings across all pages of search results.

        Returns:
            list: A list of dictionaries containing all listings.
        """
        self.parse_page()
        self.num_of_pages()
        
        all_listings = []

        for page in range(int(self.page_n) + 1):
            if page != 0:
                all_listings += self.find_listings_in_a_page()
            
        return all_listings