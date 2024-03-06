from HandleDriver import HandleDriver

class Context():
    
    def __init__(self):
        self.BASE_URL = "https://www.linkedin.com/login/es"
        self.MY_NETWORK_URL = "https://www.linkedin.com/mynetwork/network-manager/company/"
        self.EMAIL =  "mateocao@hotmail.com"  # "abel.angel96@outlook.es" 
        self.PSWRD =  "Villavicencio23" # "TrabajosIt2023" 

        self.handle_driver = HandleDriver()
        self.handle_driver.initialize_driver(headless=False)
        self.driver = self.handle_driver.get_driver()
