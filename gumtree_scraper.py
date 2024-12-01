import requests
from bs4 import BeautifulSoup
import urllib.parse

class GumtreeScraper:
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
        self.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" }

    def parse_page(self):
        """
        Parse the HTML content of a search results page.

        Sets:
            self.soup (BeautifulSoup): Parsed HTML content of the page.
        """
    
        url = f"https://www.gumtree.com/search?search_category=freebies&search_location={self.user_location}&search_distance={self.distance}&q={self.keywords}&page={self.page_n}"
        
        response = requests.get(url, headers=self.headers)
        decoded_text = urllib.parse.unquote(response.text)
        self.soup = BeautifulSoup(decoded_text, 'html.parser')
        print(url)
        
    def find_listings_in_a_page(self):
        """
        Find listings on the current page.

        This method extracts listing details such as name, location, image URL, and link 
        from the parsed HTML content of a search results page using BeautifulSoup.

        Returns:
            list: A list of dictionaries containing listing details, each with keys 
                'name', 'location', 'image', and 'link'.
        """
        
        ads = self.soup.find("div",{"class":"css-zfj6vx"})
        listing_names = ads.find_all("div", {'class':"css-iqq11e"}) 
        locations = ads.find_all("div", {'class': 'css-30gart'}) 
        images = ads.find_all("div", class_="css-1r4pvhe e25keea15")
        
        links = ads.find_all("a")

    
        listings_in_a_page = []
       
        for item in range(len(listing_names)):
            listing_details = dict()
            listing_details['name'] = listing_names[item].text
            listing_details['location'] = locations[item].text
            
            # Check if the image is a placeholder
            test_image = images[item].find("img")
            if test_image:
                if item < 2:
                    listing_details['image'] = test_image.get('src')
                else:
                    listing_details['image'] = test_image.get('data-src')
            else:
                listing_details['image'] = "placeholder"
            listing_details['link'] = "https://www.gumtree.com/" + links[item].get('href')
            listings_in_a_page.append(listing_details)
    
        return listings_in_a_page

    def num_of_pages(self):
        """
        Determine the number of pages in the search results.

        Sets:
            self.page_n (int): The number of pages in the search results.
        """
        # Check if there are multiple pages
        has_next = self.soup.find("h2",{"class":"css-130y58l"})

        if has_next:
            page_n = "1"
        else:
            page_n = "2"
                                                                
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



