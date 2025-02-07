import time
import json
import requests
import itertools
from lxml import html
import psutil #opcional para medir el rendimiento del script
import time
from datetime import date


#mido rendimiento del script
inicio = time.time()
proceso = psutil.Process()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
} #porque hay sitios que no aceptan bots


"""_________________________________________________________________________________________________
____________________________________________________________________________________________________
_________________________________OBTENGO LOS ENLACES DE CADA PAGINA_________________________________
____________________________________________________________________________________________________
_________________________________________________________________________________________________
                                                                                                """


numero_pagina=1 #para poder cambiar de página
pagina_final = 3 #solo es para darle un valor para realizar la primera iteración entre páginas luego este valor se modifica al valor real

lista_de_listas=[]

while numero_pagina <= pagina_final:
    url = f'https://books.toscrape.com/catalogue/page-{numero_pagina}.html'
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code == 200:
        tree = html.fromstring(response.content)
        total_libros = int(tree.xpath( '//strong')[0].text)
        pagina_final =  int(tree.xpath('//div/ul[contains(@class, "pager")]/li[contains(@class, "current")]/text()')[0].split('of ')[1].split('\n')[0])
        
        lista_enlaces_porpagina = tree.xpath('//article/h3/a/@href')
        lista_de_listas.append(lista_enlaces_porpagina)
        numero_pagina += 1




lista_enlaces_conmpleta = list(itertools.chain(*lista_de_listas))


"""_________________________________________________________________________________________________
____________________________________________________________________________________________________
__________________________________OBTENGO LOS DATOS DE CADA LIBRO___________________________________
____________________________________________________________________________________________________
_________________________________________________________________________________________________
                                                                                                """


lista_libros=[]

for libro in lista_enlaces_conmpleta:
    url_libro = f'https://books.toscrape.com/catalogue/{libro}'
    busqueda_libro= requests.get(url_libro, headers=HEADERS, timeout=10)
    if busqueda_libro.status_code == 200:
        tree = html.fromstring(busqueda_libro.content)
        try:
            titulo = tree.xpath('//h1/text()')[0]
        except:
            titulo = None
    
        try:
            categoria = tree.xpath('//ul[contains(@class, "breadcrumb")]/li[3]/a/text()')[0]
        except:
            categoria = None
    
        try:
            precio = float(tree.xpath('//p[contains(@class, "price_color")]/text()')[0].replace('£', ''))
        except:
            precio = None
    
        try:
            disponibles = int(tree.xpath('//p[contains(@class, "instock")]/text()')[1].strip().split("(")[1].split()[0])
        except:
            disponibles = None
    
        try:
            estrellas = tree.xpath('//p[contains(@class, "star-rating")]/@class')[0].split()[-1].lower()
            estrellas_dicc = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
            estrellas = estrellas_dicc.get(estrellas, 0)
        except:
            estrellas = None
    
        try:
            descripcion = tree.xpath('//article/p/text()')
            descripcion = descripcion[0] if descripcion else None
        except:
            descripcion = None
    
        try:
            upc = tree.xpath('//table//th[text()="UPC"]/following-sibling::td/text()')[0]
        except:
            upc = None
    
        try:
            price_excl_tax = float(tree.xpath('//table//th[text()="Price (excl. tax)"]/following-sibling::td/text()')[0].replace('£', ''))
        except:
            price_excl_tax = None
    
        try:
            price_incl_tax = float(tree.xpath('//table//th[text()="Price (incl. tax)"]/following-sibling::td/text()')[0].replace('£', ''))
        except:
            price_incl_tax = None
    
        try:
            tax = float(tree.xpath('//table//th[text()="Tax"]/following-sibling::td/text()')[0].replace('£', ''))
        except:
            tax = None
    
        try:
            resenas = int(tree.xpath('//table//th[text()="Number of reviews"]/following-sibling::td/text()')[0])
        except:
            resenas = None
    
        try:
            imagen = tree.xpath('//div[contains(@id, "gallery")]/div/div/div/img/@src')[0]
            imagen = "https://books.toscrape.com" + imagen.replace("../", "/")
        except:
            imagen = None
    
        hoy = date.today().strftime("%Y-%m-%d")

        libro_info = {
            "Title": titulo,
            "Stars": estrellas,
            "Price (euros)": precio,
            "Stock": disponibles,
            "Category": categoria,
            "Description": descripcion,
            "UPC": upc,
            "Price (excl. tax)": price_excl_tax,
            "Price (incl. tax)": price_incl_tax,
            "Tax": tax,
            "Number of reviews": resenas,
            "Image": imagen,
            "Link": url_libro,
            "Date": hoy
        }
        lista_libros.append(libro_info)
        time.sleep(0.2)


"""_________________________________________________________________________________________________
____________________________________________________________________________________________________
_____________________________________CREO EL JSON CON LOS DATOS_____________________________________
____________________________________________________________________________________________________
_________________________________________________________________________________________________
                                                                                                """


#En caso de haber obtenido datos de aunque sea 1 libro, creo el archivo json con los datos
if len(lista_libros) != 0:
    with open('libros.json', 'w', encoding='utf-8') as f:
        json.dump(lista_libros, f, ensure_ascii=False, indent=4)
    print(f"Obtención de datos finalizada. {len(lista_libros)} libros procesados de {total_libros} disponibles.")
else:
    print("No se obtuvo datos de ningun libro")



#mido rendimiento del script
fin = time.time()
uso_memoria = proceso.memory_info().rss / (1024 * 1024)  # Convertir a MB
uso_cpu = proceso.cpu_percent(interval=1)

print(f"Tiempo: {fin - inicio:.4f} segundos")
print(f"Memoria usada: {uso_memoria:.2f} MB")
print(f"Uso de CPU: {uso_cpu:.2f}%")