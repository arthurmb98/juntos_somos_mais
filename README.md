# User Data API

## Descrição

API para carregar, transformar e consultar dados de usuários a partir de arquivos CSV e JSON.

## Endpoints

### `GET /api/health/`

Verifica se a aplicação está funcionando.

### `GET /api/load_data/`

Carrega e transforma dados dos arquivos CSV e JSON.

### `GET /api/users/`

Lista os usuários com paginação. Parâmetros:
- `pageNumber`: Número da página (default: 1)
- `pageSize`: Tamanho da página (default: 10)

## Instalação

1. Clone o repositório:
    ```bash
    git clone <repository-url>
    ```
2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Windows use: venv\Scripts\activate
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute as migrações e inicie o servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Requisitos

- Python 3.x
- Django
- djangorestframework
- requests
