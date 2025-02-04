from ofertas.models import Produto
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging



def run():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.mercadolivre.com.br")
    search_box = driver.find_element(By.NAME, "as_word")
    search_box.send_keys("Computador Gamer i7 16gb ssd 1tb")
    search_box.submit()

    time.sleep(5)

    # try:
    #     # Espera até que os produtos sejam carregados
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '.ui-search-layout__item'))
    #     )

    produtos = driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item')

    for produto in produtos:
        try:
            nome = produto.find_element(By.CSS_SELECTOR, '.poly-component__title').text
            preco = produto.find_element(By.CSS_SELECTOR, '.poly-price__current .andes-money-amount__fraction').text
            preco = preco.replace('R$', '').replace('\n', '').replace('.', '')
            preco = float(preco)
            link = produto.find_element(By.CSS_SELECTOR, '.poly-component__title').get_attribute('href')
            imagem = produto.find_element(By.CSS_SELECTOR, '.poly-component__picture').get_attribute('src')
            parcelamento = produto.find_element(By.CSS_SELECTOR, '.poly-price__installments').text
            tipo_entrega = produto.find_element(By.CSS_SELECTOR, '.poly-component__shipping').text
            frete_gratis = 'Frete grátis' in tipo_entrega

            try:
                preco_sem_desconto = produto.find_element(By.CSS_SELECTOR, '.andes-money-amount--previous').text
                preco_sem_desconto = preco.replace('R$', '').replace('\n', '').replace('.', '')
                preco_sem_desconto = float(preco)
                percentual_desconto = produto.find_element(By.CSS_SELECTOR, '.andes-money-amount__discount').text
            except:
                preco_sem_desconto = None
                percentual_desconto = None

            print(f"Nome: {len(nome)} caracteres")
            print(f"Parcelamento: {len(parcelamento)} caracteres")
            print(f"Tipo de Entrega: {len(tipo_entrega)} caracteres")
            print(f"Percentual de Desconto: {len(str(percentual_desconto))} caracteres")
            print(f"Link: {len(link)} caracteres")
            print(f"Imagem: {len(imagem)} caracteres")

            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.info(f"Nome: {nome}")
            logger.info(f"Parcelamento: {parcelamento}")
            logger.info(f"Tipo de Entrega: {tipo_entrega}")
            logger.info(f"Percentual de Desconto: {percentual_desconto}")
            logger.info(f"Link: {link}")
            logger.info(f"Imagem: {imagem}")

            Produto.objects.create(
                imagem=imagem,
                nome=nome,
                preco=preco,
                parcelamento=parcelamento,
                link=link,
                preco_sem_desconto=preco_sem_desconto,
                percentual_desconto=percentual_desconto,
                tipo_entrega=tipo_entrega,
                frete_gratis=frete_gratis
            )

        except Exception as e:
            print(f"Erro ao processar produto: {e}")

    driver.quit()