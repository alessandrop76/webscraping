import csv
from bs4 import BeautifulSoup
from selenium import webdriver


def get_url(search_term):
    """Gerando a Url de busca por termo"""
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ','+')
    
    #adiciona o termo que queremos na busca
    url = template.format(search_term)

    url += '&page{}'

    return url

def extract_record(item):
    """Extraindo e retornando dados de um unico registro"""
    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://amazon.com' + atag.get('href')

    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:    
    # #ranking and rating
    #     rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        # rating = ''
        review_count = ''

    result = (description, price)

    return result
    
   
def main(search_term):
    """ rotina principal *main* """
    #iniciando o webdriver
    driver = webdriver.Chrome()
    
    records = []
    url = get_url(search_term)

    for page in range(1):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in result:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    with open('results.csv', 'w',  encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price'])
        writer.writerows(records)

main('iphone')



    
