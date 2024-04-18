import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

def get_news(search_phrase, news_category):
    # Constructing the search URL
    search_url = f"https://www.aljazeera.com/search/{search_phrase}"
    
    # Sending a request to the search page
    response = requests.get(search_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {search_url}. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Finding the latest news link
    latest_news_link = soup.find('a', class_='search-card')
    if not latest_news_link:
        print("Latest news link not found.")
        return None
    
    # Constructing the URL for the latest news
    news_url = latest_news_link['href']
    
    # Sending a request to the latest news page
    response = requests.get(news_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {news_url}. Status code: {response.status_code}")
        return None
    
    # Parseing the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting title, date, description, and image URL
    title = soup.find('h1', class_='post-title').text.strip()
    date = soup.find('time')['datetime']
    description = soup.find('meta', attrs={'name': 'description'})['content']
    image_url = soup.find('meta', property='og:image')['content']
    
    # Downloading the image
    image_filename = download_image(image_url)
    
    # Determining if the title or description contains any amount of money
    contains_money = any(re.search(r'\$\d+\.?\d*', text) for text in [title, description])
    
    return {'title': title, 'date': date, 'description': description, 'image_filename': image_filename, 'contains_money': contains_money}

def download_image(image_url):
    # Geting the filename from the URL
    filename = os.path.basename(image_url)
    
    # Sending a request to download the image
    response = requests.get(image_url)
    
    if response.status_code != 200:
        print(f"Failed to download image from {image_url}. Status code: {response.status_code}")
        return None
    
    # Saving the image to a file
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    return filename

def save_to_excel(news_data, excel_filename):
    df = pd.DataFrame(news_data)
    df.to_excel(excel_filename, index=False)

if __name__ == "__main__":
    # Using inputs
    search_phrase = input("Enter search phrase: ")
    news_category = input("Enter news category/section/topic: ")
    num_articles = int(input("Enter number of articles to fetch: "))
    
    # Geting news data
    news_data = []
    for i in range(num_articles):
        article_data = get_news(search_phrase, news_category)
        if article_data:
            news_data.append(article_data)
    
    # Saving to Excel
    save_to_excel(news_data, 'news_data.xlsx')



