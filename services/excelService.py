import pandas as pd

class ExcelService():

    def createExcel(self, lista_empresas):
        if len(lista_empresas) == 0: 
            return
        nombre_excel = input("¿Qué nombre desea darle al archivo? (Pulsa Enter para 'datos_empresas', aunque si ya tienes uno con ese nombre no generará otro) ")
        print("Generando Excel...")
        if not nombre_excel:
            nombre_excel = 'datos_empresas'
        df_empresas = pd.DataFrame(lista_empresas)
        nombre_excel_con_extension = nombre_excel + '.xlsx'
        df_empresas.to_excel(nombre_excel_con_extension, index=False)
        print(f"Datos exportados exitosamente a {nombre_excel+'.xlsx'}")
        
        