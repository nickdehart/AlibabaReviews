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
scrapy crawl reviews -a id="ITEM_NUMBER" -o OUTFILE.json
- OR -
pipenv run scrapy crawl reviews -a id="ITEM_NUMBER" -o OUTFILE.json
```
- Scraper runs a regular expression to find an 6-15 digit number in "id" parameter.
- Can just feed an 11-digit item number alone or the url as above.

#### Output:
- Outputs a .json file "OUTFILE.json" with the scraped results.
- Crawls one page of aliexpress to get stats of reviews.
   - Number of 5, 4, 3, 2, 1 star reviews
- Uses that info to determine how many pages of reviews will be scraped.
   - 10 pages of 5 star reviews
   - Ceiling( percentage of reviews / 10 ) for other reviews
   - Minimum is 10 reviews on 1 page.
- JSON format is as follows:
```
[
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
```