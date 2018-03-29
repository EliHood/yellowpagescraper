import scrapy
import sys
import random
import csv


search_item = input("Input The Search Item: ")
location = input("Location:")


# city = [
#     "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "Fort Worth", 
#     "San Diego", "Dallas", "San Jose", "Austin", "Columbus", "Indianapolis",  "Seattle", "St. Paul", "Nashville", 
#     "Louisville", "Plano"
# ]

# rancity = random.choice(city)



class Item(scrapy.Item):
    business_name = scrapy.Field()
    website = scrapy.Field()
    phonenumber = scrapy.Field()
    email = scrapy.Field()
    location = scrapy.Field()


class YellowSpider(scrapy.Spider):


    name = "yellow"

    start_urls = [
        "https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + location
    ]
    def __init__(self):
        self.seen_business_names = []
        self.seen_phonenumbers = []
        self.seen_websites = []
        self.seen_emails = []


    def parse(self, response):
        for href in response.css('div.v-card a.business-name::attr(href)'):
            yield response.follow(href, self.businessprofile)

        for href in response.css('div.pagination a::attr(href)'):
            yield response.follow(href, self.parse)

    def businessprofile(self, response):
        for business in response.css('header#main-header'):
            item = Item()
            item['business_name'] = business.css('div.sales-info h1::text').extract()
            w = business.css('a.secondary-btn.website-link::attr(href)').extract()

            item['website'] = str(w).strip('[]')
            item['location'] = location
       
            s = business.css('a.email-business::attr(href)').extract()
            item['email'] = [item[7:] for item in s]

            item['phonenumber'] = business.css('p.phone::text').extract_first()
            for x in item['business_name']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_business_names:
                    if item['business_name']:
                        if item['phonenumber']:
                            if item['email']:
                                if item['website']:
                                    yield item
                                    self.seen_business_names.append(x)
                                    
                
                                

   