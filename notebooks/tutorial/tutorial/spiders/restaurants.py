import scrapy
import urllib
import pandas as pd
import pybase64

#scrapy crawl restaurants -a json=test2.json -o full_test2.json

class RestaurantsSpider(scrapy.Spider):
    name = "restaurants"
    
    def __init__(self, json=None, *args, **kwargs):
        super(RestaurantsSpider, self).__init__(*args, **kwargs)
        self.df = pd.read_json(json)
        self.i = 0
        self.start_urls =  ['https://www.tripadvisor.es/'+self.df.loc[self.i,'url']] 
     
                               
    def parse(self, response):
         
        pageurl = self.df.loc[self.i,'url']
            
        try:
            positionlink = response.css("div.xAOpeG9l * a._2wKz--mA._27M8V6YV::attr(data-encoded-url)").get()
        except: positionlink = None
        
        if positionlink !=None:
            try:
                positionlink = pybase64.b64decode(positionlink).decode('UTF-8')
                coordinates = positionlink.split('@')[1].split('_')[0].split(',')      
                positionlink[positionlink.find('@')+1:positionlink.find('_',-5,-1)].split(',')
                latitude = float(coordinates[0])
                longitude = float(coordinates[1])
            except: 
                coordinates = None
                latitude = None
                longitude = None
        else:
            coordinates = None
            latitude = None
            longitude = None

        try: geolist = [item.extract() for item in response.css('ul.breadcrumbs > li.breadcrumb *::text')]
        except: geolist = [None for i in range(15)]
        province = geolist[6]
        city = geolist[9]
        
        try:
            name = response.css('h1.HjBfq::text').get()
        except:
            pass
        
        locationAll = None    

        try:
            locationAll = response.css('a.YnKZo.Ci.Wc._S.C.FPPgD').attrib['href'] ## toqué aquí
        except:
            pass
        
        cuisines = None
        meals = None
        specialDiets = None
        priceRangeNum = None
        
        try :
            sections= response.css("div.tbUiL.b::text").getall()
            contents = response.css("div.SrqKb::text").getall()
            
            for i, section in enumerate(sections):
                if section.lower() == 'tipos de cocina': 
                    cuisines = contents[i]
                elif section.lower() == 'comidas' : 
                    meals = contents[i]
                elif section.lower() == 'dietas especiales': 
                    specialDiets = contents[i]
                elif section.lower() == 'rango de precios': 
                    priceRangeNum = contents[i]
                
        except: pass

        price = None

        try:
            price = response.css("a.dlMOJ::text").getall()[0] 
        except:
            pass

        try:
            price_all = response.css('span.DsyBj.DxyfE').getall() 
        except:
            pass

        try:
            rating = response.css('svg.UctUV.d.H0::attr(aria-label)').getall()
        except:
            pass

        try:
            direction = response.css('a.AYHFM::text').get()
        except:
            pass
            
        yield {'name':name, 'url' : pageurl, 'province': province, 'city':city, 'price_all': price_all, 'price':price, 'direction': direction, 'latitude': latitude, 'longitude': longitude, 'cuisines':cuisines, 'meals':meals,'specialDiets':specialDiets, 'priceRangeNum':priceRangeNum, 'locationAll': locationAll, 'coordinates':coordinates, 'rating':rating, 'positionlink':positionlink}
                    
        self.i += 1
        try: next_page = 'https://www.tripadvisor.es/'+self.df.loc[self.i,'url']
        except: next_page = None
        if next_page is not None:
            yield response.follow(next_page,callback=self.parse)
           
        