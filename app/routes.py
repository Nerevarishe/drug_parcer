from app import app
from flask import render_template #, flash, redirect, url_for
from app.forms import SearchForm
import requests
import bs4


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    
    DL_apteka_ru = None
    DL_apteka_sklad_com = None
    DL_glav_apteka_ru = None
    
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
        soup = soup.find("div", class_="list catalog-list")
        drug = soup.find_all("span", class_="h2-style")
        price = soup.find_all("div", class_="price")
        drug = [ element.get_text() for element in drug ]
        price = [ element.get_text() for element in price ]
        DL_apteka_ru =[ dict(zip(drug, price)) ]
        
        
        # apteka-sklad.com
        # Поисковый запрос на сайте apteka-sklad.compile
        SL_apteka_sklad_com = 'https://apteka-sklad.com/search/?q=' + search_query
        
        # Ссылка для выбора региона
        #region_link = ''
        
        response = session.get(SL_apteka_sklad_com)
        
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        soup = soup.find(id="search-results")
        
        # Убрать цены до акции 
        test = soup.find_all("div", class_="products-list__price products-list__price--old")
        for element in test:
            _ = element.extract()
        drug = soup.find_all("a", class_="products-list__link")
        price = soup.find_all("div", class_="products-list__price")
        drug = [ element.get_text() for element in drug ]
        price = [ element.get_text() for element in price ]
        DL_apteka_sklad_com =[ dict(zip(drug, price)) ]
        
        # glav-apteka.ru
        # Поисквая ссылка
        SL_glav_apteka_ru = 'https://glav-apteka.ru/searchSmart/?query=' + search_query
        response = session.get(SL_glav_apteka_ru)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        drug = soup.find_all("h5", class_="s-product-header")
        price = soup.find_all("span", class_="s-price")
        print(drug)
        print(price)
        drug = [ element.get_text() for element in drug ]
        price = [ element.get_text() for element in price ]
        print(drug)
        print(price)
        DL_glav_apteka_ru =[ dict(zip(drug, price)) ]
        print(DL_glav_apteka_ru)
        
    return render_template('index.html', form=form, DL_apteka_ru=DL_apteka_ru, DL_apteka_sklad_com=DL_apteka_sklad_com, DL_glav_apteka_ru=DL_glav_apteka_ru)