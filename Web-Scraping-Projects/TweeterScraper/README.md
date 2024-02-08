# TwitterScraper

TwitterScraper is a Python script for scraping Twitter data based on specified search terms without using API. 
It utilizes Selenium WebDriver for automating interactions with the Twitter website, collecting tweets, and saving them to CSV files. 
This repository contains the script for scraping data as well as a cleaning process for preprocessing the scraped data.


## Features

- Scrapes Twitter data based on user-defined search terms.
- Automates the login process using Selenium WebDriver.
- Collects tweets from the current view on the Twitter search page.
- Saves unique tweets to CSV files.
- Includes a cleaning process for removing duplicate rows and formatting dates.
- Automatically creates a folder with the current date to store scraped data.


## Requirements

- Pandas
- PyFiglet
- Python 3.x
- Deep Translator
- Selenium WebDriver
- Chrome WebDriver (compatible with Selenium)


## Usage

1. Clone the repository to your local machine.

2. Install the required Python packages using `pip install -r requirements.txt`.

3. Provide your Twitter username and password in the  `scrape(` of `TwitterScraper.py` script.

4. Input the path where you want to save the scraped data in the `scrape()` of`TwitterScraper.py` script.

5. Modify the `keywords` list in `keywords.py` script with the search terms you want to scrape Twitter data for.

6. Run the script in your terminal or in any IDE
	`$ python keywords.py`

7. The script will automatically clean the scraped data by removing duplicate entries and formatting dates.

8. The cleaned CSV files will be saved in a folder named according to the current date in the specified directory.


## Example Output

![Demo](https://github.com/krvipin15/Data-Analytics-Project/assets/75027461/8d6a8371-6ff7-4205-86a9-870e691b98f0)


## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.


## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Acknowledgements

- This project was inspired by the [investment-research-twitter-scraper](https://github.com/Fadeleke57/investment-research-twitter-scraper) repository by Farouk Adeleke (@Fadeleke57).

- Special thanks to [OpenAI](https://openai.com/) for providing the GPT-3 language model used for generating documentation and assistance.
