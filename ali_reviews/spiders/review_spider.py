import scrapy
from scrapy.http import FormRequest
import re
import math
import json

class ReviewsSpider(scrapy.Spider):
   name = "reviews"

   def __init__(self, *args, **kwargs):
      super(ReviewsSpider, self).__init__(*args, **kwargs) 
      try:
         productId = re.search("[0-9]{6,15}", kwargs.get('id'))
         productId = productId.group(0)
         self.productId = productId
      except Exception as e:
         self.log("No Product ID Found!!!")
         self.log(e)
         exit(1)

   def start_requests(self):
      url = "https://feedback.aliexpress.com/display/productEvaluation.htm?v=2&productId=" + self.productId + \
      "&ownerMemberId=233046329&companyId=242229398&memberType=seller&startValidDate=&i18n=true"
      yield scrapy.Request(url, callback=self.get_stats, priority=1)

   def get_stats(self, response):
      info = {
         'stars': {
            '5 Stars': int(response.xpath('/html/body/div/div[2]/ul/li[1]/span[3]/text()').get().replace('%', '')),
            '4 Stars': int(response.xpath('/html/body/div/div[2]/ul/li[2]/span[3]/text()').get().replace('%', '')),
            '3 Stars': int(response.xpath('/html/body/div/div[2]/ul/li[3]/span[3]/text()').get().replace('%', '')),
            '2 Stars': int(response.xpath('/html/body/div/div[2]/ul/li[4]/span[3]/text()').get().replace('%', '')),
            '1 Stars': int(response.xpath('/html/body/div/div[2]/ul/li[5]/span[3]/text()').get().replace('%', '')),
         },
         'total': int(response.xpath('/html/body/div/div[1]/text()').get().replace('Customer Reviews (', '').replace(')', '')),
         'avg': float(response.xpath('/html/body/div/div[2]/div/span/b/text()').get())
      }
      
      ratings = [
         '5 Stars',
         '4 Stars',
         '3 Stars',
         '2 Stars',
         '1 Stars',
      ]

      for rating in ratings:
         end = 11
         if rating != '5 Stars':
            end = math.ceil(info['stars'][rating] / 10) + 1
         for i in range(1, end):
            num = 10
            if i == end - 1 and info['stars'][rating] < 10:
               num = info['stars'][rating]
            frmdata = {
               'ownerMemberId': '222312782',
               'memberType': 'seller',
               'productId': self.productId,
               'companyId': '',
               'evaStarFilterValue': rating,
               'evaSortValue': 'sortlarest@feedback',
               'page': str(i),
               'currentPage': str(i-1),
               'startValidDate': '',
               'i18n': 'true',
               'withPictures': 'false',
               'withPersonalInfo': 'false',
               'withAdditionalFeedback': 'false',
               'onlyFromMyCountry': 'false',
               'version': '',
               'isOpened': 'true',
               'translate':  'Y', 
               'jumpToTop': 'true',
               'v': '2'
            }
            url = "https://feedback.aliexpress.com/display/productEvaluation.htm"
            yield FormRequest(url, callback=self.parse, formdata=frmdata, meta={ 'num': num })

   def parse(self, response):

      for i in range(1, response.meta['num']):
         try:
            starValue = response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[2]/div[1]/span/span').get()
            starValue = re.search("[0-9]{2,3}", starValue)
            starValue = int(starValue.group(0))
            rating = 0
            if starValue == 100:
               rating = 5
            elif starValue == 80:
               rating = 4
            elif starValue == 60:
               rating = 3
            elif starValue == 40:
               rating = 2
            else:
               rating = 1

            images = response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[2]/div[3]/dl/dd/ul')

            yield {
               'id': self.productId,
               'username': response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[1]/span/a/text()').get(),
               'country': response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[1]/div/b/text()').get(),
               'rating': rating,
               'text': response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[2]/div[3]/dl/dt/span[1]/text()').get(),
               'date': response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[2]/div[3]/dl/dt/span[2]/text()').get(),
               'images': images.css('li.pic-view-item img::attr(src)').getall(),
               'useful': int(response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[2]/div[3]/dl/div/span[2]/span[2]/text()').get()),
               'useless': int(response.xpath('/html/body/div/div[5]/div[' + str(i) + ']/div[2]/div[3]/dl/div/span[3]/span[2]/text()').get()),
            }

         except Exception as e:
            self.log(e)
