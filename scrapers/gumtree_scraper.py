from .base_scraper import BaseScraper

class GumtreeScraper(BaseScraper):
    def __init__(self,  keywords="", user_location="", distance=""):
        url_template = "https://www.gumtree.com/search?search_category=freebies&search_location={user_location}&search_distance={distance}&q={keywords}&page={page_n}"
        super().__init__(url_template, keywords, user_location, distance)
        self.format_url()
        print(self.url)
        
    def get_pagination_element(self):
        return self.soup.find_all("a", {"class": "button pagination-link css-1vrkhz0"})
    
    def extract_page_n(self, pagination_element):
        return pagination_element[-1].text
        
    def get_ads_container(self):
        return self.soup.find("div",{"class":"css-zfj6vx"})
    
    def get_listing_name_selector(self):
        return "div", {'class':"css-iqq11e"}
    
    def get_location_selector(self):
        return "div", {"class": "css-30gart"}
    
    def get_image_selector(self):
        return "div", {"class": "css-1r4pvhe e25keea15"}
    
    def get_link_selector(self):
        return "a"
    
    def get_image_src(self, image, item):
        if item < 2:
            return image.find("img").get('src')
        else:
            return image.find("img").get('data-src')
    
    def get_full_link(self, link):
        return "https://www.gumtree.com" + link
