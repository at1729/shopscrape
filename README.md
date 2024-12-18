__ShopScrape__

ShopScrape is a web scraper that retrieves all the product URLs from a specified domain.

This project has been created using [Scrapy](https://scrapy.org/) to leverage parallelism and asynchronous processing of URLs.

__Dependencies__
```
Python 3.8.3
pip install scrapy==2.11.2
pip install scrapyd==1.5.0 ( For local deployment )
```
Usage

Download the project and navigate to the shopscrape folder.
The spider can be run directly from the command line as follows:
```
$ scrapy crawl ShopSpider -a start_url=<domain-name> -a product_pattern=<comma-separated-keywords> -a restricted_pattern=<comma-separated-keywords> -a output_path=<path-to-output-file>
```
Arguments:
* __start_url (str) (mandatory)__: This is the homepage for the website to be scraped ( example : https://books.toscrape.com/ )
* __product_pattern (str) (mandatory)__: Comma seprated strings which will always be part of a product web page URL. ( This can differ for different website. example : catalogue as https://books.toscrape.com/ uses catalogue in all of the product pages )
* __restricted_pattern (str) (optional)__: Comma separated strings which will never be part of a product web page URL. ( This can be used to filter out URLs that contain product_pattern but are not valid matches. example: page,category as https://books.toscrape.com/ uses page and category alongwith catalogue in web page URLs that are not product pages )
* __output_path (str)__: absolute path where the result should be stored.

The following command can be run on Windows OS to generate the results:
```
$ scrapy crawl ShopSpider -a start_url=https://books.toscrape.com/ -a product_pattern=catalogue -a restricted_pattern=page,category -a output_path=D:\
```
The above command generates a jsonlines file with the current timestamp at path D:\books.toscrape.com\ containing all the 1000 product URLs hosted on the website.

Output sample:
```
{"url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"}
{"url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"}
{"url": "https://books.toscrape.com/catalogue/soumission_998/index.html"}
{"url": "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"}
{"url": "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"}
.....
```

The project can also be deployed to a server that accepts REST API requests to schedule scraping jobs and a web interface to monitor the jobs.

__Usage__

Start a [scrapyd](https://scrapyd.readthedocs.io/en/latest/) instance using the following command (this will create a server listening on port 6800):
```
$ scrapyd
```

Navigate to the shopscrape folder and upload the project to the server (scrapy.cfg is configured to deploy to url = http://localhost:6800/):
```
$ scrapyd-deploy
```
Now scraping jobs can be scheduled with HTTP POST request to REST API listening on http://localhost:6800/. curl commands can be used as follows:
```
$ curl http://localhost:6800/schedule.json -d start_url=https://books.toscrape.com/ -d product_pattern=catalogue -d restricted_pattern=page,category -d output_path=D: -d project=shopscrape -d spider=ShopSpider
```
__Note__: __project=shopscrape__ and __spider=ShopSpider__ are fixed parameters for the scraper

Jobs can be monitored by accessing the Web Interface available at http://localhost:6800/
