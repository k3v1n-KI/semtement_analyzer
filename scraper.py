"""

Code Reference

This code was largly gotten from the amazon-reviews-extraction github repository belonging to Md Kawsar (github username: kawsarlog) 
https://github.com/kawsarlog/amazon-reviews-extraction.git

In accordance with the MIT License,

MIT License

Copyright (c) 2023 MD Kawsar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


# Import packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


class AmazonReviewScraper:
    def __init__(self):
        # Header to set the requests as a browser requests
        self.headers = {
            'authority': 'www.amazon.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }


    # Extra Data as Html object from amazon Review page
    def get_reviews_html(self, url, len_page):
        
        # Empty List define to store all pages html data
        soups = []
        
        # Loop for gather all 3000 reviews from 300 pages via range
        for page_no in range(1, len_page + 1):
            
            # parameter set as page no to the requests body
            params = {
                'ie': 'UTF8',
                'reviewerType': 'all_reviews',
                'filterByStar': 'critical',
                'pageNumber': page_no,
            }
            
            # Request make for each page
            response = requests.get(url, headers=self.headers)
            
            # Save Html object by using BeautifulSoup4 and lxml parser
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Add single Html page data in master soups list
            soups.append(soup)
        
        return soups

    # Grab Reviews name, description, date, stars, title from HTML
    def extract_review_from_html(self, html_data):

        # Create Empty list to Hold all data
        data_dicts = []
        
        # Select all Reviews BOX html using css selector
        boxes = html_data.select('div[data-hook="review"]')
        
        # Iterate all Reviews BOX 
        for box in boxes:
            
            # Select Name using css selector and cleaning text using strip()
            # If Value is empty define value with 'N/A' for all.
            try:
                name = box.select_one('[class="a-profile-name"]').text.strip()
            except Exception as e:
                name = 'N/A'

            try:
                stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
            except Exception as e:
                stars = 'N/A'   

            try:
                title = box.select_one('[data-hook="review-title"]').text.strip()
            except Exception as e:
                title = 'N/A'

            try:
                # Convert date str to dd/mm/yyy format
                datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
                date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
            except Exception as e:
                date = 'N/A'

            try:
                description = box.select_one('[data-hook="review-body"]').text.strip()
            except Exception as e:
                description = 'N/A'

            # create Dictionary with al review data 
            data_dict = {
                'Name' : name,
                'Stars' : stars,
                'Title' : title,
                'Date' : date,
                'Description' : description
            }

            # Add Dictionary in master empty List
            data_dicts.append(data_dict)
            
        return data_dicts
    
    
    def get_reviews(self, reviews_url, len_page = 4):
        # Grab all HTML
        html_datas = self.get_reviews_html(reviews_url, len_page)
        
        # Empty List to Hold all reviews data
        reviews = []
        # Iterate all Html page 
        for html_data in html_datas:
            
            # Grab review data
            review = self.extract_review_from_html(html_data)
            
            # add review data in reviews empty list
            reviews += review
        # Create a dataframe with reviews Data
        df_reviews = pd.DataFrame(reviews)
        return df_reviews
        

web_scraper = AmazonReviewScraper()

url = "https://www.amazon.ca/dp/B0CWCWL81G"

df_reviews = web_scraper.get_reviews(url)

print(df_reviews)

