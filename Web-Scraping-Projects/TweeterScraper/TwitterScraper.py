import os
import csv
import pyfiglet
from time import sleep
from selenium import webdriver
from selenium.common import exceptions
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add a global variable to store the WebDriver instance
global_driver = None

def login_x(username: str, password: str):
    """
    Log in to Twitter using the provided username and password.

    This function automates the login process on Twitter using Selenium WebDriver.
    It opens the Twitter login page, enters the provided username and password, and submits the form.
    It will store webdriver instance in global variable so it can be used in all program.

    Parameters:
    username (str): The Twitter username to log in with.
    password (str): The Twitter password for the specified username.

    Returns:
    WebDriver
    """
    global global_driver

    if global_driver is None:
        options = ChromeOptions()
        # Sets the Chrome window to start in maximized mode 
        options.add_argument("--start-maximized")
        # Excludes the automation flag to reduce the chance of detection by websites
        options.add_experimental_option("excludeSwitches", ["enable-automation"])   
        driver = webdriver.Chrome(options=options)

        # Open the Twitter login page
        url = "https://twitter.com/i/flow/login"
        driver.get(url)

        # Find and input the username
        username_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
        username_input.send_keys(username)
        username_input.send_keys(Keys.ENTER)

        # Find and input the password
        password_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        
        print("Stay on the driver instance until the scraper logs in as user")
        print("Login successfull... Initiating Twitter Scraper \n")

        # Assign diver to global variable
        global_driver = driver

        sleep(45)

    return global_driver


def change_page_sort(tab_name: str, driver):
    """
    Sorts the tweets on the search page between "Latest" and "Top."

    This function is designed to work with the Twitter search page 
    where you can switch between "Latest" and "Top" tweets, and
    returns the XPath expression for checking the state of the tab.

    Parameters:
    tab_name (str): Enter the tab name (e.g., "Latest" or "Top")
    driver (Any): Initializes a Chrome webdriver with the specified options.

    Returns:
    str
    """
    tab = driver.find_element(by=By.LINK_TEXT, value=tab_name)
    tab.click()
    sleep(3)


def twitter_search(driver, search_term: str):
    """
    Performs a Twitter search using the provided search term.

    This function automates the search process on Twitter using Selenium WebDriver.
    It opens the Twitter search page, enters the provided keyword, you want to search 
    and returns True if found the post related to specified keyword.

    Parameters:
    driver (Any): Initializes a Chrome webdriver with the specified options.
    search_term (str): The specified keyword.

    Returns:
    bool
    """
    try:
        driver.get('https://twitter.com/search')
        print(f"Searching for tweets with the term {search_term}.")
        sleep(5)

        # Insert keyword into search box and start searching
        search_input = driver.find_element(by=By.XPATH, value='//input[@data-testid="SearchBox_Search_Input"]')
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)
        sleep(2)

        # Change page to "Latest" instead of "Top"
        change_page_sort("Latest", driver)

        try:
            # If no result for a keyword, move to next keyword 
            error_message = driver.find_element(by=By.XPATH, value='//div[@data-testid="empty_state_header_text"]')
            if error_message.text.startswith("No results"):
                print(f"No results found for {search_term}. \n")
                return False
        except exceptions.NoSuchElementException:
            pass

        return True
    except:
        driver.refresh()
        scrape(search_term)


def generate_tweet_id(tweet):
    """
    Join tweets together
    
    Parameter:
    tweet (Any): Takes all the tweets scraped from Tweeter 
    
    Return:
    str
    """
    return ''.join(tweet)


def scroll_down_page(driver, last_position, num_seconds_to_load: float =1.5, scroll_attempt: int =0, max_attempts: int =5):
    """
    Scrolls down a webpage using selenium

    This function is designed to be used iteratively to continuously scroll down a page 
    until a certain condition is met (e.g., reaching the end of the scrollable content).
    
    Parameters:
    driver (Any): Initializes a Chrome webdriver with the specified options.
    last_position (Any): Specify the last position of webpage.
    num_seconds_to_load (float): Pauses the execution for specified duration e.g., 0.5.
    scroll_attempt (int): Shows the number of times webpage is scrolled e.g., 0.
    max_attempts (int): Specify the number of times a script should run e.g., 5.

    Returns:
    tuple[Any, Any | bool]
    """
    end_of_scroll_region = False
    
    # Execute JavaScript to scroll to the bottom of the page.
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    sleep(num_seconds_to_load)

    # Retrieves the current vertical scroll position of the page.
    curr_position = driver.execute_script("return window.pageYOffset;")

    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            last_position, end_of_scroll_region = scroll_down_page(driver, curr_position, num_seconds_to_load, scroll_attempt + 1, max_attempts)
        else:
            end_of_scroll_region = True

    last_position = curr_position

    return last_position, end_of_scroll_region


def save_tweet_data_to_csv(records, filepath: str, mode: str ='a+'):
    """
    Saves collected data into a CSV file using CSV Library.

    This function takes the data and the filepath, 
    and saves it as a CSV file.

    Parameters:
    records (Any): Takes data collected by scrping twitter.
    filepath (str): Specify the filename to save as a CSV file
    mode (str): Specify the mode

    Returns:
    None
    """
    header = ['name', 'handle', 'imgurl', 'retweets', 'likes', 'url', 'post', 'date']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerow(records)


def collect_all_tweets_from_current_view(driver, lookback_limit: int =25):
    """
    Collect tweets from the current view on a Twitter page.

    This function is designed to limit the number of collected tweets
    to the specified lookback limit.

    Parameters:
    data (Any): Takes data collected by scrping twitter.
    lookback_limit (int): Limits number of tweets to be collected e.g., 25.

    Returns:
    Any
    """
    # Locates tweet elements on the page using an XPath expression.
    page_cards = driver.find_elements(by=By.XPATH, value='//article[@data-testid="tweet"]')
    # If tweets on a page are less then specified limit, return tweets 
    if len(page_cards) <= lookback_limit:
        return page_cards
    # Return all the tweets present
    else:
        return page_cards[-lookback_limit:]


def translate_text(text):
    """
    Translates tweets from the current view on a Twitter page.

    This function is designed to translate collected tweets from hindi to english
    using Google Translator.

    Parameters:
    text (str): Provide the tweet text 

    Returns:
    str
    """
    try:
        translated = GoogleTranslator(source="auto", target="en").translate(text)
        return translated
    except Exception:
        pass


def extract_data_from_current_tweet_card(card):
    """
    Extracts specific data from the tweets

    This function is designed to extract various data points 
    from a given tweet card on Twitter, and returns data list 
    which contains a dictionary for each tweet, and
    the list will be populated with these dictionaries.

    Parameters:
    card (Any): Provide latest tweet card from Tweeter.

    Returns:
    tuple
    """
    # Extract name of the Twitter user
    try:
        name = card.find_element(by=By.XPATH, value='.//span').text
        name = translate_text(name)
    except exceptions.NoSuchElementException:
        name = ""
    except exceptions.StaleElementReferenceException:
        name = ""
    
    # Extract Twitter handle (username) of the Tweeter user
    try:
        handle = card.find_element(by=By.XPATH, value='.//span[contains(text(), "@")]').text
    except exceptions.NoSuchElementException:
        handle = ""
    
    # Extract the date when the tweet was posted and formates the data e.g., yyyy-mm-dd
    try:
        date = card.find_element(by=By.XPATH, value='.//time').get_attribute('datetime')[:10]
    except exceptions.NoSuchElementException:
        date = ""
    
    # Extract text content of the tweet posted
    try:
        post = card.find_element(by=By.CSS_SELECTOR, value="div[data-testid='tweetText']").text
        post = translate_text(post)
    except exceptions.NoSuchElementException:
        post = ""

    # Extract the number of retweets on the tweet posted
    try:
        retweets = card.find_element(by=By.XPATH, value='.//div[@data-testid="retweet"]').text
    except exceptions.NoSuchElementException:
        retweets = ""
    
    # Extract the number of likes on the tweet posted
    try:
        likes = card.find_element(by=By.XPATH, value='.//div[@data-testid="like"]').text
    except exceptions.NoSuchElementException:
        likes = ""
    
    # Extract the URL of the tweet
    try:
        urls = card.find_elements(By.CSS_SELECTOR, "a")
        url = urls[3].get_attribute("href")
    except exceptions.NoSuchElementException:
        url = ""
    
    # Extract the URL of an image or video associated with the tweet
    try:
        image_element = card.find_element(by=By.CSS_SELECTOR, value='div[data-testid="tweetPhoto"] img')
        imgurl = image_element.get_attribute("src")
    except exceptions.NoSuchElementException:
        try:
            video_element = card.find_element(by=By.CSS_SELECTOR, value='div[data-testid="videoPlayer"] video')
            imgurl = video_element.get_attribute("src")
        except exceptions.NoSuchElementException:
            try:
                video_element = card.find_element(by=By.CSS_SELECTOR, value='video[aria-label="Embedded video"]')
                imgurl = video_element.get_attribute("poster")
            except exceptions.NoSuchElementException:
                imgurl = ""

    tweet = (name, handle, imgurl, retweets, likes, url, post, date)
    return tweet


def scrape(search_terms: list):
    """
    Scrapes Twitter data based on the provided search term and saves unique tweets to a CSV file.

    Parameters:
        search_terms (list): The search term to query Twitter.

    Returns:
        str: The filepath where the CSV file is saved.

    Example:
        scrape("#Python")

    Notes:
        - Requires a valid Twitter login using Selenium.
        - Collects tweets from the current view, avoiding duplicates.
    """
    
    # Generate ASCII art for "TwitterScraper"
    ascii_art = pyfiglet.figlet_format("TwitterScraper", font="standard")
    print(ascii_art)

    # Information about the developer
    print("""
            [-] TwitterScraper [-]
             [ By: Vipin Kumar ]

    ===============================================
    [+] Github    : www.github.com/krvipin15
    [+] Twitter   : www.twitter.com/krvipin15
    [+] Instagram : www.instagram.com/krvipin15
    [+] Linkedin  : www.linkedin.com/in/krvipin15
    ===============================================
    """)

    print("Initializing WebDriver for the Chrome browser...")

    global global_driver
    # Getting current date time
    curr_date = datetime.now()
    # Getting date and month
    ddmm = curr_date.strftime('%d%m')
    
    try:
        directory = f"tweet_{ddmm}"
        parent_dir = "C:/Users/vipin/Downloads/" # Enter the desired location to create a new folder
        path = os.path.join(parent_dir, directory)
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as e:
        pass

    for search_term in search_terms:
        # Use login_x() to get or create a WebDriver instance
        username, password = "knght2024", "aceknght"
        driver = login_x(username=username, password=password)

        # Create filepath for every search_term
        filepath = f"{path}/{search_term.lower()}_tt{ddmm}.csv"

        until = curr_date.strftime('%Y-%m-%d')
        since = (curr_date - timedelta(days=1)).strftime('%Y-%m-%d')
        search_term = f'"#{search_term}" until:{until} since:{since}'

        result = twitter_search(driver, search_term)
        sleep(30)
        if not result:
            continue

        save_tweet_data_to_csv(None, filepath, 'w')      
        last_position = None
        end_of_scroll_region = False
        unique_tweets = set()

        while not end_of_scroll_region:
            cards = collect_all_tweets_from_current_view(driver)
            for card in cards:
                try:
                    tweet = extract_data_from_current_tweet_card(card)
                except exceptions.StaleElementReferenceException:
                    continue
                if not tweet:
                    continue
                tweet_id = generate_tweet_id(tweet)
                if tweet_id not in unique_tweets:
                    unique_tweets.add(tweet_id)
                    save_tweet_data_to_csv(tweet, filepath)
            last_position, end_of_scroll_region = scroll_down_page(driver, last_position)
            if end_of_scroll_region:
                break
        print(f"Successfully scraped data saved at {filepath}. \n")

    driver.quit()
    print("Scraping completed successfully. \n")

    return filepath
    

if __name__ == "__main__":
    keywords = ['Vhopal','budaun']
    scrape(search_terms=keywords)
