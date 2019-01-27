import scrapy
import sys
import random
import csv
from scrape.items import Item
from var_dump import var_dump


search_item = input("Input The Search Item: ")
location = input("Location:")
second_location = input("Second Location:")
third_location = input("Third Location:")
fourth_location = input("Fourth Location:")
fifth_location = input("Fifth Location:")
sixth_location = input("Sixth Location:")




# city = [
#     "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "Fort Worth", 
#     "San Diego", "Dallas", "San Jose", "Austin", "Columbus", "Indianapolis",  "Seattle", "St. Paul", "Nashville", 
#     "Louisville", "Plano"
# ]

# rancity = random.choice(city)


class YellowSpider(scrapy.Spider):


    name = "yellow"

    # start_urls = [
    #     "https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + location
    #     # "https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + third_location,
    #     # "https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + fourth_location
    # ]

    def start_requests(self):
        yield scrapy.Request("https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + location, self.parse)
        yield scrapy.Request("https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + second_location, self.parse2)
        yield scrapy.Request("https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + third_location, self.parse3)
        yield scrapy.Request("https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + fourth_location, self.parse4)
        yield scrapy.Request("https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + fifth_location, self.parse5)
        yield scrapy.Request("https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + sixth_location, self.parse6)
        # yield scrapy.Request('http://www.example.com/3.html', self.parse)

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

    def parse2(self, response):
        for href in response.css('div.v-card a.business-name::attr(href)'):
            yield response.follow(href, self.businessprofile2)

        for href in response.css('div.pagination a::attr(href)'):
            yield response.follow(href, self.parse2)
    
    def parse3(self, response):
        for href in response.css('div.v-card a.business-name::attr(href)'):
            yield response.follow(href, self.businessprofile3)

        for href in response.css('div.pagination a::attr(href)'):
            yield response.follow(href, self.parse3)

    def parse4(self, response):
        for href in response.css('div.v-card a.business-name::attr(href)'):
            yield response.follow(href, self.businessprofile4)

        for href in response.css('div.pagination a::attr(href)'):
            yield response.follow(href, self.parse4)

    def parse5(self, response):
        for href in response.css('div.v-card a.business-name::attr(href)'):
            yield response.follow(href, self.businessprofile5)

        for href in response.css('div.pagination a::attr(href)'):
            yield response.follow(href, self.parse5)

    def parse6(self, response):
        for href in response.css('div.v-card a.business-name::attr(href)'):
            yield response.follow(href, self.businessprofile6)

        for href in response.css('div.pagination a::attr(href)'):
            yield response.follow(href, self.parse6)           

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
            for x in item['email']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_emails:
                    if item['email']:
                        if item['phonenumber']:
                            if item['website']:
                                self.seen_emails.append(x)
                                yield item

                         
    def businessprofile2(self, response):
        for business in response.css('header#main-header'):
            item = Item()
            item['business_name'] = business.css('div.sales-info h1::text').extract()
            w = business.css('a.secondary-btn.website-link::attr(href)').extract()

            item['website'] = str(w).strip('[]')

            item['location'] = second_location

            s = business.css('a.email-business::attr(href)').extract()
            item['email'] = [item[7:] for item in s]

            item['phonenumber'] = business.css('p.phone::text').extract_first()
            for x in item['email']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_emails:
                    if item['email']:
                        if item['phonenumber']:
                            if item['website']:
                                self.seen_emails.append(x)
                                yield item                                   

    def businessprofile3(self, response):
        for business in response.css('header#main-header'):
            item = Item()
            item['business_name'] = business.css('div.sales-info h1::text').extract()
            w = business.css('a.secondary-btn.website-link::attr(href)').extract()

            item['website'] = str(w).strip('[]')

            item['location'] = third_location

            s = business.css('a.email-business::attr(href)').extract()
            item['email'] = [item[7:] for item in s]

            item['phonenumber'] = business.css('p.phone::text').extract_first()
            for x in item['email']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_emails:
                    if item['email']:
                        if item['phonenumber']:
                            if item['website']:
                                self.seen_emails.append(x)
                                yield item 

    def businessprofile4(self, response):
        for business in response.css('header#main-header'):
            item = Item()
            item['business_name'] = business.css('div.sales-info h1::text').extract()
            w = business.css('a.secondary-btn.website-link::attr(href)').extract()

            item['website'] = str(w).strip('[]')

            item['location'] = fourth_location

            s = business.css('a.email-business::attr(href)').extract()
            item['email'] = [item[7:] for item in s]

            item['phonenumber'] = business.css('p.phone::text').extract_first()
            for x in item['email']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_emails:
                    if item['email']:
                        if item['phonenumber']:
                            if item['website']:
                                self.seen_emails.append(x)
                                yield item 

    def businessprofile5(self, response):
        for business in response.css('header#main-header'):
            item = Item()
            item['business_name'] = business.css('div.sales-info h1::text').extract()
            w = business.css('a.secondary-btn.website-link::attr(href)').extract()

            item['website'] = str(w).strip('[]')

            item['location'] = fifth_location

            s = business.css('a.email-business::attr(href)').extract()
            item['email'] = [item[7:] for item in s]

            item['phonenumber'] = business.css('p.phone::text').extract_first()
            for x in item['email']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_emails:
                    if item['email']:
                        if item['phonenumber']:
                            if item['website']:
                                self.seen_emails.append(x)
                                yield item 


    def businessprofile6(self, response):
        for business in response.css('header#main-header'):
            item = Item()
            item['business_name'] = business.css('div.sales-info h1::text').extract()
            w = business.css('a.secondary-btn.website-link::attr(href)').extract()

            item['website'] = str(w).strip('[]')

            item['location'] = sixth_location

            s = business.css('a.email-business::attr(href)').extract()
            item['email'] = [item[7:] for item in s]

            item['phonenumber'] = business.css('p.phone::text').extract_first()
            for x in item['email']:
                #new code here, call to self.seen_business_names
                if x not in self.seen_emails:
                    if item['email']:
                        if item['phonenumber']:
                            if item['website']:
                                self.seen_emails.append(x)
                                yield item                                 