# Web Scraping Simple de Libros desde Books to Scrape (**requests**, **lxml**, **XPath**)

Este script en Python realiza un **web scraping** del sitio [Books to Scrape](https://books.toscrape.com), extrayendo información relevante de los libros disponibles en el catálogo. Los datos recopilados incluyen el título del libro, la calificación en estrellas, el precio y la disponibilidad en stock. La información se guarda en un archivo `libros.json` para su posterior análisis.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instaladas las siguientes bibliotecas de Python:

- **requests**: Para realizar solicitudes HTTP.
- **lxml**: Para el procesamiento de HTML y la extracción de datos utilizando XPath.

### Instalación de dependencias

Puedes instalar las dependencias necesarias usando `pip`:

```bash
pip install requests lxml
```
o tambien puedes intalar las dependencias del archivo requirements.txt

```bash
pip install -r requirements.txt
```

## Descripción del Script

1. **Solicitud de Páginas**: El script navega por todas las páginas del sitio web, comenzando desde la página 1 hasta la última página disponible en el catálogo.
2. **Extracción de Datos**: Para cada libro encontrado, se extraen los siguientes datos:
   - **Título** del libro.
   - **Calificación** en estrellas (convertida a valores numéricos de 1 a 5).
   - **Precio** del libro.
   - **Disponibilidad** en stock.
3. **Guardado en JSON**: Toda la información recopilada se almacena en un archivo llamado `libros.json`.


## Consideraciones

- Este script está diseñado con fines educativos y de práctica de **web scraping**. La misma página [Books to Scrape](https://books.toscrape.com) tiene estos fines.
- Si bien este codigo es simple, en la posteridad realizaré lo mismo pero para un entorno big data así quede a disposición este codigo sencillo de extracción de datos y el completo.
- En este caso usé **requests** para traer los datos pero también traeré el código simple usando **selenium** para navegar cada producto y obtener datos adicionales.

## Problemas Comunes

- **Error de conexión**: Si el sitio está caído o hay problemas de red, el script mostrará un mensaje de error.
- **Cambios en la estructura del sitio**: Si la estructura del HTML cambia, los XPath utilizados pueden dejar de funcionar correctamente.

## Autor

Este script fue creado para practicar técnicas de **web scraping** utilizando **requests** y **lxml** para aplicar **XPath**.
