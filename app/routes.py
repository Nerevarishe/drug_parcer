from app import app
from flask import render_template #, flash, redirect, url_for
from app.forms import SearchForm
import requests
import bs4


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    drug_list1 = None
    drug_list2 = None
    if form.validate_on_submit():
        search_query = form.searchfield.data
        # apteka.ru
        # Поисковый запрос на сайте apteka.ru
        SL_apteka_ru = 'https://apteka.ru/search/?q=' + search_query
        
        # Ссылка для выбра региона
        region_link = 'https://apteka.ru/_action/geoip/setBranch/144/'
        
        # Объект в котором хранится активная сессия
        session = requests.Session()
        
        # Выбрать регион на сайте
        response = session.get(region_link)
        
        # Загрузить страницу для парсинга
        response = session.get(SL_apteka_ru)
        
        # Парсинг... TODO Дописать комментарии
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        soup = soup.find("div", "list catalog-list")
        drug = soup.find_all("span", "h2-style")
        price = soup.find_all("div", "price")
        drug = [ element.get_text() for element in drug ]
        price = [ element.get_text() for element in price ]
        drug_list1 =[ dict(zip(drug, price)) ]
        
        
        # apteka-sklad.com
        # Поисковый запрос на сайте apteka-sklad.compile
        SL_apteka_sklad_com = 'https://apteka-sklad.com/search/?q=' + search_query
        
        # Ссылка для выбора региона
        #region_link = ''
        
        response = session.get(SL_apteka_sklad_com)
        
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        soup = soup.find(id="search-results")
        drug = soup.find_all("a", "products-list__link")
        price = soup.find_all("div", "products-list__price")
        drug = [ element.get_text() for element in drug ]
        price = [ element.get_text() for element in price ]
        drug_list2 =[ dict(zip(drug, price)) ]
        
    return render_template('index.html', form=form, drug_list1=drug_list1, drug_list2=drug_list2)