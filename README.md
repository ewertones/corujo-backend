### :us: Sorry, but this README was written in Portuguese! :us:

# Corujo API - https://api.corujo.com.br

## O que é isso?

https://corujo.com.br é um site de previsão de ativos da bolsa. Este repositório armazena o código back-end, tendo sito feito em Python com a utilização do framework FastAPI. Caso esteja procurando o front-end, ele pode ser acessado aqui: https://github.com/ewertones/corujo-frontend

## Como testá-lo localmente?

Como o repositório está dockerizado, é fortemente recomendado que utilize um sistema UNIX, como Mac ou Linux. O código foi escrito numa máquina rodando Ubuntu 22.04 LTS, Docker 20.10 e Python 3.10.

A seguir:

1. Abra o terminal onde deseja armazenar o projeto;
2. Clone o repositório:

```bash
git clone git@github.com:ewertones/corujo-backend.git
```

3. Entre na pasta criada:

```bash
cd corujo-backend
```

4. Crie um ambiente virtual:

```bash
python3 -m venv venv
```

5. Ative o ambiente virtual:

```bash
source venv/bin/activate
```

6. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

7. Crie a imagem no Docker:

```bash
docker build -t corujo-backend:Dockerfile .
```

8. Suba um contâiner com a imagem:

```bash
docker run \
-e PORT=8000 \
-e DB_HOST="localhost" \
-e DB_USERNAME="postgres" \
-e DB_DATABASE="postgres" \
-e DB_PASSWORD="postgres" \
-e FASTAPI_SECRET_KEY="qualquercoisa" \
-p 8000:8000 \
corujo-backend:Dockerfile
```

## Suporte

Caso não tenha conseguido acessar/clonar/rodar o projeto, mande um e-mail para admin@corujo.com.br relatando o problema.
