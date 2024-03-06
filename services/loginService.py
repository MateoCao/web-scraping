from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException 

class LoginService():
    ''' servicio para iniciar sesion '''
    def getDriver(self, scraper):
      ''' necesita recibir el scraper '''
      self.driver = scraper
    def login(self, email, password):
        self.txt_username = None
        self.txt_password_field = None
        self.btn_submit = None
        ''' inicia sesion con un email y password '''
        try:
          self.txt_username = self.driver.find_element(By.XPATH, "//*[@id='username']")
          self.txt_password_field = self.driver.find_element(By.XPATH, "//*[@id='password']")
          self.btn_submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")

          self.txt_username.send_keys(email)
          self.txt_password_field.send_keys(password)
          self.btn_submit.click()
        except NoSuchElementException as e:
          print("ERROR AL INICIAR SESION", e)
          
    # def verifyLogin(self, login_state):
    #     if login_state == False:
    #       self.successfull_login = False
    #     return self.successfull_login
          
    def login2(self, email, password):
      #  common_service = CommonService(self.driver)

        print(f'self: {self}')
        print(f'email: {email}')
        print(f'password: {password}')

      #  common_service.WaitAndSendKeys(self.txt_username, email)
      #  common_service.WaitAndSendKeys(self.txt_password_field, password)
      #  common_service.WaitAndClick(self.btn_submit)
        


