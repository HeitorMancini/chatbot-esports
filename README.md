# FuriaBot – Chatbot para fãs da FURIA

## 1. Descrição

O FuriaBot é um chatbot desenvolvido para interagir com fãs do time de CS:GO da FURIA, respondendo perguntas sobre jogadores, partidas, estatísticas e curiosidades. Ele foi construído com Python, Flask e a API do Gemini, e pode ser acessado via uma interface web simples.

### 1.1 Funcionalidades

- Responde perguntas diversas sobre a FURIA
- Fornece resultados de partidas recentes
- Suporte a conversação natural baseada no contexto da FURIA (usando Gemini API)

## 2. Tecnologias usadas

- Python
- Flask
- Gemini API
- HTML/CSS/JS (Página web)
- Render (deploy)

## 3. Deploy

O FuriaBot está hospedado na plataforma Render, que oferece deploy automático de aplicações web diretamente a partir de um repositório GitHub.
### Acesso à aplicação
A aplicação pode ser acessada usando o seguinte link:
[furiabot.hesm.net](https://furiabot.hesm.net/)

### 3.1 Como foi feito o deploy

1. Foi criado um serviço web na plataforma [Render](https://render.com/)
2. O repositório do projeto foi vinculado à plataforma
3. As configurações usadas foram:
  - Build command: </br> ``` pip install -r requirements.txt ```
  - Start command: </br> ``` python app.py ```
  - Environment: </br> Python 3.11 (ou a versão utilizada no seu projeto)
  - Branch: </br> `main` (ou a branch principal do seu repositório)

### 3.2 Configurando variáveis de ambiente

A variável API_KEY deve ser configurada pelo painel da Render
- `GEMINI_API_KEY`: "sua chave da API" 

Por questões de segurança, a API_KEY não deve ser incluída no repositório
    
## 4. Autor
Heitor Souza Mancini
