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

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run():
    chrome_options = Options()

    # Evitar detecção de automação
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=pt-BR")
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")    
    chrome_options.add_argument("--window-size=1920,1080")

    # Definir user-agent
    user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.64 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)  # Tempo de espera explícito

    try:
        driver.get("https://www.mercadolivre.com.br")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
        search_box.send_keys("Computador Gamer i7 16gb ssd 1tb")
        search_box.submit()

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ui-search-layout__item')))
        products = driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, '.poly-component__title').text.strip()
                
                price_str = product.find_element(By.CSS_SELECTOR, '.poly-price__current .andes-money-amount__fraction').text
                price = float(price_str.replace('R$', '').replace('\n', '').replace('.', '').replace(',', '.'))
                
                link = product.find_element(By.CSS_SELECTOR, '.poly-component__title').get_attribute('href')

                # Extrair a imagem do produto
                image = None
                try:
                    image_element = product.find_element(By.CSS_SELECTOR, 'img.poly-component__picture')
                    image = image_element.get_attribute('data-src') or image_element.get_attribute('src')
                    
                    # Ignorar placeholders
                    if image and (image.startswith('data:image') or 'placeholder' in image):
                        image = None
                except NoSuchElementException:
                    logger.warning(f"Imagem não encontrada para o produto: {name}")
                except Exception as e:
                    logger.error(f"Erro ao processar imagem: {e}")
                
                installment = product.find_element(By.CSS_SELECTOR, '.poly-price__installments').text.strip()
                
                try:
                    delivery_type_element = product.find_element(By.CSS_SELECTOR, '.poly-component__shipping')
                    delivery_type = delivery_type_element.text.strip()
                    free_shipping = 'grátis' in delivery_type.lower()
                except:
                    delivery_type = None
                    free_shipping = False
                
                try:
                    original_price_element = product.find_element(By.CSS_SELECTOR, '.andes-money-amount--previous')
                    price_without_discount = float(original_price_element.text.replace('R$', '').replace('\n', '').replace('.', '').replace(',', '.'))
                except:
                    price_without_discount = None
                
                try:
                    discount_element = product.find_element(By.CSS_SELECTOR, '.andes-money-amount__discount')
                    discount_percentage = float(discount_element.text.replace('% OFF', '').strip())
                except:
                    discount_percentage = None
                
                Product.objects.update_or_create(
                    link=link,
                    defaults={
                        'image': image,
                        'name': name,
                        'price': price,
                        'installment': installment,
                        'price_without_discount': price_without_discount,
                        'discount_percentage': discount_percentage,
                        'delivery_type': delivery_type,
                        'free_shipping': free_shipping
                    }
                )

                logger.info(f"Produto salvo: {name} - R${price}")
            except NoSuchElementException as e:
                logger.error(f"Elemento não encontrado: {e}")
            except TimeoutException as e:
                logger.error(f"Timeout ao carregar elemento: {e}")
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")

    except Exception as e:
        logger.error(f"Erro geral no scraping: {e}")
    finally:
        driver.quit()
