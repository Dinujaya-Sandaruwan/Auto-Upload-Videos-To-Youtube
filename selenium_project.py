from selenium_project import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Wait Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



PATH = 'C:\Program Files (x86)\chromedriver.exe'
# PATH = 'C:\Program Files (x86)\msedgedriver.exe'
driver = webdriver.Chrome(PATH) # Selenium also supports edge and firefox
driver.get("https://www.techwithtim.net/")

search = driver.find_element_by_name("s")
search.clear()
search.send_keys("test")
search.send_keys(Keys.RETURN) # RETURN = Enter

main = driver.find_element_by_id("main")
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    # print(main.text)
    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)
    
# except: (මේකෙන් වෙන්නෙ Try එකේ එක වුනේ නැත්තන් වෙන දේ)
finally: # මේකෙන් වෙන්නෙ Try එකේ එක වුනාට පස්සෙ වෙන දේ
    driver.quit()


# time.sleep(5)
# driver.quit()