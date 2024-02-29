# Librerias
import requests
import json
from string import Template

# Funciones
def request_get(url):
    """Funcion de extraccion de datos desde AP
    Args:
        url (list): URL correspondiente a la API a utilizar

    Returns:
        json: Datos extraidos
    """
    return requests.get(url).json()

def extraccion(lista1, clave):
    """Extrae los elementos de la lista1 con elementos diccionarios, según la clave ingresada
    Args:
        lista1 (list): Lista de diccionarios
        clave (str): Clave a extraer e ingrear en la lista2

    Returns:
        list: Lista resultante
    """
    lista2 = []
    for elemento in lista1:
        lista2.append(elemento[clave])
    return lista2

# API
data = request_get("https://aves.ninjas.cl/api/birds")

# Variables de los diferentes elementos a utilizar
nombres = extraccion(data, 'name')
nombre_esp = extraccion(nombres, 'spanish')
nombre_eng = extraccion(nombres, 'english')
nombre_latin = extraccion(nombres, 'latin')
imagenes = extraccion(data,'images')
img = extraccion(imagenes, 'main')

# Variable con valor igual a la cantidad de elementos extraidos
cantidad_aves = len(img)

# Template de HTML, con <head>, <body> y la <section> que recibirá los div de las cards
html_template = Template(
    '''
    <!DOCTYPE html>
    
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aves de Chile</title>
        <!-- BOOTSTRAP -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        <!-- Fuente desde Font Google -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cabin:wght@400;700&family=Lobster&display=swap"
            rel="stylesheet">
        <!--- Se agrega Kit de FontAwesome -->
        <script src="https://kit.fontawesome.com/df6a1ef9d7.js" crossorigin="anonymous"></script>
        <!-- Link a archivo de estilos en CSS -->
        <link rel="stylesheet" href="assets/css/style.css">
    </head>
    <body class="bg-success-subtle text-success-emphasis">
        <h1 class="text-center py-4">Nuestras Aves</h1>
        <section class="container">
            <div class="row">
                $body
            </div>
        </section>
        <footer class="text-center py-4 bg-success text-white">
            <p class="px-4">© 2024 Aves de Chile - Desafio Latam.Todos los derechos reservados.</p>
        </footer>
        <!-- BOOTSTRAP -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
            crossorigin="anonymous">
        </script>
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"
            integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous">
        </script>
    </body>
    </html>
    ''')

# Template de los div que contienen las card de los elementos solicitados
card_template = Template(
    '''
    <div class="col-12 col-md-3 col-lg-3">
        <div class="card my-4">
            <img src="$imagen_url" class="card-img-top" alt="$nombre_latin" style"height: 50px;">
            <div class="card-body">
                <h5 class="card-title">$nombre_latin</h5>
            </div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">$nombre_esp</li>
                <li class="list-group-item">$nombre_eng</li>
            </ul>
         </div>
    </div>'''
    )

# Variable que recibe los elementos a reemplazar
entradas_html = []

# Ciclo for que itera sobre la cantidad de elementos extraidos, 
# y va agregando los diferentes elementos que compondrán el archivo html
for i in range(cantidad_aves):
    entrada = card_template.substitute(
        imagen_url=img[i],
        nombre_latin=nombre_latin[i],
        nombre_esp=nombre_esp[i],
        nombre_eng=nombre_eng[i],
        )
    entradas_html.append(entrada)

# Construccion del texto del $body    
body_content = "\n".join(entradas_html)
pagina_completa = html_template.substitute(body=body_content)

# Exportar el sitio como archivo HTML
with open("aves_de_chile.html", "w", encoding="utf-8") as file:
    file.write(pagina_completa)