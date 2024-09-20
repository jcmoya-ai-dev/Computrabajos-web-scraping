from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
import csv
import math
from datetime import datetime
UBCIACION = ['pichincha', 'pastaza', 'napo', 'morona-santiago', 'carchi', 'sucumbios', 'esmeraldas', 'canar',
             'cotopaxi', 'loja', 'chimborazo', 'santa-elena', 'los-rios', 'imbabura', 'tungurahua',
             'santo-domingo-de-los-tsachilas', 'el-oro', 'manabi', 'azuay', 'guayas' ]
# Function to calculate number page
def get_total_page(total_offers, paginated):
    return math.ceil(total_offers/paginated)

# Function to extract job offer identifier and request details
def get_offer_details( offer_id):
    # Construct the URL
    url = f"https://oferta.computrabajo.com/offer/{offer_id}/d/j?ipo=6&iapo=1"

    # Send GET request
    response = requests.get(url)

    if response.status_code == 200:
        # Print the JSON response
        json_response = response.json()
        #print("Job Offer Details:", json_response)
        return json_response
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

# Function to extract information from a page
def extract_information(driver):
    # Extract job offers information
    try:
        offers = driver.execute_script("return window.collectorData.oin;")
        #print("Offers List Oin:", offers)
        return offers
    except Exception as e:
        print("Error extracting information:", e)

def clean_text(text):
    """
    Clean and format text by replacing commas with periods and newlines with tabs.
    Handles non-string values by converting them to strings.
    """
    if text is None:
        return ''
    if isinstance(text, bool):
        return str(text)  # Convert boolean to string
    text = str(text)  # Ensure the value is a string
    text = text.replace(',', '.')  # Replace commas with periods
    text = text.replace('\r\n', '\t')  # Replace newlines with tabs
    text = text.replace('\n', ' ')  # Replace newlines with tabs
    return text

def convert_to_csv(data, filename):
    fieldnames = [
        'id','origen', 'cambioResidencia', 'viajar', 'empresa', 'paisEmpresa', 'ciudad', 'provincia', 'pais', 'areaName',
        'fechaHoraPublicacion', 'fechaHoraVence', 'experienciaAnos', 'skills', 'idiomas', 'descripcion', 'tipoTrabajo',
        'tipoContrato', 'salarioDescripcion', 'salario', 'titulo', 'descripcionTitulo', 'categoria', 'edadMaxima',
        'edadMinima', 'educacionMinima', 'cantidadVacante', 'modalidadTrabajo', 'empresaVerificada', 'anuncioRelevante',
        'aptoDiscapacitado', 'promedioEmpresa'
    ]

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for offer in data:
            try:
                # Ensure 'o' and 'c' are not None
                o_data = offer.get('o', {}) or {}
                c_data = offer.get('c', {}) or {}

                # Validate paisEmpresa (if it's None or empty, set to 'Ecuador')
                paisEmpresa = clean_text(c_data.get('c', ''))
                if not paisEmpresa or paisEmpresa == ' ':
                    paisEmpresa = 'Ecuador'

                # Validate fechaHoraPublicacion
                fechaHoraPublicacion = clean_text(o_data.get('pt', ''))
                dlu = clean_text(o_data.get('dlu', ''))

                # Convert to datetime to compare
                try:
                    fechaHoraPublicacion_dt = datetime.strptime(fechaHoraPublicacion, '%Y-%m-%dT%H:%M:%S')
                    dlu_dt = datetime.strptime(dlu, '%Y-%m-%dT%H:%M:%S')

                    if fechaHoraPublicacion_dt < dlu_dt:
                        fechaHoraPublicacion = dlu
                except Exception:
                    fechaHoraPublicacion = dlu

                # Validate fechaHoraVence
                fechaHoraVence = clean_text(o_data.get('st', ''))
                try:
                    fechaHoraVence_dt = datetime.strptime(fechaHoraVence, '%Y-%m-%dT%H:%M:%S')
                    if fechaHoraVence_dt < dlu_dt:
                        fechaHoraVence = dlu
                except Exception:
                    fechaHoraVence = dlu

                cleaned_offer = {
                    'id': clean_text(o_data.get('eoi', '')),
                    'origen': 'computrabajo',
                    'cambioResidencia': clean_text(o_data.get('acr', '')),
                    'viajar': clean_text(o_data.get('at', '')),
                    'empresa': clean_text(c_data.get('cn', '')),
                    'paisEmpresa': paisEmpresa,
                    'ciudad': clean_text(o_data.get('c', '')),
                    'provincia': clean_text(o_data.get('l', '')),
                    'pais': 'Ecuador',
                    'areaName': clean_text(o_data.get('cat', '')),
                    'fechaHoraPublicacion': fechaHoraPublicacion,
                    'fechaHoraVence': fechaHoraVence,
                    'experienciaAnos': clean_text(o_data.get('ey', '')),
                    'skills': clean_text(o_data.get('k', '')),
                    'idiomas': clean_text(o_data.get('la', '')),
                    'descripcion': clean_text(o_data.get('ld', '')),
                    'tipoTrabajo': clean_text(o_data.get('lset', '')),
                    'tipoContrato': clean_text(o_data.get('lsj', '')),
                    'salarioDescripcion': clean_text(o_data.get('lss', '')),
                    'salario': clean_text(o_data.get('s', '')),
                    'titulo': clean_text(o_data.get('ltr', '')),
                    'descripcionTitulo': clean_text(o_data.get('lc', '')),
                    'categoria': clean_text(o_data.get('cat', '')),
                    'edadMaxima': clean_text(o_data.get('maxa', '')),
                    'edadMinima': clean_text(o_data.get('mina', '')),
                    'educacionMinima': clean_text(o_data.get('me', '')),
                    'cantidadVacante': clean_text(o_data.get('v', '')),
                    'modalidadTrabajo': 'Presencial' if o_data.get('iwt') == 1 else 'Híbrido' if o_data.get(
                        'iwt') == 3 else 'Remoto' if o_data.get('iwt') ==2 else '',
                    'empresaVerificada': clean_text(o_data.get('icv', '')),
                    'anuncioRelevante': clean_text(o_data.get('ihc', '')),
                    'aptoDiscapacitado': clean_text(o_data.get('dy', '')),
                    'promedioEmpresa': clean_text(c_data.get('ad', ''))
                }
                # Ensure no extra keys are present in cleaned_offer
                cleaned_offer = {key: cleaned_offer.get(key, '') for key in fieldnames}
                writer.writerow(cleaned_offer)
            except Exception as e:
                print(f"Error processing offer: {offer}")
                print(f"Error message: {e}")

total_offers_detailed = []
for ubicacion in UBCIACION:

    # Set up Chrome options with User-Agent
    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument("--headless")  # Run in headless mode for testing

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Start from the first page
    page_number = 1
    offers_list = []
    offers_list_detailed = []
    total_offers = 0
    num_offer = 1
    paginated = 20

    # Extract total number of offers
    try:
        driver.get(f"https://ec.computrabajo.com/empleos-en-{ubicacion}?p={page_number}")
        total_offers = driver.find_element(By.XPATH, "//h1[@class='title_page']/span").text
        print("Total Offers:", total_offers)
    except Exception as e:
        print("Error extracting total offers:", e)

    total_page = get_total_page(int(total_offers), paginated)

    while True:
        print(f"Scraping page {page_number}...")
        driver.get(f"https://ec.computrabajo.com/empleos-en-{ubicacion}?p={page_number}")

        # Extract information from the current page
        offers = extract_information(driver)
        for offer in offers:
            offer_to_detail = offer['oi']
            offer_detailed = get_offer_details(offer_to_detail)
            offers_list_detailed.append(offer_detailed)
            total_offers_detailed.append(offer_detailed)
            print(f'Offer: {num_offer} de {total_offers}: ', offer_detailed)
            num_offer = num_offer + 1

        # Check if there is a next page
        try:
            if (page_number == total_page):
                next_button = None
            else:
                next_button = driver.find_element(By.XPATH, "//span[@title='Siguiente' and not(@class='disabled')]")
            if next_button:
                # Go to the next page
                next_page_url = next_button.get_attribute("data-path")
                page_number += 1
                driver.get(next_page_url)
                time.sleep(1)  # Wait for the page to load
            else:
                print("No more pages to scrape.")
                break
        except Exception as e:
            print("Error navigating to the next page:", e)
            break

    convert_to_csv(offers_list_detailed, f'ComputrabajoCSVV2\computrabajo_{ubicacion}V2.csv')
    driver.quit()

convert_to_csv(total_offers_detailed, f'computrabajoAllV2.csv')

