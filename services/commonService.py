from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CommonService():

    def __init__(self, driver):
        self.driver = driver

    def WaitAndClick(self, locator, seconds=10):       
        WebDriverWait(self.driver, seconds).until(
            EC.presence_of_element_located(locator)).click()
        
    def WaitAndSendKeys(self, locator, keys, seconds=10):       
        WebDriverWait(self.driver, seconds).until(
            EC.presence_of_element_located(locator)).send_keys(keys)

    def WaitAndFindElements(self, locator, seconds=10):
            WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(locator))
            return handle.find_elements(locator)
    
    def WaitAndText(self, locator, seconds=10):
            WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(locator))
            return locator.text