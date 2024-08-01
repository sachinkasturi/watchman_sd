from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta
import pytz
import requests

# Define functions to send messages via Telegram
def telegram_bot_sendques(bot_message):
    bot_token = '7434696374:AAEZohkjyvSYqviFQ7RMcIVVY7gwlpr5iQc'
    bot_chatID = '1155462778'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=MarkdownV2&text=' + str(bot_message).replace('.', '\\.')  # Escape the dot character
    response = requests.get(send_text)
    return response.json()

def telegram_bot_sendtext(bot_message):
    bot_token = '7244741562:AAFMffEdd8Cnigb7j9StokLppAaPw3K-ahM'
    bot_chatID = '1121025878'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=MarkdownV2&text=' + str(bot_message).replace('.', '\\.')  # Escape the dot character
    response = requests.get(send_text)
    return response.json()

#variables
sub = "CSd"
username = "tiwarikasturi@gmail.com"
password = "Expert@751"
login_text= f" Logged {sub}"
limit_texts = f"Limit hit {sub}"

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Open the Chegg website and log in
driver.get("https://expert.chegg.com/auth")
time.sleep(3)

#print(driver.find_element(By.XPATH, "/html/body").text)

# Username
element = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/form/div[1]/div[2]/div/div/input")  # Replace with the correct XPath
element.send_keys(username)
element.send_keys(Keys.ENTER)
time.sleep(3)

# Password
passw = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/form/div[1]/div[2]/div[2]/div/div/input")  # Replace with the correct XPath
passw.send_keys(password)
passw.send_keys(Keys.ENTER)
time.sleep(3)


telegram_bot_sendtext(login_text)

# Navigate to the authoring page
driver.get("https://expert.chegg.com/qna/authoring/answer")
time.sleep(3)

i = 1
while True:
    try:
        driver.get("https://expert.chegg.com/qna/authoring/answer")
        time.sleep(3)
        limit = driver.current_url
        limit_text = f"{limit}"

        if limit_text != "https://expert.chegg.com/qna/authoring/answer":
           # Define the time zone (UTC+5:30)
           tz = pytz.timezone('Asia/Kolkata')
           # Get the current time in UTC+5:30
           now = datetime.now(tz)
           # Define the target time (12:30 PM)
           target_time = now.replace(hour=12, minute=30, second=0, microsecond=0)
           # If the current time is already past 12:30 PM, set the target time to the next day
           if now > target_time:
               target_time += timedelta(days=1)
           # Calculate the difference in seconds
           n = (target_time - now).total_seconds()
           telegram_bot_sendques(limit_texts)
           time.sleep(n)

        driver.get("https://expert.chegg.com/qna/authoring/answer")
        time.sleep(5)
        message = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/div[2]/div[1]")
        text_to_copy = message.text

        if text_to_copy == "Thank you for your efforts on Chegg Q&A! Unfortunately, no Qs are available in your queue at the moment.":
            driver.refresh()
            
            if i <= 1:
                telegram_bot_sendtext(i)
            elif i % 100 == 0:
                status = f"UP Running...  {i/10} {sub}"
                telegram_bot_sendtext(status)
            i += 1
            
        else:
            telegram_bot_sendques(f"{sub}")
            time.sleep(720)

    except Exception as e:
        telegram_bot_sendtext(f"An error occurred {sub}")
        
# Quit the WebDriver
driver.quit()
