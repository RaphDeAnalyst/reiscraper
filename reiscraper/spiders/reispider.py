import scrapy
import re
from reiscraper.items import AmazonscraperItem

class AmazonspiderSpider(scrapy.Spider):
    name = "reispider"
    allowed_domains = ["www.rei.com"]
    start_urls = ["https://www.rei.com/s/new-arrivals"]

    def parse(self, response):
        # Extract the desired elements using the CSS selector
        target_elements = response.css('ul li.VcGDfKKy_dvNbxUqm29K')
        
        # Define the regular expression pattern for extracting ratings and number of reviews
        pattern1 = r'(\d+) reviews with an average rating of (\d+\.\d+) out of 5 stars'
        pattern2 = r'Rated (\d+\.\d+) out of 5 stars'
        
        # Loop through each target element and extract data
        for target_element in target_elements:
            # Extract the full price
            full_price_text = target_element.css('span[data-ui="full-price"]::text').get()
            full_price = full_price_text.split(" ")[2] if '-' in full_price_text else full_price_text
                        
            # Extract the sale price
            sale_price = target_element.css('span[data-ui="sale-price"]::text').get()

            # If sale price is not directly available, extract from the range
            if not sale_price and '-' in full_price_text:
                sale_price = full_price_text.split(" ")[0]

            # Extract Caption e.g., '155 reviews with an average rating of 4.5 out of 5 stars'
            caption = target_element.css('span.cdr-rating__caption-sr_13-5-2 ::text').get()
            
            # Use regular expressions to extract ratings
            match1 = re.search(pattern1, caption)
            match2 = re.search(pattern2, caption)
            
            if match1:
                number_of_reviews = match1.group(1)
                rating = match1.group(2)
            elif match2:
                number_of_reviews = None  # We don't have number of reviews for this format
                rating = match2.group(1)
            else:
                number_of_reviews = None
                rating = None
            
            # Initialize an empty list to store colors
            colors = []
            
            # Extract colors
            color_elements = target_element.css("div.X6FZOQYGZUa4N9FoRUAn button")
            for color_element in color_elements:
                color = color_element.css('::attr(aria-label)').get()
                if color:
                    colors.append(color)
                
            # Concatenate the colors with commas
            concatenated_colors = ', '.join(colors)
            
            rei_item = AmazonscraperItem(
                name_of_item=target_element.css('h2 ::text').get(),
                description=target_element.css('h2 span.Xpx0MUGhB7jSm5UvK2EY ::text').get(),
                full_price=full_price,
                sale_price=sale_price,
                category=target_element.css('div.UgLX7TmYU6vCz9ovpPnR ::text').get(),
                url=target_element.css('a ::attr(href)').get(),
                number_of_reviews=number_of_reviews,
                rating=rating,
                type_color_available=concatenated_colors
            )
            yield rei_item

        # Extract hrefs for pagination and request next pages
        next_page_link = response.css('a[data-id="pagination-test-link-next"]::attr(href)').get()
        self.logger.info(f"Next page link: {next_page_link}")
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
