# scrapyNetEaseNewsComments 
This is a scrapy project to crawl the comments as well as contents of news from NetEase. The scraped data is stored into MongoDB.

## Requirement(on Ubuntu Linux):
1. mongo: sudo apt-get install mongodb-server
2. scrapy: pip install Scrapy==1.0.3
3. pymongo: pip install pymongo
4. apt-get install libxml2-dev libxslt-dev  
5. apt-get install python-lxml
6. apt-get install python-twisted

## Run: 
scrapy crawl stack_crawler

## Reference
1. https://realpython.com/blog/python/web-scraping-with-scrapy-and-mongodb/
2. https://realpython.com/blog/python/web-scraping-and-crawling-with-scrapy-and-mongodb/
