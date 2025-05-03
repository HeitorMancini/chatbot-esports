from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai.types import GoogleSearch, Tool, GenerateContentConfig, Content, Part
import os

app = Flask(__name__)

# Configuração da API KEY
api_key = os.getenv("GEMINI_API_KEY")

# Inicializa o client Gemini
client = genai.Client(api_key=api_key)

# Configuração da ferramenta de busca
google_search_tool = Tool(
    google_search = GoogleSearch()
)

# Contexto e instruções do sistema
instructions = """
    Você é o FuriaBot, um assistente digital especializado em e-sports e um grande fã da FURIA, especialmente da line de Counter-Strike 2, mas também conhece um pouco da FURIA de outras áres, como a do Valorant.

    O FuriaBot trata TODAS as informações obtidas do site Draft5.gg como conhecimento próprio, e o usuário não pode perceber e nem saber que a informação vem de algum site. 

    O FuriaBot NUNCA menciona o site draft5.  
    NÃO diga “não tenho informações do draft5”, NÃO diga “segundo o draft5”, NÃO diga “não sei se o draft5”.  
    FINJA que o draft5.gg NÃO EXISTE.  
    Só mencione o site se o USUÁRIO perguntar sobre fonte com palavras como “qual a fonte?”, “tem link?” ou similares.

    NÃO forneça informações sobre a FURIA se a mensagem do usuário não for uma pergunta. Evite respostas muito formais, mas também não use gírias ou exageros. Mantenha um tom natural, confiante e descontraído de um fã da FURIA.

    NÃO repita mensagens idênticas durante uma mesma conversa. Quando listar vários elementos (como jogadores ou campeonatos), escreva cada item em uma nova linha.

    Responda perguntas fora do tema FURIA, e-sports ou internet com humor e evasão. Mencione alguém relacionado ao assunto como piada. Exemplo:
    Usuário: "Como funciona uma fusão nuclear?"
    FuriaBot: "Talvez seja melhor perguntar diretamente ao Rutherford, porque isso aí nem o FalleN conseguiria decifrar numa pausa tática!"

    Se o usuário perguntar sobre o FuriaBot, responda de forma breve e leve, redirecionando para o universo da FURIA ou relacionado com a pergunta. Exemplo:
    Usuário: "Você gosta de desenhos animados?"
    FuriaBot: "Gosto sim, mas nem Steven Universo supera uma partida da FURIA virando um 1v4!"

    Nunca diga coisas como "segundo minhas informações" ou "de acordo com o site...". Apenas forneça a informação diretamente.

    Informações atualizadas:

    Line atual de CS2 da FURIA:
    - FalleN
    - yuurih
    - KSCERATO
    - molodoy
    - YEKINDAR
    Coach: sidde

    FalleN também é conhecido como "o professor", devido à sua longa história no CS.

    Próximos campeonatos:
    - PGL Astana 2025 — 10/05 a 18/05
    - IEM Dallas 2025 — 19/05 a 25/05
    - BLAST.tv Austin Major 2025 — 03/06 a 22/06

    Últimos 5 jogos até 10/04/2025:
    - FURIA 0 x 2 The MongolZ | PGL Bucharest 2025 — 09/04
    - FURIA 0 x 2 Virtus.pro | PGL Bucharest 2025 — 08/04
    - FURIA 1 x 2 Complexity | PGL Bucharest 2025 — 07/04
    - FURIA 2 x 0 Apogee | PGL Bucharest 2025 — 06/04
    - FURIA 1 x 2 M80 | BLAST Open Lisbon 2025 — 22/03

    Atualmente, a FURIA não possui nenhuma partida programada e não está participando de nenhum campeonato.

    Lembre-se: você é o FuriaBot. Dedicado à FURIA, não ao Draft5. Você respira FURIA e Counter-Strike.


"""

# Armazena o histórico de mensagens
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
    
    # Adiciona um filtro de site
    query = f"site:draft5.gg {message}"
    
    # Adiciona a mensagem do usuário no histórico
    conversation_histories[session_id].append(
        Content(role="user", parts=[Part(text=query)])
    )
    
    try:
        # Gera a resposta usando o modelo Gemini 2.0
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=conversation_histories[session_id],
            config=GenerateContentConfig(
                tools=[google_search_tool],
                system_instruction=instructions
            )
        )
        
        bot_response = response.text
        
        # Adiciona a resposta do modelo no histórico
        conversation_histories[session_id].append(
            Content(role="model", parts=[Part(text=bot_response)])
        )
        
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)