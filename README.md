# REI Items Python Scraper

This Python Scrapy spider extracts new arrival item data from [rei.com](https://www.rei.com). The scraper retrieves information about various items including their name, description, prices, category, URL, reviews, ratings, and available colors.

## Development
This scraper is developed using Python and Scrapy framework.
The spider is designed to extract data from the [New Arrivals](https://www.rei.com/s/new-arrivals) section of rei's website.
The pipeline saves the extracted data into a MySQL database for further analysis or usage.

## Dependencies
To run this project smoothly, ensure you have the following dependencies installed using pip:
```
pip install Python Scrapy mysql-connector-python
```
## Installation
Clone this repository to your local machine:
```
https://github.com/RaphDeAnalyst/reiscraper.git
```
Troubleshooting
If you encounter issues running scrapy crawl, try deactivating and then reactivating your virtual environment:
```
deactivate
```
then activate again:

Mac OS
```
source venv/bin/activate
```
Windows
```
venv\Scripts\activate
```
## Customization
Customize the scraper for your specific use case:

Adjust the spider to scrape additional data fields if needed.
Modify the pipeline to save data into a different database or storage system.
Fine-tune the CSS selectors in the spider to handle changes in the website structure.

## Usage
Configure MySQL database settings in the pipelines.py file:
#### Modify these database settings according to your MySQL configuration
```
self.conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='your_password',
    database='rei_items'
)
```
#### If you are using postgres database go to this [link](https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-7-saving-data/#saving-data-to-a-postgres-database) to read about how to set it up for your use case
### Run the Scrapy spider to start scraping:
```
scrapy crawl reispider
```
Monitor the scraping process and check for any errors or warnings.

Access the MySQL database to view the scraped data.
## Data Storage
The scraped data is saved into a MySQL database named rei_items. The database schema includes the following fields:
```
id: Unique identifier for each item
name_of_item: Name of the item
description: Description of the item
full_price: Full price of the item
sale_price: Sale price of the item
category: Category of the item
url: URL of the item
number_of_reviews: Number of reviews for the item
rating: Rating of the item
type_color_available: Available colors for the item
```

## Folder Structure
```
reiscraper/
reiscraper/
items.py: Defines the Scrapy item class.
pipelines.py: Contains pipeline classes for data processing and storage.
settings.py: Configuration settings for the Scrapy project.
spiders/
reinspider.py: Implements the scraping spider to extract data from the REI website.
README.md: This file providing information about the project.
```
#### To deactivate any specific functionality or middleware, you can comment out the relevant code in the spider or pipeline files.

#### Contributions are welcome! If you have suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.



