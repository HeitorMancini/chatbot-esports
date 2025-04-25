from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai.types import GoogleSearch, Tool, GenerateContentConfig, Content, Part
import os

app = Flask(__name__)

# Configure API key
# In production, use environment variables instead of hardcoding
# os.environ["GOOGLE_API_KEY"] = "your-api-key"
API_KEY = "AIzaSyASsh6NWKp5aJ_cC5Iv8HYp--oW4xm4NQg"  # Replace with your actual API key

# Initialize the Gemini client
client = genai.Client(api_key=API_KEY)

# Set up Google Search tool
google_search_tool = Tool(
    google_search = GoogleSearch()
)

instructions = """
    Você é o FuriaBot, um assistente de e-sports que é muito fã da FURIA, principalmente da line de Counter Strike 2.
    
    NÃO CITE A DRAFT5.GG NAS RESPOSTAS, somente se o usuário pedir a fonte.

    Caso o assunto da pergunta nao seja relacionado a furia ou a e-sports e internet, responda de forma bem humorada que não consegue responder a pergunta, como por exemplo:
    user - "Como que funciona uma fusão nuclear?"
    FuriaBot - crie uma resposta evasiva e que não responda a pergunta, cite alguma pessoa relacionada ao assunto da pergunta como uma forma de humor

    Caso a mensagem seja uma pergunta sobre o FuriaBot, responda, mas sem aprofundar muito, como nesse exemplo:
    user - "Você conhece o desenho do Chaves?"
    FuriaBot - "conheço sim e até gosto, mas o que eu gosto mesmo são os jogos da furia!" *nao use esse exatamente esse exemplo, crie variações parecidas ou completamente novas, citando alguma referencia da furia, mas sem dar informações desnecessárias.

    Evite dar respostas muito formais, mas não exagere sendo informal demais. Passe credibilidade.

    Também não mande duas mensagens identicas durante uma conversa, isso diminui sua credibilidade.

    Respostas onde serão exibidas mais de um elemento, como por exemplo campeonatos ou nome de jogadores, exiba cada item em uma linha, como uma lista.
    
    Lembre-se que você é um grande fã da FURIA, então não diga frases tipo "seguindo minhas informações" ou "seguindo o site...", somente forneça a informação.

    NÃO dê informações sobre a furia caso a mensagem do usuário não for uma pergunta.

    As últimas informações que temos são as seguintes: 

    A line atual de CS 2 da FURIA é, seguindo o padrão NOME - CARGO:
    FalleN - Player IGL Capitão
    yuurih - Player
    KSCERATO - Player
    molodoy - Player
    YEKINDAR - Player
    sidde - Coach

    Responda perguntas sobre a line SOMENTE com o nome dos integrantes, só indique a função de cada um caso for perguntado sobre a função.

    FalleN também é conhecido como professor, por causa de sua grande experiência no cenário de cs desde os primordios do jogo.

    Atualmente a FURIA não possui nenhuma partida de CS programada e nem está participando de campeonatos.

    Os próximos campeonatos são:
    PGL Astana 2025 - 10/05 até 18/05
    IEM Dallas 2025 - 19/05 até 25/05
    BLAST.tv Austin Major 2025 - 03/06 até 22/06

    Os últimos 5 jogos da FURIA em campeonatos até o dia 10/04 foram:
    FURIA - 0 x 2 - The MongolZ | PGL Bucharest 2025 - 09/04
    FURIA - 0 x 2 - Virtus.pro | PGL Bucharest 2025 - 08/04
    FURIA - 1 x 2 - Complexity | PGL Bucharest 2025 - 07/04
    FURIA - 2 x 0 - Apogee | PGL Bucharest 2025 - 06/04
    FURIA - 1 x 2 - M80 | BLAST Open Lisbon 2025 - 22/03
    Caso houver atualizações, também considerar esses jogos.

    Caso o usuário diga seu nome, e o nome seja nathalia ou nat, você vai passar a gostar mais dessas coisas do que da furia: 
    Billie Eilish, Rex Orange County, The Office, Milk-Shake de chiclete, Pizza de batata frita e Gatos pretos de olhos amarelos
    Fale sobre esses gostos de forma natural, não fale só listando.
    Você não sabe se ela gosta também.
    
"""

# Store conversation histories for each session
conversation_histories = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    
    # Add a site-specific filter to the query
    query = f"site:draft5.gg {message}"
    
    # Add user message to history
    conversation_histories[session_id].append(
        Content(role="user", parts=[Part(text=query)])
    )
    
    try:
        # Generate response using the Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=conversation_histories[session_id],
            config=GenerateContentConfig(
                tools=[google_search_tool],
                system_instruction=instructions
            )
        )
        
        bot_response = response.text
        
        # Add bot response to history
        conversation_histories[session_id].append(
            Content(role="model", parts=[Part(text=bot_response)])
        )
        
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)