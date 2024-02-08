import os
import pandas as pd
from datetime import datetime
from TwitterScraper import scrape

# Scrap data on these Keywords
keywords1 = [
    "saharanpur","kairana","muzaffarnagar","bijnor","nagina","moradabad","rampur","sambhal","amroha","meerut","baghpat","ghaziabad",
    "gautam buddh nagar","bulandshahr","aligarh","hathras","mathura","agra","fatehpur sikri","firozabad","mainpuri","etah","budaun",
    "aonla","bareilly","pilibhit","shahjahanpur","kheri","dhaurahra","sitapur","hardoi","misrikh","unnao","mohanlalganj","lucknow",
    "rae bareli","amethi","sultanpur","pratapgarh","farrukhabad","etawah","kannauj","kanpur","akbarpur","jalaun","jhansi","hamirpur",
    "banda UP","fatehpur","kaushambi","phulpur","allahabad","barabanki","faizabad","ambedkar nagar","bahraich","kaiserganj","shrawasti",
    "gonda","domariyaganj","basti","sant kabir nagar","maharajganj","gorakhpur","kushi nagar","deoria","bansgaon","lalganj","azamgarh",
    "ghosi","salempur","ballia","jaunpur","machhlishahr","ghazipur","chandauli","varanasi","bhadohi","mirzapur","robertsganj",
    "thiruvallur","chennai north","chennai south","chennai central","sriperumbudur","kancheepuram","arakkonam","vellore","krishnagiri",
    "dharmapuri","tiruvannamalai","arani","viluppuram","kallakurichi","salem","namakkal","erode","tiruppur","nilgiris","coimbatore",
    "pollachi","dindigul","karur","tiruchirappalli","perambalur","cuddalore","chidambaram","mayiladuthurai","nagapattinam","thanjavur",
    "sivaganga","madurai","theni","virudhunagar","ramanathapuram","thoothukkudi","tenkasi","tirunelveli","kanyakumari","morena MP","bhind",
    "gwalior","guna","sagar","tikamgarh","damoh","khajuraho","satna","rewa","sidhi","shahdol","jabalpur","mandla","balaghat","chhindwara",
    "hoshangabad","vidisha","bhopal","rajgarh","dewas","ujjain","mandsour","ratlam","dhar","indore","khargone","khandwa","betul","chikkodi",
    "belgaum","bagalkot","bijapur","gulbarga","raichur","bidar","koppal","bellary"
]

keywords2 = [
    "haveri", "dharwad", "uttara kannada", "davanagere", "shimoga", "udupi chikmagalur", "hassan", "dakshina kannada", 
    "chitradurga", "tumkur", "mandya", "mysore", "chamarajanagar", "bangalore rural", "bangalore north", "bangalore central", 
    "bangalore south", "chikballapur", "kolar", "kachchh", "banaskantha", "patan", "mahesana", "sabarkantha", "gandhinagar", 
    "ahmedabad east", "ahmedabad west", "surendranagar", "rajkot", "porbandar", "jamnagar", "junagadh", "amreli", "bhavnagar", 
    "anand", "kheda", "panchmahal", "dahod", "vadodara", "chhota udaipur", "bharuch", "bardoli", "surat", "navsari", "valsad", 
    "chandni chowk", "north east delhi", "east delhi", "new delhi", "north west delhi", "west delhi", "south delhi", 
    "valmikinagar", "paschim champaran", "purvi champaran", "sheohar", "sitamarhi", "madhubani", "jhanjharpur", "supaul", 
    "araria", "kishanganj", "katihar", "purnia", "madhepura", "darbhanga", "muzaffarpur", "vaishali", "gopalganj", "siwan", 
    "saran", "hajipur", "ujiarpur", "samastipur", "begusarai", "khagaria", "bhagalpur", "banka", "munger", "nalanda", 
    "patna sahib", "pataliputra", "arrah", "buxar", "sasaram", "karakat", "jahanabad", "aurangabad", "gaya", "nawada", 
    "jamui", "cooch behar", "alipurduars", "jalpaiguri", "darjeeling", "raiganj", "balurghat", "maldaha uttar", 
    "maldaha dakshin", "jangipur", "berhampore", "murshidabad", "krishnanagar", "ranaghat", "bangaon", "barrackpore", 
    "dum dum", "barasat", "basirhat", "jaynagar", "mathurapur", "diamond harbour", "jadavpur", "kolkata dakshin", 
    "kolkata uttar", "howrah", "uluberia", "srerampur", "hooghly", "arambagh", "tamluk", "kanthi", "ghatal", "jhargram", 
    "medinipur", "purulia", "bankura", "bishnupur", "bardhaman purba", "bardhaman durgapur", "asansol", "bolpur", "birbhum", 
    "araku", "srikakulam", "vizianagaram", "visakhapatnam", "anakapalli", "kakinada", "amalapuram", "rajahmundry", 
    "narasapuram", "eluru", "machilipatnam", "vijayawada", "guntur", "narasaraopet", "bapatla", "ongole", "nandyal", 
    "kurnool", "anantapur", "hindupur", "kadapa", "nellore", "tirupati", "rajampet", "chittoor"
]

# Scrape Twitter data using provided keywords
scrape(keywords1)

print("Initiating cleaning process on the scraped data...\n")

def formatting_date(_date: str):
    """
    Function to convert date string to datetime object.

    Parameter:
    date_str (str): Date string in format '%Y-%m-%d'.

    Returns:
    datetime: Datetime object.
    """
    return datetime.strptime(_date, '%Y-%m-%d')

try:
    # Get current date
    curr_date = datetime.now()
    # Get day and month part of the date
    ddmm = curr_date.strftime('%d%m')
    # Construct folder path where CSV files are stored
    folder_path = f"C:/Users/vipin/Downloads/tweet_{ddmm}"

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            print(f"{filename} is in process...")

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Remove duplicate rows from the DataFrame
            df.drop_duplicates(inplace=True)

            # Apply formatting_date function to 'date' column
            df['date'] = df['date'].apply(formatting_date)

            # Save the cleaned DataFrame back to the CSV file
            df.to_csv(file_path, index=False, encoding="utf-8")

            print("File successfully processed and saved in the directory.\n")

except FileNotFoundError:
    print("File not found. Please check the file path and try again.\n")

except Exception as e:
    print(f"An error occurred: {e}.\n")
