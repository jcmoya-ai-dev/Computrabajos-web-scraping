import json
import csv

# Lee el archivo JSON
with open('ContentMultitrabajos.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extrae la lista de contenidos
content_list = data['content']

# Define los nombres de las cabeceras
headers_original = [
    "id","origen", "titulo", "empresa", "paisEmpresa", "descripcion", "aptoDiscapacitado", "idEmpresa",
    "confidencial", "logoURL", "fechaHoraPublicacion", "fechaPublicacion",
    "planPublicacion.id", "planPublicacion.nombre", "portal", "tipoTrabajo",
    "idPais", "idArea", "idSubarea", "leido", "visitadoPorPostulante",
    "localizacion", "cantidadVacante", "guardado", "gptwUrl", "match",
    "promedioEmpresa", "modalidadTrabajo", "tipoAviso"
]

# Define los nombres de las cabeceras
headers = [
    "id","origen", "titulo", "empresa", "paisEmpresa", "descripcion", "aptoDiscapacitado", "fechaHoraPublicacion",
    "tipoTrabajo", "idArea", "localizacion", "cantidadVacante", "promedioEmpresa", "modalidadTrabajo", "tipoAviso"
]

# Crea una lista de filas para el CSV
rows = []
for item in content_list:
    # Reemplaza comas por puntos en titulo y detalle
    titulo = item.get('titulo', '').replace(',', '.')
    descripcion = item.get('detalle', '').replace(',', '.')
    origen = 'multitrabajos'
    paisEmpresa='Ecuador'

    row = [
        item.get('id', ''),
        origen,
        titulo,
        item.get('empresa', ''),
        paisEmpresa,
        descripcion,
        item.get('aptoDiscapacitado', ''),
        item.get('fechaHoraPublicacion', ''),
        item.get('tipoTrabajo', ''),
        item.get('idArea', ''),
        item.get('localizacion', ''),
        item.get('cantidadVacantes', ''),
        item.get('promedioEmpresa', ''),
        item.get('modalidadTrabajo', ''),
        item.get('tipoAviso', '')
    ]
    rows.append(row)

# Escribe los datos en un archivo CSV
with open('multitrabajosV2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(rows)

print("Archivo CSV creado exitosamente.")

# Lee el archivo JSON con la codificación correcta
with open('area.txt', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extrae la lista de facets
facets = data.get('facets', [])

# Define los nombres de las cabeceras
headers = ["id", "idSemantico", "name"]

# Crea una lista de filas para el CSV
rows = []
for facet in facets:
    # Reemplaza comas por puntos en el campo 'name'
    name = facet.get('name', '').replace(',', '.')

    row = [
        facet.get('id', ''),
        facet.get('idSemantico', ''),
        name
    ]
    rows.append(row)

# Escribe los datos en un archivo CSV
with open('areasV1.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(rows)

print("Archivo CSV creado exitosamente.")

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
