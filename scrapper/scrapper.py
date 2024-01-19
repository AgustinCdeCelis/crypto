#scrapp.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup



class Scrapp:
    def __init__(self,url:str,cantidad_paginas:int=10) -> None:
        self.driver = webdriver.Chrome()
        self.url = url
        self.cantidad_paginas=cantidad_paginas
        self.__html_raw = " "
        self.raw_data = []


    def call(self)->None:
        self.driver.get(self.url) #vamos a la pagina
        time.sleep(10)
        button = self.driver.find_element(By.ID, "onetrust-reject-all-handler")                       
        if button.is_displayed(): # Comprueba si el botón está visible
            button.click()


    def busqueda(self):
    
        table = self.driver.find_element(By.TAG_NAME, "table")
        self.driver.execute_script("arguments[0].scrollIntoView();", table)
        self.__html_raw = table.get_attribute("outerHTML")


    def get_data(self):
        soup = BeautifulSoup(self.__html_raw, "html.parser") #codigo fuente con selenium
        trs = soup.find_all("tr", class_="css-1cxc880")
         
        for tr in trs: 
            row_data ={}
            td = tr.find("td", class_="css-1sem0fc")
            row_data['nombre'] =td.find('p').text #primer valor
            row_data['siglas'] = td.find('span').text #segundo valor
            
            td2 = tr.find('td',class_='css-1m7ejhk')
            row_data['precio'] = td2.find('p').text
            td3 = tr.find('td',class_='css-vtw5vj')
            row_data['24hs_change'] = td3.find('p').text #cuarto valor
            row_data['24hs_volume']=tr.find('td',class_='css-15lyn3l').text
            row_data['market_cap'] =tr.find('td',class_='css-15lyn3l').text

            self.raw_data.append(row_data)
            
        print(self.raw_data)    
            # Separa el texto en dos partes
            

            
    

if __name__== '__main__':
    prueba = Scrapp('https://crypto.com/price',10)
    prueba.call()
    prueba.busqueda()
    prueba.get_data()
    