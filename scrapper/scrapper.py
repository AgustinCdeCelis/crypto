#scrapp.py
from selenium import webdriver
from bs4 import BeautifulSoup


class Scrapp:
    def __init__(self,url:str,cantidad_paginas:int=10) -> None:
        self.driver = webdriver.Chrome()
        self.url = url
        self.cantidad_paginas=cantidad_paginas

    def get_data(self):
        self.driver.get(self.url)
        # Obtenemos el código fuente de la página
        page_source = self.driver.page_source
        # Creamos un objeto BeautifulSoup para analizar el código fuente
        soup = BeautifulSoup(page_source, "html.parser")
        print(soup)

if __name__== '__main__':
    prueba = Scrapp('https://crypto.com/price',10)
    prueba.get_data()
    