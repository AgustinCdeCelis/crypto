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
        print(len(trs))
        
        trs = soup.select("tr.css-1cxc880")

        for tr in trs:
    # Obtiene el elemento <td> con la clase "css-1sem0fc"
            td = tr.find("td", class_="css-1sem0fc")

            print(td.text)
    # Obtiene el texto del elemento <td>



        #soup = BeautifulSoup(page_source, "html.parser") #parser de la pagina
        #print(type(soup))
        #time.sleep(500)
        #print(soup)

if __name__== '__main__':
    prueba = Scrapp('https://crypto.com/price',10)
    prueba.call()
    prueba.busqueda()
    prueba.get_data()
    