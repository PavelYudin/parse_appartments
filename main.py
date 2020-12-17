import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
def input_sum():
    pmax=input('Введите максимальную стоимость: ')
    return pmax
def get_html(url):
    r=requests.get(url)
    return r.text
def get_total_pages(soup):
    pages_count=soup.find(text='Объявления по вашему запросу в других городах')
    if pages_count:
    	return 1
    pages=soup.find('div',class_='pagination-pages clearfix')
    if pages is None:
        return 1
    link=list(pages.children)[len(pages)-1].get('href')
    pages_count=urlparse(link).query.split('&')[0].split('=')[-1]
    return pages_count
def search_ads_on_the_page(html,soup):
    page_arr=[]
    
    def get_title(obj_soup):
        tag_span=obj_soup.select('.iva-item-titleStep-2bjuh span')
        return tag_span[len(tag_span)-1].get_text()
    
    def get_url(obj_soup):
        tag_a=obj_soup.select('.iva-item-titleStep-2bjuh a')
        return 'https://www.avito.ru'+tag_a[len(tag_a)-1].attrs['href']
    
    def get_price(obj_soup):
        tag_span=obj_soup.select('.price-text-1HrJ_.text-text-1PdBw.text-size-s-1PUdo')
        return tag_span[len(tag_span)-1].get_text()
    
    def get_street(obj_soup):
        tag_span=obj_soup.select('.geo-address-9QndR.text-text-1PdBw.text-size-s-1PUdo span')
        return tag_span[len(tag_span)-1].get_text()
    
    main_div=soup.find('div',attrs={'data-marker':'catalog-serp'})
    ads=main_div.find_all('div',attrs={'class':'iva-item-body-NPl6W'})
    
    for ad in ads:
        res_dict={}
        res_dict['title']=get_title(ad)
        res_dict['price']=get_price(ad)
        res_dict['street']=get_street(ad)
        res_dict['url']=get_url(ad)
        page_arr.append(res_dict)
    return page_arr
    
def main():
    result=[]
    pmax=input_sum()
    base_url='https://www.avito.ru/moskovskaya_oblast_chehov/kvartiry/prodam/vtorichka-ASgBAQICAUSSA8YQAUDmBxSMUg?'
    page_part='p='
    url=base_url+'&pmax='+pmax
    print(url)
    html=get_html(url)
    soup=BeautifulSoup(html,'html.parser')
    pages_count=int(get_total_pages(soup))
    print('всего страниц ',pages_count,' type ',type(pages_count))
    for page in range(1,pages_count+1):
    	url=base_url+'&pmax='+pmax+'&p='+str(page)
    	html=get_html(url)
    	result.append(search_ads_on_the_page(html,soup))

    columns=['title','price','street','url']
    with open("apartments.csv", mode="w", encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=columns,delimiter = "|", lineterminator="\r")
        writer.writeheader()
        for page in result:
            writer.writerows(page)

if __name__=='__main__':
    main()
    
