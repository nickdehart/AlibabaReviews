## Alibaba Express Review Scraper

#### Installation:
- Requires:
   - Python 3.6
   - Scrapy

- Optional:
   - Pipenv

```
pip install scrapy
- OR -
pip install pipenv
pipenv install
```

#### Usage:
```
scrapy crawl reviews -a start_url="https://www.aliexpress.com/item/ITEM_NUMBER.html"
- OR -
pipenv run scrapy crawl reviews -a start_url="https://www.aliexpress.com/item/ITEM_NUMBER.html"
```
- Scraper runs a regular expression to find an 11-digit number in "start_url" parameter.
- Can just feed an 11-digit item number alone or the url as above.

#### Output:
- Outputs a .json file "reviews-ITEM_NUMBER.json" with the scraped results.
- JSON format is as follows:
```
{
   'count': (Integer) total number of reviews on alibaba express,
   'avg': (Float) average rating of reviews on alibaba express,
   'stars': {
      '5': (String) percentage of 5 star reviews on alibaba express, 
      '4': (String) percentage of 4 star reviews on alibaba express, 
      '3': (String) percentage of 3 star reviews on alibaba express, 
      '2': (String) percentage of 2 star reviews on alibaba express, 
      '1': (String) percentage of 1 star reviews on alibaba express, 
   },
   'reviews': [
      // Array of reviews
      {
         'username': (String) person who left review,
         'country': (String) country of person who left review,
         'rating': (Integer) number of stars person left as review,
         'text': (String) review text,
         'date': (String) date review was left,
         'useful': (Integer) number of other users who found this review useful,
         'useless': (Integer) number of other user who found this review NOT useful,
         'images': [
            // Array of image urls
         ],
      }
      ...
   ]
}
```