from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import os

# Fake url for shopping cart automation

# In the same folder create a file named .env with credentials

# Retrieve credentials from environment variables
username_val = os.getenv('MY_APP_USERNAME')
password_val = os.getenv('MY_APP_PASSWORD')

if not username_val or not password_val:
    raise ValueError("Username and/or password environment variables not set.")


driver = webdriver.Chrome() 
driver.get("https://www.saucedemo.com/")

username_field = driver.find_element(By.ID, "user-name") 
password_field = driver.find_element(By.ID, "password") 
login_button = driver.find_element(By.ID, "login-button") 

username_field.send_keys(username_val)
password_field.send_keys(password_val)
login_button.click()



