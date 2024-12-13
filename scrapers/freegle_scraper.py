import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from lxml_html_clean import Cleaner

url = "https://www.ilovefreegle.org/"


session = HTMLSession()
response = session.get(url)

response.html.find('div[class="autocomplete-wrapper"]', first=True).attrs['modelvalue'] = 'E14 6DN'

response = requests.post(url, data={
    'autocomplete-wrapper': 'E14 6DN'
})


print(response.url)

soup = BeautifulSoup(response.text, 'html.parser')
items = soup.find_all("a", {"class":"nodecor text-wrap item"})
print(len(items))
for item in items:
    print(item.text)