#scrapp.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

__all__=['Scrapp']

class Scrapp:
    def __init__(self,url:str,cantidad_paginas:int=10) -> None:
        self.driver = webdriver.Chrome()
        self.url = url
        self.cantidad_paginas=cantidad_paginas
        self.pagina = 1
        self.__html_raw = " " #tags a partir de la tabla
        self.raw_data = [] #lista de tablas


    def call(self)->None:
        self.driver.get(self.url) #vamos a la pagina
        time.sleep(10)
        button = self.driver.find_element(By.ID, "onetrust-reject-all-handler")                       
        if button.is_displayed(): # Comprueba si el botón está visible
            button.click()


    def busqueda(self)->None:
    
        table = self.driver.find_element(By.TAG_NAME, "table") #busco tabla
        self.driver.execute_script("arguments[0].scrollIntoView();", table)
        self.__html_raw = table.get_attribute("outerHTML")


    def get_data(self)->None:
        soup = BeautifulSoup(self.__html_raw, "html.parser") #codigo fuente con selenium
        trs = soup.find_all("tr", class_="css-1cxc880") #estos son las filas de la tabla
        for tr in trs: 
            row_data ={}
            row_data['fecha'] = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
            td = tr.find("td", class_="css-1sem0fc")
            row_data['nombre'] =td.find('p').text #primer valor
            row_data['siglas'] = td.find('span').text #segundo valor
            td2 = tr.find('td',class_='css-1m7ejhk')
            row_data['precio'] = td2.find('p').text #tercer valor
            td3 = tr.find('td',class_='css-vtw5vj')
            row_data['24hs_change'] = td3.find('p').text #cuarto valor
            row_data['24hs_volume']=tr.find('td',class_='css-15lyn3l').text #quinto
            row_data['market_cap'] =tr.find('td',class_='css-15lyn3l').text #sexto

            self.raw_data.append(row_data) #almaceno en lista

    def transform(self)->None:
        fecha = datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        archivo= f"./data/datos_{fecha}.csv"
        df = pd.DataFrame(self.raw_data)
        df.to_csv(archivo,index=False)
        print(f"CSV file saved as: {archivo}")  # Print a confirmation message

    def next(self)->bool:
        if self.pagina < self.cantidad_paginas:
            self.pagina+=1
            add_str=f'?page{self.pagina}'
            pagina = self.url +add_str
            element = self.driver.find_element(By.CSS_SELECTOR,'button.chakra-button.css-1c62rym')
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            if element.text=='2':
                element.click()
            time.sleep(5)
            print(pagina)
            
def test():
    start_time = time.perf_counter()
    prueba = Scrapp('https://crypto.com/price',10)
    prueba.call()
    prueba.busqueda()
    prueba.get_data()
    prueba.transform()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    prueba.next()
    print(f"Execution time: {execution_time:.4f} seconds")
            
    

if __name__== '__main__':
    test()
    