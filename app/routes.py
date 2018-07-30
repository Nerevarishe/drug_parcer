from app import app
from flask import render_template #, flash, redirect, url_for
from app.forms import SearchForm
import requests
import bs4


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    drug_list = None
    if form.validate_on_submit():
        search_query = form.searchfield.data
        SL_apteka_ru = 'https://apteka.ru/search/?q=' + search_query
        region_link = 'https://apteka.ru/_action/geoip/setBranch/144/'
        session = requests.Session()
        response = session.get(region_link)
        response = session.get(SL_apteka_ru)
        soup = bs4.BeautifulSoup(response.text)
        drug = soup.find_all("span", "h2-style")
        price = soup.find_all("div", "price")
        drug = [ element.get_text() for element in drug ]
        price = [ element.get_text() for element in price ]
        drug_list =[ dict(zip(drug, price)) ]
    return render_template('index.html', form=form, drug_list=drug_list)