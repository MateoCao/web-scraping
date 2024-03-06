from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

class CompanyService():

    def __init__(self, scrapper):
        self.driver = scrapper.driver
        self.acerca_de = None
        self.algo = None

    def WaitAndFindElements(self, locator, seconds=10):
            (locatorStrategy, values) = locator
            WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(locatorStrategy, values)
    
    def WaitAndText(self, locator, seconds=10):
        (locatorStrategy, values) = locator
        WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(locator))
        return self.driver.find_element(locatorStrategy, values).text
    
    def AbrirNuevaVentanaCon(self, enlace):
        ''' abre una nueva ventana que redirecciona al enlace y se posiciona sobre ella'''
        if enlace:
            self.driver.execute_script(f"window.open('{enlace}', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
    
    def IrAcercaDe(self):
            ''' Hacer clic en la pestaña "Acerca de"
            precondicion: estar en la pagina linkedin de una empresa '''
            try:
                self.acerca_de = self.driver.find_element(By.XPATH, "//li[contains(.,'Acerca de')]//a/..")
                self.acerca_de.click()
                time.sleep(5)
                return True
            except NoSuchElementException as e:
                print("Página no disponible, continua con la siguiente", e)
                return False

    def eliminarElementosNoDeseados(self):
        ''' abel: no se que hace este metodo. '''
        # Esperar y encontrar elementos adicionales     
        selected_elements = self.WaitAndFindElements((By.XPATH,"//dd"))

        # Eliminar elementos no deseados
        for element in selected_elements:
            if "miembros asociados" in element.text:
                self.driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)
                break

    def cerrarVentana(self):
        self.driver.close() # cerrar ventana actual
        print("exec cerrar ventana")
        self.driver.switch_to.window(self.driver.window_handles[0]) # ir(volver) a ventana principal

    # scrape_additional_data
    def recopilacionOpcionalDeDatos(self):
        """ Recopila datos adicionales de la empresa. """
 
        datos_adicionales_empresa = {} # Inicializar el diccionario para almacenar datos adicionales      
        numero_de_datos_a_obtener = self.WaitAndFindElements( (By.XPATH, "//div[contains(@id,'ember')]//dt") ) # Obtener la lista de elementos a partir del tag "dd"

        # Iterar sobre los elementos y recopilar datos
        for dato_index, _ in enumerate(numero_de_datos_a_obtener):
            # Esperar a que el elemento esté presente y obtener su texto
            nombre_del_campo = self.WaitAndText( (By.XPATH, f"//div[contains(@id,'ember')]//dt[{dato_index + 1}]") )
            valor_del_campo = self.handleValuesDD(f"//div[contains(@id,'ember')]//dd[{dato_index + 1}]")
            datos_adicionales_empresa[nombre_del_campo] = valor_del_campo
            print(str({dato_index + 1}) + ": " + str(datos_adicionales_empresa) )

        return datos_adicionales_empresa
    
    def handleValuesDD(self, locator):
        ''' si el dd tiene varios valores retorna una lista de valores, caso contrario retorna el texto del dd'''
        # (c, v) = locator # separo los elementos de la tupla
        e = self.driver.find_element(By.XPATH, locator) # busco los elementos del locator
        soup = BeautifulSoup(e.get_attribute("outerHTML"), "html.parser") # Crear un objeto BeautifulSoup para facilitar el análisis del HTML

        lsli = [] # ls = lista, lsli = lista de li

        if soup.find("ul"):  # Si hay un ul..
            for index, li in enumerate( soup.find_all('li') ): # por cada li..
                 print(f'li {index}:' + str(li))
                 lsli.append( li.get_text(strip=True) ) # agrega el texto del li a la lista.
        else: # Si no hay un ul...
            lsli = soup.find("dd")
            lsli = lsli.get_text(strip=True) # pisa la lista y la reemplaza por el texto de dd

        return lsli # retorna una ls de los valores de cada li o retorna el texto de dd
    
    def recopilarDatosEnBloquesDl(self):
        lsdl = self.driver.find_elements(By.XPATH, '//dl') # ls = lista, lista de bloques con etiqueta dl.
        lsdl_soup = []

        # transforma cada dl, uno por uno. (no se puede hacer sobre todos directamente)
        for dl in lsdl:
            # lista de bloques con etiqueta dl transformada a soup.
            dl_soup = BeautifulSoup(dl.get_attribute("outerHTML"), "html.parser")
            lsdl_soup.append(dl_soup) 

        lsdl_soup_filtered = [] # lista de dl filtrada por las que tienen 'dt' (dado que existen dl vacias)

        for dl in lsdl_soup: # dado la lista de dl soup
            if dl.find('dt'): # si tiene 'dt'
                lsdl_soup_filtered.append(dl) # se agrega a la lista

        datos_emp = {}

        # recorre cada dl una cantidad_dt de veces y guarda los datos en datos_emp
        for dl in lsdl_soup_filtered:
            ls_dt = dl.find_all('dt') # obtiene la cantidad de dt en el dl
            for index,_ in enumerate(ls_dt): # recorre la cantidad de veces cant_dt
                dt = dl.find(f'dt[{index+1}]') # extrae un dt del dl
                dd = dl.find(f'dd[{index+1}]') # extrae un dd del dl
                datos_emp[dt] = dd # los guarda en este formato clave-valor

        print(datos_emp)
        return datos_emp

    def paginaDisponible(self, tiempo_espera=10):
        try:
            # Esperar hasta que el elemento esté presente en la página
            WebDriverWait(self.driver, tiempo_espera).until(
                EC.presence_of_element_located((By.XPATH, "//li[contains(.,'Acerca de')]//a/.."))
            )            
            return True # Si la espera tiene éxito, retornar True
        except Exception as e:     
            return False # Si la espera falla retornar False

    def recopilarDatos_VersionChatGPT(self):
        lsdl = self.driver.find_elements(By.XPATH, '//dl') # Encuentra todos los elementos <dl>

        lsdl_soup = []

        # transforma cada dl, uno por uno. (no se puede hacer sobre todos directamente)
        for dl in lsdl:
            # lista de bloques con etiqueta dl transformada a soup.
            dl_soup = BeautifulSoup(dl.get_attribute("outerHTML"), "html.parser")
            lsdl_soup.append(dl_soup) 

        datos_emp = {}  # Diccionario para almacenar los datos
       
        for dl in lsdl_soup: # Itera sobre cada elemento <dl>           
            if dl.find('dt'): # Verifica si el <dl> tiene al menos un <dt>
                ls_dt = dl.find_all('dt') # Encuentra todos los elementos <dt> y <dd> dentro del <dl>
                ls_dd = dl.find_all('dd') # Encuentra todos los elementos <dt> y <dd> dentro del <dl>

                for dt, dd in zip(ls_dt, ls_dd): # Itera sobre los elementos <dt> y <dd> y almacena en datos_emp
                    datos_emp[dt.get_text(strip=True)] = dd.get_text(strip=True)

        return datos_emp
    
    def recopilarDatos_VersionChatGPT_Mateo(self):
        # Encuentra todos los elementos <dl>
        lsdl = self.driver.find_elements(By.XPATH, '//dl')

        lsdl_soup = []

        # transforma cada dl, uno por uno. (no se puede hacer sobre todos directamente)
        for dl in lsdl:
            # lista de bloques con etiqueta dl transformada a soup.
            dl_soup = BeautifulSoup(dl.get_attribute("outerHTML"), "html.parser")
            lsdl_soup.append(dl_soup) 

        datos_emp = {}  # Diccionario para almacenar los datos
        lssdd = []

        for dl in lsdl_soup: # Itera sobre cada elemento <dl> dl -> dt / dt
            lsdt = dl.find_all('dt')
            for dt in lsdt: 
                lsdd = []
                if dt:
                    dt_y_dd = dt.find_next_siblings()
                    for element in dt_y_dd: 
                        if element.name == 'dd':
                            lsdd.append(element) 
                        else:   
                            lssdd.append(lsdd)
                            break              

                # for dt, dd in zip(ls_dt, ls_dd): # Itera sobre los elementos <dt> y <dd> y almacena en datos_emp
                #    datos_emp[dt.get_text(strip=True)] = dd.get_text(strip=True)

        print("Datos recopilados:") # Imprime los resultados
        for clave, valor in datos_emp.items():
            print(f"{clave}: {valor}")

        # Supongamos que tienes un objeto BeautifulSoup llamado soup que contiene tu HTML


    
    