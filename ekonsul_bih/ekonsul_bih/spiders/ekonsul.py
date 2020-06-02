# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import datetime
import pandas


class EkonsulSpider(scrapy.Spider):
    name = 'ekonsul'
    allowed_domains = ['ekonsultacije.gov.ba']
    start_urls = ['https://ekonsultacije.gov.ba/consultations']

    def parse(self, response):
        self.logger.info(f'parse: {response.url}')

        script = response.xpath('//script[not(@*)][contains(.,".kendoGrid")]/text()').get()
        jsonstring = script.split('"data":{"Data":', maxsplit=1)[1].strip()
        jsonstring = jsonstring.split(',"Total":')[0].strip()
        # self.logger.info(jsonstring)
        # obj = json.loads(jsonstring)
        # self.logger.info(obj)
        df = pandas.read_json(jsonstring)
        print(df.head())
        df.to_csv('consultations.csv')
