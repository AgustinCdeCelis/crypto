from .scrapper import *

__all__ =[scrapper.__all__]


def crypto_scrapp(num):
    prueba = Scrapp(num)
    print(prueba)

    for pagina in range(prueba.cantidad_paginas):
        prueba.call()
        prueba.busqueda()
        prueba.next()
        
    prueba.get_data()
    prueba.transform()