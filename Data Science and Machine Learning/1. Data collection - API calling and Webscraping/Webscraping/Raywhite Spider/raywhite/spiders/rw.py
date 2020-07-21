# -*- coding: utf-8 -*-
import scrapy
import regex as re


class RwSpider(scrapy.Spider):
    name = 'rw'
    allowed_domains = ['raywhite.co.nz']
    start_urls = ['https://raywhite.co.nz/search/?sort=&type_code=RES&res_type_code=SAL&categoryCode=NHS&regionSelect=6&districtSelect=all&priceMin=&priceMax=&bedroomsMin=&bedroomsMax=&bathroomsMin=&bathroomsMax=&keywordSearch=&filterResults=&carSpacesMin=&carSpacesMax=&buildingSizeMin=&buildingSizeMax=&landSizeMin=&landSizeMax=']

    def parse(self, response):

        cards = response.xpath('//div[@class="card-body"]')

        for card in cards:
            address = card.xpath('./a/h5/text()').getall()
            address = [x.strip() for x in address]
            address = [x.replace('\xa0',' ') for x in address]
            address = ", ".join(address)

            bed_bath = card.xpath('./div[@class="card-details"]/div[@class="card-tags font-regular text-grey"]/text()').get()
            if bed_bath is None:
                bed_bath = ''
            bed_bath = bed_bath.strip()
            bed_bath = bed_bath.replace('\xa0', ' ')

            if re.match('([0-9]+) Bed', bed_bath):
                bedrooms = re.match('([0-9]+) Bed', bed_bath).group(1)
            else:
                bedrooms = ''
            
            if re.match('.* ([0-9]+) Bath', bed_bath):
                bathrooms = re.match('.* ([0-9]+) Bath', bed_bath).group(1)
            else:
                bathrooms = ''

            yield { "Address" : address,
                    "bedrooms" : bedrooms,
                    "bathrooms" : bathrooms}

        yield scrapy.Request(response.xpath('//li[@class="page-item  active"]/following-sibling::li[1]/a/@href').get(), callback = self.parse)
