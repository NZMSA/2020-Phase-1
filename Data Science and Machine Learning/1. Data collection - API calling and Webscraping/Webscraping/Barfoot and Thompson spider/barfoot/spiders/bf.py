# -*- coding: utf-8 -*-
import scrapy
import regex as re


class BfSpider(scrapy.Spider):
    name = 'bf'
    allowed_domains = ['barfoot.co.nz']
    start_urls = ['https://www.barfoot.co.nz/properties/residential/region=auckland-city/property-type=house']

    def parse(self, response):
        # Getting each property card on the webpage into a "list" that we can iterate through
        cards = response.xpath('//div[@class="property-details "]')

        #Iterate through each card to get the address, bedrooms, bathrooms
        for card in cards:
            address = card.xpath('./a/div[@class="address"]/text()').get()
            bed = card.xpath('./a/div/span[@class="bed"]/text()').get()
            bath = card.xpath('./a/div/span[@class="bath"]').get()

            #Regex expression here - we are extracting the numerical values only
            bed = re.findall('\d+', bed)[0]
            bath = re.findall('\d+', bath)[0]
            
            yield { "Address" : address,
                    "Bed" : bed,
                    "Bath" : bath}
        
        #There is a next button on the page - and the next page url is within the attribute "onclick" within this button
        url = response.xpath('//div[@class="button secondary-button next"]')
        url = url.xpath('./@onclick').get()
        url = re.match("window.location = '(.*)'$", url).group(1)
        #Here we are simply concatenating python strings together to get a functional url
        url = 'https://www.' + self.allowed_domains[0] + url
        
        yield scrapy.Request(url=url, callback=self.parse)