import requests
from bs4 import BeautifulSoup


class BaseScraper:
    """
    A class to scrape listings from websites based on keywords, location, and distance.
    """

    def __init__(self, url="", keywords="", user_location="", distance=""):
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
        self.url_template = url
        self.ads = False
        self.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" }

    
    
    def format_url(self):
        self.url = self.url_template.format(
            keywords=self.keywords, 
            user_location=self.user_location, 
            distance=self.distance, 
            page_n=self.page_n)
        
    def parse_page(self):
        """
        Parse the HTML content of a search results page.

        Sets:
            self.soup (BeautifulSoup): Parsed HTML content of the page.
        """      
        response = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')
    
    
    def num_of_pages(self):
        """
        Determine the number of pages in the search results.

        Sets:
            self.page_n (int): The number of pages in the search results.
        """
        has_next = self.get_pagination_element()
        extended = self.extened_search()
        if has_next and not extended:    
            self.page_n = self.extract_page_n(has_next)
        else:
            self.page_n = "1"   
       
    
    def find_listings_in_a_page(self):
        """
        Find listings on the current page.

        Returns:
            list: A list of dictionaries containing listing details.
        """
        
        ads = self.get_ads_container()
        
        if ads is None:
            return []

        listing_names = ads.find_all(*self.get_listing_name_selector())
        locations = ads.find_all(*self.get_location_selector())
        images = ads.find_all(*self.get_image_selector())
        links = ads.find_all(*self.get_link_selector())


        
        listings_in_a_page = []

        for item in range(len(images)):
            listing_details = dict()
            listing_details['name'] = listing_names[item].text
            listing_details['location'] = locations[item].text
            listing_details['image'] = self.get_image_src(images[item], item)
            listing_details['link'] = self.get_full_link(links[item].get('href'))
            listings_in_a_page.append(listing_details)
          
        return listings_in_a_page
    
    
    
    def find_listings_in_all_pages(self):
        """
        Find listings across all pages of search results.

        Returns:
            list: A list of dictionaries containing all listings.
        """

        self.parse_page()
        self.num_of_pages()
        all_listings = []
        
        for page in range(int(self.page_n)  + 1):
            if page != 0 and page < 4:
                all_listings += self.find_listings_in_a_page()
        
        return all_listings
    
    def extened_search(self):
        return False
    
    def get_full_link(self, link):
        return link
    
    def get_ads_container(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_listing_name_selector(self):        
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_location_selector(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_image_selector(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_link_selector(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_image_src(self, image, item):
        raise NotImplementedError("Subclasses should implement this method")

    def get_pagination_element(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def extract_page_n(self, element):
        raise NotImplementedError("Subclasses should implement this method")
