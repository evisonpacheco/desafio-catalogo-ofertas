from decimal import Decimal
from ofertas.models import Product
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import random

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='scraper.log',
    filemode='a',
    )
logger = logging.getLogger(__name__)

# Constantes
BASE_URL = "https://www.mercadolivre.com.br"
SEARCH_QUERY = "Computador Gamer i7 16gb ssd 1tb"
WAIT_TIMEOUT = 10
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
]

def setup_driver():
    # Configura e retorna uma instância do WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=pt-BR")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    user_agent = get_random_user_agent()

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    logger.info(f"User Agent definido para: {user_agent}")

    return driver

def get_random_user_agent():
    # Aplica um user-agent aleatório
    return random.choice(USER_AGENTS)

def extract_product_data(product):
    # Extrai os dados de um produto
    try:
        name = product.find_element(By.CSS_SELECTOR, '.poly-component__title').text.strip()
        price_str = product.find_element(By.CSS_SELECTOR, '.poly-price__current .andes-money-amount__fraction').text
        price = Decimal(price_str.replace('R$', '').replace('\n', '').replace('.', '').replace(',', '.'))
        link = product.find_element(By.CSS_SELECTOR, '.poly-component__title').get_attribute('href')

        # Extrai a imagem do produto
        image = None
        try:
            image_element = product.find_element(By.CSS_SELECTOR, 'img.poly-component__picture')
            image = image_element.get_attribute('data-src') or image_element.get_attribute('src')
            if image and (image.startswith('data:image') or 'placeholder' in image):
                image = None
        except NoSuchElementException:
            logger.warning(f"Imagem não encontrada para o produto: {name}")
        except Exception as e:
            logger.error(f"Erro ao processar imagem: {e}")

        installment = product.find_element(By.CSS_SELECTOR, '.poly-price__installments').text.strip()

        try:
            delivery_type = 'Normal' 
            if product.find_elements(By.CSS_SELECTOR, '.poly-component__shipped-from'): 
                delivery_type = 'Full'
            free_shipping = bool(product.find_elements(By.CSS_SELECTOR, '.poly-component__shipping'))
        except NoSuchElementException:
            delivery_type = 'Normal'
            free_shipping = False
            print("Elemento não encontrado, tratando com valores padrão")

        try:
            original_price_element = product.find_element(By.CSS_SELECTOR, '.andes-money-amount--previous')
            price_without_discount = Decimal(original_price_element.text.replace('R$', '').replace('\n', '').replace('.', '').replace(',', '.'))
        except NoSuchElementException:
            price_without_discount = None

        try:
            discount_element = product.find_element(By.CSS_SELECTOR, '.andes-money-amount__discount')
            discount_percentage = Decimal(discount_element.text.replace('% OFF', '').strip())
        except NoSuchElementException:
            discount_percentage = 0

        return {
            'name': name,
            'price': price,
            'link': link,
            'image': image,
            'installment': installment,
            'delivery_type': delivery_type,
            'free_shipping': free_shipping,
            'price_without_discount': price_without_discount,
            'discount_percentage': discount_percentage
        }

    except NoSuchElementException as e:
        logger.error(f"Elemento não encontrado: {e}")
    except Exception as e:
        logger.error(f"Erro ao extrair dados do produto: {e}")
    return None

def save_product_data(product_data):
    # Salva ou atualiza os dados do produto no banco de dados.
    if product_data:
        image_url = product_data['image'].strip()
        
        # Atualiza ou cria o produto com base no link
        product, created = Product.objects.update_or_create(
            image=image_url,
            defaults={
                'link': product_data['link'],
                'name': product_data['name'],
                'price': product_data['price'],
                'installment': product_data['installment'],
                'price_without_discount': product_data.get('price_without_discount'), 
                'discount_percentage': product_data.get('discount_percentage'), 
                'delivery_type': product_data['delivery_type'],
                'free_shipping': product_data['free_shipping']
            }
        )

        if created:
            logger.info(f"Produto criado: {product_data['name']} - R${product_data['price']}")
        else:
            logger.info(f"Produto atualizado: {product_data['name']} - R${product_data['price']}")

def run():
    # Função principal para executar o scraping
    driver = setup_driver()
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    try:
        driver.get(BASE_URL)
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
        search_box.send_keys(SEARCH_QUERY)
        search_box.submit()

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ui-search-layout__item')))
        products = driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')

        for product in products:
            product_data = extract_product_data(product)
            if product_data:
                save_product_data(product_data)

    except TimeoutException as e:
        logger.error(f"Timeout ao carregar a página ou elementos: {e}")
    except Exception as e:
        logger.error(f"Erro geral no scraping: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run()