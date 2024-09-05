# User Data API

## Descrição

API para carregar, transformar e consultar dados de usuários a partir de arquivos CSV e JSON.

## Endpoints

### `GET /api/health/`

Verifica se a aplicação está funcionando.

### `GET /swagger/`

Swagger da aplicação.

### `GET /api/users/`

Lista os usuários com paginação. Parâmetros:
- `page`: Número da página (default: 1)
- `page_size`: Tamanho da página (default: 10)

### `GET /api/users_by_type/`

Lista os usuários filtrados por tipo com paginação. Parâmetros:
- `type`: Tipo de usuário (obrigatório)
- `page`: Número da página (default: 1)
- `page_size`: Tamanho da página (default: 10)

### `POST /api/users/create`

Cria novos usuários. O corpo da solicitação deve conter o link do arquivo JSON ou CSV.
- `body`: { "file_url": "https://url/file.json" } (obrigatório)

### `POST /api/populate_database/`

Popula o banco de dados a partir dos arquivos CSV e JSON estáticos.

### `POST /api/populate_csv/`

Popula o banco de dados a partir do arquivo CSV estático.

### `POST /api/populate_json/`

Popula o banco de dados a partir do arquivo JSON estático.

### `GET /api/purge_users/`

Expurga todos os dados de usuários.

## Instalação

1. Clone o repositório:
    ```bash
    git clone <repository-url>
    ```
2. Crie e ative um ambiente virtual com o nome `juntos_somos_mais_env`:
    ```bash
    python -m venv juntos_somos_mais_env
    source juntos_somos_mais_env/bin/activate  # Para Windows use: juntos_somos_mais_env\Scripts\activate
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
