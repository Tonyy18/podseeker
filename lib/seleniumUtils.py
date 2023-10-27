from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
        
class Selenium:
    def __init__(self, gui=True):
        op = webdriver.ChromeOptions()
        if(gui == False):
            op.add_argument('--headless')
            op.add_argument("--window-size=1920,1080")
        op.add_argument("--start-maximized");
        self.driver = webdriver.Chrome(options=op)
    
    def element_is_visible(self, css, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
        except TimeoutException as e:
            return None

    def get_element(self, css):
        try:
            return self.driver.find_element(By.CSS_SELECTOR,css)
        except:
            pass

    def get_elements(self, css):
        try:
            return self.driver.find_elements(By.CSS_SELECTOR,css)
        except:
            return None

    def elements_are_visible(self, css, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
            return self.driver.find_elements(By.CSS_SELECTOR,css)
        except TimeoutException as e:
            return None
    
    def get_from_element(self, el, css):
        try:
            return el.find_element(By.CSS_SELECTOR,css)
        except:
            return None
    
    def get_all_from_element(self, el, css):
        try:
            return el.find_elements(By.CSS_SELECTOR,css)
        except:
            return None

    def remove_element(self, cl, id=None):
        sel = "getElementsByClassName('" + cl + "')"
        if(id):
            sel = "getElementById('" + id + "')"
        self.execute_script("return document." + sel + "[0].remove();")

    def click_to_point(self, el, x, y):
        action = webdriver.common.action_chains.ActionChains(self.driver)
        action.move_to_element_with_offset(el, x, y)
        action.click()
        action.perform()

    def get(self, url):
        self.driver.get(url)

    def execute_script(self, script, arguments=None):
        return self.driver.execute_script(script)
    
    def scroll_to_bottom(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        self.execute_script("window.scrollTo(0, 0)")

    def scroll_to(self, x=0, y=0):
        self.execute_script("window.scrollTo(" + str(x) + ", " + str(y) + ")");

    def quit(self):
        self.driver.quit()
        