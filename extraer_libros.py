import requests
from lxml import html
import json



numero_pagina=1
lista_libros = []
pagina_final = 3 #solo es para darle un valor para realizar la primera iteración entre páginas luego este valor se modifica al valor real


while numero_pagina <= pagina_final:
  url = f'https://books.toscrape.com/catalogue/page-{numero_pagina}.html'
  response = requests.get(url)
  

  if response.status_code == 200:
    tree = html.fromstring(response.content)
    pagina_final =  int(tree.xpath('//div/ul[contains(@class, "pager")]/li[contains(@class, "current")]/text()')[0].split('of ')[1].split('\n')[0])
    libros = tree.xpath('//article')

    for libro in libros:
      #Obtengo los datos que me interesan
      estrellas = libro.xpath('p/@class')[0].split(" ")[1].lower()
      
      titulo = libro.xpath('h3/a/@title')[0]
      
      precio = libro.xpath('div[contains(@class, "price")]/p[contains(@class, "price")]/text()')[0]
      
      stock = libro.xpath('div[contains(@class, "price")]/p[contains(@class, "stock")]/i/@class')[0].split("-")[1]
      
      #Transformo los valores de estrellas a enteros
      estrellas_dicc = {
          "one" : 1,
          "two" : 2,
          "three" : 3,
          "four" : 4,
          "five" : 5
      }

      estrella = estrellas_dicc.get(estrellas, 0)

      #creo el diicionario con los datos
      libro_info = {
          "Title" : titulo,
          "Stars" : estrella,
          "Price" : precio,
          "Stock" : stock
      }
      #incorporo los datos del libro a la lista
      lista_libros.append(libro_info)
    

    
  elif response.status_code != 200:
    print("Error al encontrar la página")
  numero_pagina += 1

#En caso de haber obtenido datos de aunque sea 1 libro, creo el json
if len(lista_libros) != 0:
  with open('libros.json', 'w', encoding='utf-8') as f:
      json.dump(lista_libros, f, ensure_ascii=False, indent=4)
  print("Obtención de datos finalizada")
else:
  print("No se obtuvo datos de ningun libro")