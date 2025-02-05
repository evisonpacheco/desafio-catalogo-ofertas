# Web Scraper do Mercado Livre com Django e Selenium
Este projeto é um web scraper desenvolvido em Django e Selenium que coleta informações de produtos do Mercado Livre e as armazena em um banco de dados. Além disso, ele oferece uma interface web para visualizar e filtrar os produtos coletados.

## Funcionalidades Principais
- Scraping: Extrai detalhes como nome, preço, URL, imagem, tipo de entrega e frete grátis.

- Armazenamento: Salva os dados extraídos no scraping em um banco de dados PostgreSQL.

- Evita duplicidade: Caso o Script seja rodado mais de uma vez os produtos duplicados não serão armazenados, apenas atualizados; novos produtos serão salvos normalmente.

- Destaques: Exibe o produto com o maior desconto, o mais caro e o mais barato.

- Filtragem: Permite filtrar produtos por ```Entrega Grátis```, ```Entrega Full```, ```Menor Preço```, ```Maior Preço```, ```Maior Desconto```

- Logs: Uso de Logs para facilitar a depuração. São registrados em um arquivo de log (scraper.log).

- Interface Web: Permite visualizar os produtos coletados de forma organizada e filtrá-los.

## Estrutura
A estrutura do Projeto é a seguinte:

```
desafio-catalogo-ofertas
│   README.md 
└───catalogo_ofertas 
    │   manage.py
    │   requirements.txt #Requisitos do Projeto
    │
    ├───catalogo_ofertas
    │   │   settings.py # Configurações do Projeto
    │   │   urls.py # Determina as URLs do Projeto
    │
    └───ofertas
        │   models.py # Determina o modelo para armazenar os dados
        │   tests.py # Arquivo de Testes (Vazio)
        │   views.py # Determina as views do Projeto
        │
        ├───migrations # Migrações da Aplicação
        │   │   
        │
        ├───scripts
        │   │   scraper.py # Script para o Scraping
        │
        ├───templates
        │   └───ofertas
        │       │   products_list.html #Interface da página WEB
        │       └───static
        │           └───css
        │               styles.css # Estilização da Página WEB
        │
```

## Requisitos
- Django==5.1.5
- selenium==4.28.1
- webdriver-manager==4.0.2
- requests==2.32.3
- psycopg2-binary==2.9.10
- python-dotenv==1.0.1

## Configuração
1. Instale as dependências do projeto:

```
pip install -r requirements.txt
```
- Recomenda-se usar um ambiente virtual (venv) para isolar as dependências.

2. Configure o Banco de Dados
- Crie um banco de dados no PostgreSQL com o nome ```catalogo_ofertas```.

- Edite o arquivo ```catalogo_ofertas/settings.py``` e configure as credenciais do banco de dados na seção DATABASES.


3. Execute as Migrações
Aplique as migrações para criar as tabelas no banco de dados:

```
python manage.py makemigrations
python manage.py migrate
```

## Execução
1. Executar o Scraping.
Para coletar os dados dos produtos, execute o comando de scraping:

```
python manage.py runscript scraper
```
Nota: O scraper está configurado para buscar produtos relacionados a "Computador Gamer i7 16gb ssd 1tb".

2. Iniciar o Servidor de Desenvolvimento.
Inicie o servidor Django para acessar a interface web:

```
python manage.py runserver
```

3. Acesse a interface no navegador: http://127.0.0.1:8000/produtos.

## Interface Web
A interface web permite:

- Visualizar todos os produtos coletados.

- Filtrar produtos por frete grátis e entrega Full.

- Ver os destaques: maior desconto, maior preço e menor preço.

## Detalhes Técnicos

- Delays Aleatórios: Para evitar comportamentos suspeitos.

- Modo Headless: Executa o navegador em segundo plano.

- Erros são registrados em um arquivo de log (scraper.log) para facilitar a depuração.

- Termo de Busca: Para alterar o termo de busca, edite a constante SEARCH_QUERY no arquivo scraper.py.

- Filtros: Adicione novos filtros na interface web editando as views e templates.
