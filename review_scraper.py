import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

reviewlist = []

class Scraper:
    def get_reviews(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        reviews = soup.findAll('div', {'data-hook': 'review'})
        try:
            for item in reviews:
                review = {
                    'product_name': soup.title.text.strip(),
                    'rating_title': item.find('a', {'data-hook': 'review-title'}).contents[3].text.strip(),
                    'rating_value':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                }
                reviewlist.append(review)

            # for item in reviewlist:
            #     if item['rating_value'] >= 4.0:
            
        except:
            pass
        return reviewlist

# df = pd.DataFrame(reviewlist)
# df.to_excel('sony-headphones.xlsx', index=False)
# print('Fin.')