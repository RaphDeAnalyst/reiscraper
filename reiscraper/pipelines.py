import logging
from itemadapter import ItemAdapter
from urllib.parse import urljoin  # Importing urljoin from urllib.parse

class ReiscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Lowercasing certain fields
        change_cases = ["category", "description", "name_of_item", "type_color_available"]
        for change_case in change_cases:
            value = adapter.get(change_case)
            if value:
                adapter[change_case] = value.lower()
        
        # Converting price fields to float
        prices = ["full_price", "sale_price"]
        for price in prices:
            value = adapter.get(price)
            if value:
                try:
                    adapter[price] = float(value.replace("$", "").replace(",", ""))
                except ValueError:
                    logging.error(f"Failed to convert {price} to float: {value}")
        
        # Converting certain fields to integers
        to_ints = ["number_of_reviews", "rating"]
        for to_int in to_ints:
            value = adapter.get(to_int)
            if value:
                try:
                    adapter[to_int] = int(value)
                except ValueError:
                    logging.error(f"Failed to convert {to_int} to integer: {value}")
        
                # Fixing partial URLs
        url = adapter.get("url")
        if url and url.startswith("/"):
            adapter["url"] = urljoin("https://www.rei.com", url)
            
        return item


import mysql.connector
# import psycopg2

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '0814',
            database = 'rei_items'
        )
        
        # ## Create/Connect to database
        # self.connection = psycopg2.connect(host='localhost', user=mysql, password='0814', dbname='books')

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS new_arrivals(
            id int NOT NULL auto_increment, 
            name_of_item text,
            description text,
            full_price float,
            sale_price float,
            category VARCHAR(255),
            url VARCHAR(255),
            number_of_reviews INTEGER,
            rating INTEGER,
            type_color_available text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute("""insert into new_arrivals (
            name_of_item, 
            description,
            full_price,
            sale_price, 
            category, 
            url, 
            number_of_reviews,
            rating,
            type_color_available
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["name_of_item"],
            str(item["description"]), # changes made here (str())
            item["full_price"],
            item["sale_price"],
            item["category"],
            item["url"],
            item["number_of_reviews"],
            item["rating"],
            item["type_color_available"]
        ))


        ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()