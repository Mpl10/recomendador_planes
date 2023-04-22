import scrapy
import re 

class tripadvisor(scrapy.Spider):

   #the name of the spider
   name = 'tripadvisor'

   #these are the urls that we will start scraping
   allowed_domains = ['tripadvisor.es']
   start_urls = ['https://www.tripadvisor.es/Restaurants-g187514-Madrid.html#EATERY_LIST_CONTENTS']

   def parse(self, response):
        prod_class = 'roxNU.Vt.o'
        prod_name = 'Lwqic.Cj.b'
        products = response.css(f'div.{prod_class}')
        url_list = []
        for product in products:
            #here we put the data returned into the format we want to output for our csv or json file
            if product.css(f'a.{prod_name}').attrib['href'] in url_list:
                break
            else:
                print(product, url_list)
                yield {
                    'name_raw': product.css(f'a.{prod_name}').get(),
                    'price_raw' : product.css('span.SUszq').getall(),
                    'reviews' : product.css('span.IiChw').get(),
                    'url' : product.css(f'a.{prod_name}').attrib['href'],
                }
                url_list.append(product.css(f'a.{prod_name}').attrib['href'])

        next_page = response.css('a.nav.next.rndBtn.ui_button.primary.taLnk').attrib['href']
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)