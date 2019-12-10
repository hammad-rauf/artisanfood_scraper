from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
import time

from datetime import date

from ..items import ArtisonfoodItem

class ArtisonfoodSpider(CrawlSpider):

    name = "artisonfood"
    start_urls = [
                "https://theartisanfoodcompany.com/?password-protected=login&redirect_to=https%3A%2F%2Fwww.theartisanfoodcompany.com%2F"
    ]

    category = [ "BAKERY","FRESH","PANTRY","WINE & DRINKS","MIXED WINE BOXES","FOOD GIFTS","COUNTRY"]

    def parse(self,response):
        input ={
            "password_protected_pwd": "7777",
            "wp-submit": "Log In",
            "testcookie": "1",
            "password-protected": "login",
            "redirect_to": "https://www.theartisanfoodcompany.com/"
        }
        yield FormRequest.from_response(response,formdata = input,callback = self.product) 

    def product(self,respose):

        main_category = respose.css(".inner.main_menu_holder.fixed #main_nav > .menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children")

        for cat in main_category:

            cate = cat.css(".menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children  a::text").extract_first()
            
            sub_cat = cat.css(".menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children .sub-menu .menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children")

            for sub in sub_cat:

                #product["category"] = cate
                #product["sub_category"] = sub.css(".menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children > a::text").extract_first() 

                sub_sub_cat = sub.css(".sub-menu .menu-item.menu-item-type-custom.menu-item-object-custom a::text").extract()  
                links = sub.css(".sub-menu .menu-item.menu-item-type-custom.menu-item-object-custom a::attr(href)").extract()    

                for index,link in enumerate(links):
                   # product = ArtisonfoodItem()
                    category = cate
                    sub_category = sub.css(".menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children > a::text").extract_first() 
                    sub_sub_category = sub_sub_cat[index]
                    yield Request(url=link,meta={'category': category,"sub_category":sub_category,"sub_sub_category":sub_sub_category},callback=self.product_page2)
                    time.sleep(6)
                    #print(link)      
                
                
    def product_page2(self,response):         
                 
        main = response.css(".cat_list label::text").extract()

        for index,sub_filteer in enumerate(main):
            main[index] = sub_filteer.split(" (")[0]

        for index,sub_filteer in enumerate(main):
            if sub_filteer == " ":
                main.pop(index)
        #print(main)

        temp = []

        for index,data in enumerate(main):

            if data[0] == " ":
                product = ArtisonfoodItem()

                product["category"] = response.meta["category"] 
                product["sub_category"] =  response.meta["sub_category"]
                product["sub_sub_category"] =  response.meta["sub_sub_category"]
                product["filters"] = data
                temp.clear()             
            else:
                temp.append(data)
            
            if index + 1 == len(main) or main[index + 1][0] == " ":
                product["sub_filters"] = temp
                yield product 




        # sub_filters = response.css(".cat_list > .cat_sub_list2 label::text").extract()

        # for index,sub_filteer in enumerate(sub_filters):
        #     sub_filters[index] = sub_filteer.split(" (")[0]

 
        # filters = response.css(".cat_list > .cat_item label::text").extract()

        # for index,filteer in enumerate(filters):
        #     filteer = filteer.split(" (")[0]
        #     filteer = filteer.strip()

        #     product = ArtisonfoodItem()

        #     product["category"] = response.meta["category"] 
        #     product["sub_category"] =  response.meta["sub_category"]
        #     product["sub_sub_category"] =  response.meta["sub_sub_category"]

        #     product["filters"] = filteer

        #     lists = []  

        #     for data in sub_filters:

        #         if filteer in data:
        #             lists.append(data)
        #             sub_filters.remove(data)
                

        #     product["filters"] = filteer 
        #     product["sub_filters"] = lists       

        #     yield product


#    sub_cat = cat.css(".menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children .sub-menu .menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children > a::text").extract()
#    product["sub_category"] = sub_cat

#    sub_sub_cat = cat.css(".menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children .sub-menu .menu-item.menu-item-type-custom.menu-item-object-custom.menu-item-has-children .sub-menu a::text").extract()
#    product["sub_sub_category"] = sub_sub_cat