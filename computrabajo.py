from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import math

# Configura las opciones del navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Configura el servicio de ChromeDriver
service = Service(ChromeDriverManager().install())

# Inicializa el navegador
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accede a la página
driver.get('https://ec.computrabajo.com/empleos-en-pichincha')

# Verifica el título de la página para depuración
print("Page title is:", driver.title)

# Function to extract data from the page
def extract_data_oin():
    data = driver.execute_script("return window.collectorData.oin;")
    return data

# Function to extract total number of offers
def get_total_offers():
    try:
        # Find the element containing the total number of offers
        total_offers_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.title_page span.fwB'))
        )
        total_offers = int(total_offers_element.text)
        return total_offers
    except Exception as e:
        print(f"Error extracting total offers: {e}")
        return 0

# Function to navigate to the next page
def go_to_next_page():
    try:
        # Find the "Siguiente" button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@title="Siguiente"]'))
        )
        # Click the "Siguiente" button
        next_button.click()
    except Exception as e:
        print(f"Error navigating to the next page: {e}")

# Extract total number of offers
total_offers = get_total_offers()
print(f"Total number of offers: {total_offers}")

# Calculate the number of pages
items_per_page = 20
total_pages = math.ceil(total_offers / items_per_page)
print(f"Total number of pages: {total_pages}")

# Extract data from the first page
data = extract_data_oin()
print("Data from page 1:", json.dumps(data, indent=2))

# Loop through additional pages
for page_number in range(2, total_pages + 1):  # Start from page 2, as page 1 is already scraped
    go_to_next_page()
    # Wait for the page to load and extract data
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.page-content'))  # Adjust the selector if necessary
    )
    data = extract_data_oin()
    print(f"Data from page {page_number}:", json.dumps(data, indent=2))

# Close the driver
driver.quit()

print(data)



# Ejecuta JavaScript para obtener la lista `oin`
script = """
return window.collectorData.oin;
"""
oin_list = driver.execute_script(script)

# Imprime la lista `oin`
for item in oin_list:
    print(item)

# Cierra el navegador
driver.quit()
