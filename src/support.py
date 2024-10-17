from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import datetime

def web_response(url):
    """
    Realiza una solicitud GET y devuelve la respuesta si es exitosa.
    """
    response = requests.get(url)
    code = response.status_code
    if code == 200:
        return response
    else:
        print(f"Error, respuesta recibida: {code}")
        print(f"Ha fallado la url: {url}")
        return np.nan

def convert_to_soup(tosoupcontent):
    """
    Convierte el contenido en un objeto BeautifulSoup.
    """
    soup = BeautifulSoup(tosoupcontent.content, "html.parser")
    return soup

def obtain_elements(searchresultlist):
    """
    Extrae texto de una lista de elementos HTML.
    """
    element_operation = [element.getText() for element in searchresultlist]
    return element_operation

def format_dimension(dimension):
    """
    Formatea una cadena de dimensiones, eliminando saltos de línea y "(cm)".
    """
    operation = dimension.replace("\n","").replace(" (cm)","")
    return operation

def format_section(section):
    """
    Formatea una cadena de texto de secciones, eliminando caracteres extra.
    """
    operation = section.strip().replace("\xa0\xa0"," ")
    return operation

def obtain_name(soup):
    """
    Extrae los nombres de los elementos HTML con la clase 'title'.
    """
    lista_nombre_atrezo = soup.findAll('a',{'class':'title'})
    nombre_atrezo = obtain_elements(lista_nombre_atrezo)
    return nombre_atrezo

def obtain_category(soup):
    """
    Extrae las categorías de los elementos HTML con la clase 'product-slide-entry shift-image'.
    """
    lista_categoria_atrezo = soup.findAll('div',{'class':'product-slide-entry shift-image'})
    categoria_atrezo = [categoria.contents[2].getText() for categoria in lista_categoria_atrezo]
    return categoria_atrezo

def obtain_section(soup):
    """
    Extrae y formatea las secciones de los elementos con la clase 'cat-sec-box'.
    """
    lista_seccion_atrezo = soup.findAll("div",{"class":"cat-sec-box"})
    seccion_atrezo = [element.getText() for element in lista_seccion_atrezo]
    seccion = list(map(format_section,seccion_atrezo))
    return seccion

def obtain_description(soup):
    """
    Extrae y formatea las descripciones de los elementos con la clase 'product-slide-entry shift-image'.
    """
    lista_descripcion_atrezo = soup.findAll("div",{"class":"product-slide-entry shift-image"})
    descripcion_atrezo = [descripcion.getText() for descripcion in lista_descripcion_atrezo]
    descripcion = list(map(format_dimension,descripcion_atrezo))
    return descripcion

def obtain_dimensions(soup):
    """
    Extrae y formatea las dimensiones de los elementos con la clase 'price'.
    """
    lista_dimensiones_atrezo = soup.findAll("div",{"class":"price"})
    dimensiones_atrezo = obtain_elements(lista_dimensiones_atrezo)
    dimensiones = [format_dimension(dimension) for dimension in dimensiones_atrezo]
    return dimensiones

def obtain_image_url(soup):
    """
    Extrae las URLs de las imágenes de los elementos con la clase 'product-image'.
    """
    lista_imagen_atrezo = soup.findAll("div",{"class":"product-image"})
    imagenes_atrezo = [f"https://atrezzovazquez.es/{imagen.contents[0].get('src')}" for imagen in lista_imagen_atrezo]
    return imagenes_atrezo

def create_df(webpage):
    """
    Crea un DataFrame con la información extraída de la página web.
    """
    contact = web_response(webpage)
    if contact.status_code == 200:
        soup = convert_to_soup(contact)
        name_list = obtain_name(soup)
        category_list = obtain_category(soup)
        section_list = obtain_section(soup)
        description_list = obtain_description(soup)
        dimension_list = obtain_dimensions(soup)
        image_list = obtain_image_url(soup)

        df = pd.DataFrame({
            "Nombre": name_list,
            "Categoría": category_list,
            "Sección": section_list,
            "Descripción": description_list,
            "Dimensiones": dimension_list,
            "URL Imágenes": image_list
        })
        return df
    else:
        return
