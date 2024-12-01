from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from gumtree_scraper import GumtreeScraper
from preloved_scraper import PrelovedScraper

app = Flask(__name__)

@app.route('/')
def index():
    """ 
    Render the index page with the search form. 
    
    Returns: 
        str: Rendered HTML of the index page. 
    """
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    """ 
    Handle the form submission, perform searches on Preloved and Freecycle, 
    and render the results page with the search results. 
    
    Returns: 
        str: Rendered HTML of tshe results page with search results. 
    """
    keyword = request.form['keyword']
    user_location = request.form['location']
    distance = request.form['distance']

    preloved_results = PrelovedScraper(keyword, user_location, distance).find_listings_in_all_pages()
    gumtree_results = GumtreeScraper(keyword, user_location, distance).find_listings_in_all_pages()

    return render_template('results.html', preloved_results=preloved_results, gumtree_results=gumtree_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

