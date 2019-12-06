import scrapy
from scrapy.http import FormRequest
import re
import json

class ReviewsSpider(scrapy.Spider):
   name = "reviews"

   def __init__(self, *args, **kwargs):
      super(ReviewsSpider, self).__init__(*args, **kwargs) 
      try:
         productId = re.search("[0-9]{11}", kwargs.get('start_url'))
         productId = productId.group(0)
         self.productId = productId
         self.info = {}
      except Exception as e:
         self.log("No Product ID Found!!!")
         self.log(e)
         exit(1)

   def start_requests(self):

      ratings = [
         '5 Stars',
         '4 Stars',
         '3 Stars',
         '2 Stars',
         '1 Stars',
      ]
      
      for rating in ratings:
         for i in range(1, 11):
            frmdata = {
               'ownerMemberId': '222312782',
               'memberType': 'seller',
               'productId': self.productId,
               'companyId': '',
               'evaStarFilterValue': rating,
               'evaSortValue': 'sortdefault@feedback',
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
            yield FormRequest(url, callback=self.parse, formdata=frmdata)

   def parse(self, response):

      stars = response.css('body div.feedback-container div.rate-detail ul.rate-list li')
      self.info['count'] = int(response.css('body div.feedback-container div.customer-reviews::text').get().replace('Customer Reviews (', '').replace(')', ''))
      if 'stars' not in self.info:
         self.info['stars'] = {}
      self.info['stars']['5'] = stars[0].css('span.r-num::text').get()
      self.info['stars']['4'] = stars[1].css('span.r-num::text').get()
      self.info['stars']['3'] = stars[2].css('span.r-num::text').get()
      self.info['stars']['2'] = stars[3].css('span.r-num::text').get()
      self.info['stars']['1'] = stars[4].css('span.r-num::text').get()
      self.info['avg'] = float(response.css('body div.feedback-container div.rate-detail div.rate-score span.rate-score-number b::text').get())
      if 'reviews' not in self.info:
         self.info['reviews'] = []

      for review in response.css('body div.feedback-container div.feedback-list-wrap div.feedback-item'):
         starValue = review.css('div.fb-main div.f-rate-info span.star-view span').get()
         starValue = re.search("[0-9]{2,3}", starValue)
         starValue = int(starValue.group(0))
         rating = 2 if starValue > 20 else 1
         rating = 3 if starValue > 40 else 1
         rating = 4 if starValue > 60 else 1
         rating = 5 if starValue > 80 else 1

         images = []
         for image in review.css('div.fb-main div.f-content dl.buyer-review dd.r-photo-list ul.util-clearfix'):
            images.append(image.css('li.pic-view-item img::attr(src)').get())

         obj = {
            'username': review.css('div.fb-user-info span.user-name a::text').get(),
            'country': review.css('div.fb-user-info div.user-country b::text').get(),
            'rating': rating,
            'text': review.css('div.fb-main div.f-content dl.buyer-review dt.buyer-feedback span::text').get(),
            'date': review.css('div.fb-main div.f-content dl.buyer-review dt.buyer-feedback span.r-time-new::text').get(),
            'images': images,
            'useful': int(review.css('div.fb-main div.f-content dl.buyer-review div.j-digg-info-new span.thf-digg-useful span.thf-digg-num::text').get()),
            'useless': int(review.css('div.fb-main div.f-content dl.buyer-review div.j-digg-info-new span.thf-digg-useless span.thf-digg-num::text').get())
         }
         self.info['reviews'].append(obj)

      filename = 'reviews-%s.json' % self.productId
      with open(filename, 'w') as f:
         # this file gets rewritten up to 50 times.
         # should look for a better way.
         json.dump(self.info, f)
