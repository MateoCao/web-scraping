from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

class CompaniesService():

    def __init__(self, scrapper=None, driver=None):
        self.driver = driver if scrapper == None else scrapper
   
    def obtenerListaDeEmpresas(self, scroll=True):
        ''' obtiene la lista de empresas de la pagina '''
        if (scroll):
            cant_elements = len( self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container" )) # guarda la cantidad de empresas    
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);") # scrolea hacia el final de la pagina
            time.sleep(3) # espera 3 segundos
            new_cant_elemets = len( self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container" )) # guarda la cantidad de empresas despues de scrolear

            while cant_elements != new_cant_elemets: # si la cantidad es distintas despues del scroll entonces repetir el proceso.
                    cant_elements = new_cant_elemets
                    self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);") 
                    time.sleep(3)
                    new_cant_elemets = len( self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container" ))

            print(f'cantidad de empresas listadas: {cant_elements} ({new_cant_elemets})')
        try:
            lista_empresas = self.driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
            if (len(lista_empresas) == 0):
                print("Error al obtener la lista de empresas")
        except:
            print("Error al obtener la lista de empresas")
        return lista_empresas

    def extraerInformacionBasicaDeEmpresa(self, html_empresas):
        ''' desde la pagina de listados de empresas, retorna el nombre y seguidores de la empresa pedida'''
        soup = BeautifulSoup(html_empresas, "html.parser") # Crear un objeto BeautifulSoup para facilitar el análisis del HTML
        nombre_empresa = soup.find("span", class_="entity-result__title-text").get_text(strip=True) # Obtener el nombre de la empresa
        seguidores_empresa = soup.find("span", class_="member-insights__reason").get_text(strip=True) # Obtener el número de seguidores de la empresa   

        datos_empresa = {}

        datos_empresa["Nombre"] = nombre_empresa
        datos_empresa["Seguidores"] = seguidores_empresa

        return datos_empresa
        
    def GetEnlaceEmpresa(self, html_empresas):
        ''' retorna el enlace a la pagina linkedin de la empresa '''
        soup = BeautifulSoup(html_empresas, "html.parser") # Crear un objeto BeautifulSoup para facilitar el análisis del HTML
        enlace = soup.find("a", class_="app-aware-link")  # Obtener el enlace a la empresa
        print(enlace.get("href"))
        return enlace.get("href") # Extraer el valor del enlace



