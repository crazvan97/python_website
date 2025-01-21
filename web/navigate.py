# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Main Function
if __name__ == '__main__':
    # Provide the email and password
    website = 'https://www.olx.ro/anunturi-agricole/utilaje-agricole/utilaje-industriale-si-de-constructii/buldoexcavator/?currency=EUR'
    accept_cookies = '/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[1]'

    # Provide the path of chromedriver present on your system.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    # Send a get request to the url
    driver.get(website)
    # time.sleep(3)

    # Accept cookies
    driver.find_element(By.XPATH, accept_cookies).click()
    time.sleep(3)

    # Extend Mark field
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div[4]/div/div[2]/div/div/span').click()
    time.sleep(1)

    # Select Cat and Caterpillar
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div[4]/div/div[2]/div[2]/div/div[22]/label').click()
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div[4]/div/div[2]/div[2]/div/div[23]/label').click()
    time.sleep(1)

    # Set the Price
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div[5]/div[2]/div[2]/div/div[1]/div/input').send_keys("40000")
    time.sleep(1)

    # Set the Year
    year = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[3]/div[1]/div/div[6]/div[2]/div[1]/div/div/div/input')
    year.send_keys('2006')
    time.sleep(1)

    # Press Search
    driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[1]/div[3]/button').click()
    time.sleep(1)

    results = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/form/div[4]/div[2]/span/span').text
    print(results)

    all_results = driver.find_elements(By.CLASS_NAME, 'baxter-container')
    for result in all_results:
        print(result.text)

    time.sleep(40)
    # Quits the driver
    driver.close()
    driver.quit()
