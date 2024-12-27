from .base_scraper import BaseScraper
class PrelovedScraper(BaseScraper):
    def __init__(self, keywords="", user_location="", distance=""):
        url_template = "https://www.preloved.co.uk/search?keyword={keywords}&location={user_location}&distance={distance}&promotionType=free&page={page_n}"
        super().__init__(url_template, keywords, user_location, distance)
        self.format_url()
        print(self.url)
        
    def get_ads_container(self):
        return self.soup
    
    def get_listing_name_selector(self):
        return "span", {"itemprop": "name"}
    
    def get_location_selector(self):
        return "span", {"data-test-element": "advert-location"}
    
    def get_image_selector(self):
        return "img", {"data-defer": "src"}
    
    def get_link_selector(self):
        return "a", {"class": "search-result__title is-title"}
    
    def get_image_src(self, image, item):
        image_scr = image.get('data-src')
        
        if image_scr is None:
            image_scr = "placeholder"
            
        return image_scr
    
    def get_pagination_element(self):
        return self.soup.find("span", {"data-test-element": "has-next"})
    
    def extract_page_n(self, pagination_element):
        return pagination_element.text.split(' ')[-1]
