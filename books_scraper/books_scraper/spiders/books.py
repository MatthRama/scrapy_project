import re
import scrapy
from books_scraper.items import BookItem

STAR_RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css("article.product_pod"):
            item = {
                "title": book.css("h3 a::attr(title)").get(),
                "price": self.parse_price(book.css(".price_color::text").get("")),
                "star_rating": self.parse_star_rating(book),
                "in_stock": self.parse_stock_status(book),
                "thumbnail_url": response.urljoin(book.css("img::attr(src)").get()),
            }
            detail_relative_url = book.css("h3 a::attr(href)").get()
            yield response.follow(detail_relative_url, callback=self.parse_book, cb_kwargs={"item": item})

            next_page = response.css("li.next a::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    @staticmethod
    def parse_price(raw_price):
        match = re.search(r"(\d+\.?\d*)", raw_price)
        if match:
            return float(match.group())
        else:
            return None

    @staticmethod
    def parse_star_rating(book):
        classes = (book.css(".star-rating::attr(class)").get("") or "").split()
        for cls in classes:
            if cls in STAR_RATINGS:
                return STAR_RATINGS[cls]
        return None

    @staticmethod
    def parse_stock_status(book):
        texts = book.css(".instock.availability::text").getall()
        for t in texts:
            return "In Stock" in " ".join(t.strip())

    def parse_book(self, response, item):
        item["detail_url"] = response.url
        item["upc"] = self.get_table_value(response, "UPC")
        item["description"] = (response.css("#product_description ~ p::text").get("") or "").strip()

        availability = self.get_table_value(response, "Availability") or ""
        item["number_available"] = self.parse_number_available(availability)

        item["category"] = (response.css("ul.breadcrumb li:nth-child(3) a::text").get("") or "").strip()

        image_relative_url = response.css("#product gallery img::attr(src)").get()
        if image_relative_url:
            item["image_url"] = response.urljoin(image_relative_url)
        else:
            item["image_url"] = None
        yield BookItem(**item)

        if item["image_url"]:
            item["image_urls"] = [item["image_url"]]

    @staticmethod
    def parse_number_available(availability_text):
        match = re.search(r"(\d+)", availability_text)
        if match:
            return int(match.group())
        else:
            return None

    @staticmethod
    def get_table_value(response, tabname):
        return response.xpath(f'//table//tr[th[normalize-space(text())="{tabname}"]]/td/text()').get()