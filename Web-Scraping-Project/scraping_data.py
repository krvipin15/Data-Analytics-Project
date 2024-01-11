# Import required libraries
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


# This function will get model number for each phone
def finding_model(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    webpage = requests.get(url, headers=headers)

    if webpage.status_code == 200:
        soup = bs(webpage.content, 'html.parser')
        specifications = soup.find_all('li', {'class':'_21lJbe'})
        if len(specifications) > 1:
            return specifications[1].text.strip()
        else:
            return None
    
    return None


# This function will get phone's data from all the pages specified
def scraping_data(pages=5):
    base_url = "https://www.flipkart.com/search?q=phones&page="
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

    phone_data = []

    for page in range(1, pages+1):
        url = base_url + str(page)
        time.sleep(5)
        webpage = requests.get(url, headers=headers)

        if webpage.status_code != 200:
            print(f"Failed to connect to page {page}. Status Code: {webpage.status_code}. URL: {url}")
            continue

        soup = bs(webpage.content, 'html.parser')

        products = soup.find_all('div', {'class':'_2kHMtA'})

        for product in products:
            name = product.find('div', {'class':'_4rR01T'}).text.strip()
            price = product.find('div', {'class':'_30jeq3 _1_WHN1'}).text.strip()
            url = 'https://www.flipkart.com' + product.find('a', {'class':'_1fQZEK'})['href']
            model_number = finding_model(url)

            phone_data.append({
                'Name':name,
                'Price':price,
                'Model':model_number,
                'URL':url
            })
            
    return phone_data


# This function will save it as csv file
def create_csv(data, filename='flipkart_phones.csv'):
    df = pd.DataFrame(data)
    df['Price'] = df['Price'].str.replace('₹', '')
    df['Price'] = df['Price'].str.replace(',', '')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')


# Main function
if __name__ == "__main__":
    phone_data = scraping_data(pages=7)
    create_csv(phone_data)
