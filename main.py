import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Fake url for shopping cart automation

# In the same folder create a file named .env with credentials
# Loads variables from .env
load_dotenv()  
# Retrieve credentials from environment variables
username_val = os.getenv('MY_APP_USERNAME')
password_val = os.getenv('MY_APP_PASSWORD')

if not username_val or not password_val:
    raise ValueError("Username and/or password environment variables not set.")

chrome_options = Options()
# Arguments to prevent popup windows
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False
}
chrome_options.add_experimental_option("prefs", prefs)
# Additional arguments to prevent popup windows
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-save-password-bubble")
driver = webdriver.Chrome(options=chrome_options) 
driver.maximize_window()

# --- login ---
def login(username_val, password_val):
    try:
        driver.get("https://www.saucedemo.com/")
        username_field = driver.find_element(By.ID, "user-name") 
        password_field = driver.find_element(By.ID, "password") 
        login_button = driver.find_element(By.ID, "login-button") 
        username_field.send_keys(username_val)
        password_field.send_keys(password_val)
        login_button.click()
        print("Login successful!")
        login = "Login successful!"
    except Exception as e:
        print(f"Failed to login: {e}")
        login = f"Failed to login: {e}"
    return login

# --- add to cart --- 
def add_to_cart(product_url):
    driver.get(product_url)
    wait = WebDriverWait(driver,10)
    try:
        item_name = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "[data-test='inventory-item-name']")))
        item_name.click()
        add_to_cart_btn = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "[data-test='add-to-cart']")))
        add_to_cart_btn.click()
        shopping_cart = add_to_cart_btn = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "[data-test='shopping-cart-link']")))
        shopping_cart.click()
        print("Item added to cart!")
        cart = "Item added to cart!"
    except Exception as e:
        print(f"Failed to add item: {e}")
        cart = f"Failed to add item: {e}"
    return cart

# -- checkout --
def checkout(cart_url):
    driver.get(cart_url)
    wait = WebDriverWait(driver,10)
    selected_prod_name = "Sauce Labs Backpack"
    try:
        checkout_btn = wait.until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "[data-test='checkout']")))
        checkout_btn.click()
        first_name_field = driver.find_element(By.ID, "first-name")
        first_name_field.send_keys("John")
        last_name_field = driver.find_element(By.NAME, "lastName")
        last_name_field.send_keys("Lennon")
        postalCode_field = driver.find_element(By.ID, "postal-code")
        postalCode_field.send_keys("84531")
        continue_btn = driver.find_element(By.NAME, "continue")
        continue_btn.click()
        product_name = driver.find_element(By.CSS_SELECTOR, "[data-test='inventory-item-name']")
        name = product_name.text
        assert(selected_prod_name == name)   
        finish_btn = driver.find_element(By.ID, "finish")  
        finish_btn.click()
        print("Checkout OK")
        checkout = "Checkout OK"
    except Exception as e:
        print(f"Failed to checkout: {e}")  
        checkout = f"Failed to checkout: {e}" 
    return checkout

# --- checkout completed --- 
def checkout_complete(thanks_url):
    driver.get(thanks_url)
    thank_you = "Checkout: Complete!"
    try:
        element = driver.find_element(By.CSS_SELECTOR, "[data-test='title']")
        thanks = element.text
        assert(thank_you == thanks)
        print("Thank you page displayed")
        confirm = "Thank you page displayed"
        back_home_btn = driver.find_element(By.NAME, "back-to-products")
        back_home_btn.click()
        flag = "Products"
        element = driver.find_element(By.CSS_SELECTOR, "[data-test='title']")
        homepage = element.text
        assert(homepage == flag)
        print("Returned to Home")
        home = "Returned to Home"
    except Exception as e:
        print(f"Failed to back home: {e}")
        confirm = f"Failed to confirm: {e}"
        home = f"Failed back to home: {e}"
    return confirm, home

# Shopping Cart URLs after login successful
product_url = "https://www.saucedemo.com/inventory.html"
cart_url = "https://www.saucedemo.com/cart.html"
thanks_url = "https://www.saucedemo.com/checkout-complete.html"
    
# --- Execution ---
if __name__ == "__main__":
    current_datetime = datetime.now()
    datetime_string = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
    login = login(username_val, password_val)
    cart = add_to_cart(product_url)
    checkout = checkout(cart_url)
    values = checkout_complete(thanks_url)
    confirm, home = values
    
    # HTML file with variables
    original_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Execution Report</title>
    </head>
    <body>
        <h2>Test automation using Python + Selenium</h2>
        <h3>It uses fake shopping cart testing purpose</h3>
        <h4>Execution Report</h4>
        <p>Last run: {{ datetime_string }}</p>
        <p>Below are the statuses from steps</p>
        <p><b>Login:</b> {{ login }}</p>
        <p><b>Add item to cart:</b> {{ cart }}</p>
        <p><b>Checkout:</b> {{ checkout }}</p>
        <p><b>Confirm checkout:</b> {{ confirm }}</p>
        <p><b>Back to home:</b>  {{ home }}</p>
    </body>
    </html>
    """
    # Clean the last result values from index.html and restore variables
  
    with open('index.html', 'w') as file:
        file.write(original_content)
    
    # Set up the Jinja2 environment
    env = Environment(loader=FileSystemLoader('.')) 
    template = env.get_template('report_template.html')
    
    # Render the template with data
    output = template.render( 
        datetime_string=datetime_string, 
        login=login, cart=cart, 
        checkout=checkout, 
        confirm=confirm, 
        home=home)                          
    
    # Save the output to a index file
    with open("index.html", "w") as file:
        file.write(output) 
        file.close()

driver.quit()