# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime


EARLIEST_DATE = datetime(2016, 10, 14)
# EARLIEST_DATE = datetime(2020, 5, 1)


class EsavjeSpider(scrapy.Spider):
    name = 'esavje'
    allowed_domains = ['esavjetovanja.gov.hr']
    start_urls = ['https://esavjetovanja.gov.hr/ECon/Dashboard/']

    def parse(self, response):
        self.logger.info(f'parse: {response.url}')

        for row in response.css('#EConSummaries tbody tr'):
            row_id = next(iter(row.css('td:nth-child(3) a::attr(href)').re('entityId=(\d+)')), 'None')
            start = re.sub(r'\.$', '', str(row.css('td:nth-child(5) ::text').get()).strip())
            end = re.sub(r'\.$', '', str(row.css('td:nth-child(6) ::text').get()).strip())
            expected_publication = re.sub(r'\.$', '', str(row.css('td:nth-child(7) ::text').get()).strip())

            start_date = datetime.strptime(start, '%d.%m.%Y')
            if start_date < EARLIEST_DATE:
                return

            yield {
                'id': row_id,
                'institution': str(row.css('td:nth-child(2) ::text').get()).strip(),
                'title': str(row.css('td:nth-child(3) ::text').get()).strip(),
                'start': start,
                'end': end,
                'expected_publication': expected_publication,
                'status': str(row.css('td:nth-child(8) ::text').get()).strip(),
            }

            reports = row.css('td:nth-child(4) .reports-inline a::attr(href)').get()
            if reports:
                yield response.follow(reports, callback=self.parse_reports)

        next_page = response.css('.red-pagination .btnp-right')[0].xpath('../@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_reports(self, response):
        self.logger.info(f'parse_reports: {response.url}')

        parent_id = response.url.split('entityId=')[-1]
        for row in response.css('#EConReport tbody tr'):
            yield {
                'parent_id': parent_id,
                'id': str(row.css('td:nth-child(1) ::text').get()).strip(),
                'user': str(row.css('td:nth-child(2) ::text').get()).strip(),
                'area': str(row.css('td:nth-child(3) ::text').get()).strip(),
                'comment': str(row.css('td:nth-child(4) ::text').get()).strip(),
                'status': str(row.css('td:nth-child(5) ::text').get()).strip(),
                'response': str(row.css('td:nth-child(6) ::text').get()).strip(),
            }
