from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import sys

url = "https://nim-lang.org/docs/lib.html"

webdriver = webdriver.Chrome(ChromeDriverManager().install())

#default search query
search_query = "print"

if (len(sys.argv) >= 2):
    search_query = ' '.join(sys.argv[1:])
    print(search_query)

wait = WebDriverWait(webdriver, 5)
webdriver.get(url)

search = webdriver.find_element_by_id("searchInput")
search.send_keys(search_query + Keys.RETURN)

print(webdriver.page_source)
# wait.until(presence_of_element_located((By.ID,"reference.external")))
# with webdriver as driver:
#    #timeout 
#    print(driver)
#    wait = WebDriverWait(driver, 5)

#    #retrieve data
#    driver.get(url)

#    #find search box
#    search = driver.find_element_by_id("searchInput")
#    search.send_keys(search_query + Keys.RETURN)

#    #wait
#    wait.until(presence_of_element_located(By.ID, "reference.external"))
