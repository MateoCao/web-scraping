from services.loginService import LoginService
from services.companiesService import CompaniesService
from services.companyService import CompanyService
from Context import Context
from services.excelService import ExcelService
from services.filtersService import FiltersService
import time
from flask import Flask, request
from flask_cors import CORS

start_time = time.time() # inicia el tiempo de ejecucion para ver cuanto tarda en ejecutarse el programa

app = Flask(__name__)

CORS(app)

class Scrapper(Context): 

    def __init__(self):
        
        super().__init__()
        self.empresas_data = []

    def run(self, seleccionarDatos=True):
        login_service = LoginService() # instancia el servicio de login
        companies_service = CompaniesService(scrapper=self.driver) # instancia el servicio companies
        excel_service = ExcelService()
        filters_service = FiltersService()
        
        parametros = request.args.to_dict()
        
        print(parametros)
        

        self.driver.get(self.BASE_URL) # iniciar_chrome.
        login_service.getDriver(self.driver)
        login_service.login(self.EMAIL, self.PSWRD) # inicia sesion con los datos de context
        self.driver.get(self.MY_NETWORK_URL) # redireccion a la pagina de la variable de context
        lista_empresas = companies_service.obtenerListaDeEmpresas() # obtiene la lista de empresas
        self.recopilarDatosDeEmpresas(lista_empresas) # lista cada empresa_data
        self.driver.quit()
        end_time = time.time() 
        execution_time = end_time - start_time # calcula el tiempo de ejecucion
        print("El programa tardó:", execution_time, "segundos en ejecutarse.")
        if seleccionarDatos:
            empresas_data_filtrada = filters_service.filtrar_datos(self.empresas_data, parametros) # filtra las empresas segun filtros de usuario
            excel_service.createExcel(empresas_data_filtrada) # crea un excel con los datos filtrados de las empresas
            print("asd")
            return empresas_data_filtrada
        else:
            excel_service.createExcel(self.empresas_data) # crea un excel con los datos filtrados de las empresas
            return self.empresas_data
    def recopilarDatosDeEmpresas(self, lsEmpresas):
        ''' recopila datos de cada empresa y los guarda en "empresas_data" '''
        
        companies_service = CompaniesService(self)
        company_service = CompanyService(self)
        print(lsEmpresas)
        
        for empresa in enumerate(lsEmpresas): 
            empresa_data = {}
            print(companies_service.extraerInformacionBasicaDeEmpresa( empresa.get_attribute("outerHTML") ))
            empresa_data.update( companies_service.extraerInformacionBasicaDeEmpresa( empresa.get_attribute("outerHTML") ) )
            company_service.AbrirNuevaVentanaCon( companies_service.GetEnlaceEmpresa( empresa.get_attribute("outerHTML") ) )
            if (not company_service.IrAcercaDe()):
                self.empresas_data.append(empresa_data) # guarda los datos basicos y pasa a la proxima empresa.
                return
            company_service.eliminarElementosNoDeseados()
            empresa_data.update(company_service.recopilarDatos_VersionChatGPT())
            company_service.cerrarVentana()
            self.empresas_data.append(empresa_data)
            
unScrapper = Scrapper()
@app.route("/run", methods=["GET"])
def run(): return unScrapper.run(seleccionarDatos=True)

#Programa principal
if __name__ == "__main__":
    app.run(debug=True, port=5000)

# empresas_data = [
#   {
#     "Nombre": "Revista Empleo",
#     "Seguidores": "773.688 seguidores",
#     "Sitio web": "http://www.revistaempleo.com",
#     "Sector": "Servicios de recursos humanos",
#     "Tamaño de la empresa": "2-10 empleados",
#     "Fundación": "2016",
#     "Especialidades": "Difusión y Ofertas de trabajo sin experiencia"
#   }, ... ]
#   
    


