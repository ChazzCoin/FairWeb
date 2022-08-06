from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome()
driver.get("https://public.totalglobalsports.com/public/event/2038/individual-team/18/11332/9")
print(driver.title)
# test = driver.find_elements(by=By.CLASS_NAME, value="table")
search_bar = driver.find_element_by_name("table")
print(search_bar)