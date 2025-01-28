from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from dotenv import load_dotenv
import os
from groq import Groq



def teste():
        # Create the Groq client
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )

        # Set the system prompt
        system_prompt = {
            "role": "system",
            "content":
            "You are a helpful assistant. You reply with very short answers."
        }

        # Initialize the chat history
        chat_history = [system_prompt]

        while True:
            # Get user input from the console
            user_input = input("You: ")

            # Append the user input to the chat history
            chat_history.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(model="llama3-70b-8192",
                                                        messages=chat_history,
                                                        max_tokens=100,
                                                        temperature=1.2)
            # Append the response to the chat history
            chat_history.append({
                "role": "assistant",
                "content": response.choices[0].message.content
            })
            # Print the response
            print("Assistant:", response.choices[0].message.content)



#Deu certo
def certo_ask_groq(message):
    #Carrega chave
    load_dotenv()

    # Create the Groq client
    GROQ_API = os.environ.get("GROQ_API_KEY")

    llm = Groq(model='llama3-70b-8192', api_key=GROQ_API)
    response = llm.complete(message)

    paragrafos = response.text.split("\n\n") #ASSIM funciona.
    for paragrafo in paragrafos:
        print(paragrafo)
        print()

    return paragrafos

def teste_ask_groq(mensagem_usuario):
    #Carrega chave
    load_dotenv()

    # Conecta com Groq via API
    GROQ_API = os.environ.get("GROQ_API_KEY")
    client = Groq(GROQ_API)
    
    # Configura o prompts do comportamento do assistente bot.
    system_prompt = {
        "role": "system",
        "content": "You are a helpful assistant. You reply with very short answers."
    }
    
    # Inicializa o histórico do chatbot
    chat_history = [system_prompt]
    
    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": mensagem_usuario})
  
    response = client.chat.completions.create(
        #messages=chat_history,
        messages=mensagem_usuario,
        model="llama3-70b-8192",
        temperature=0.7,
        max_completion_tokens=100,
        )
        
    # chat_history.append({
    #     "role": "assistant",
    #     "content": response.choices[0].message.content
    # })
    
    return response.text.split()


def ask_groq(mensagem_usuario):
    try:
        # Carrega a chave da API
        load_dotenv()
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise ValueError("Chave da API do Groq não encontrada no .env")

        # Conecta ao Groq
        client = Groq(api_key=GROQ_API_KEY,)

        # Configura o comportamento do chatbot
        system_prompt = {
            "role": "system",
            #"content": "You are a helpful assistant. You reply with very short answers."
            "content": "Você assume o papel de assistente virtual responsável por gerenciar os pedidos que chega na confeitaria de doces que você trabalha. Seu papel é auxiliar a chef de cozinha. Sua função é descrever os pedidos que chegarem via plataforma do ifood. Você deve ler a descrição do pedido para chef de cozinha informando os seguintes dados do pedido: Número do pedido, nome do cliente, informar quantos pedidos o cliente já fez ou se já é um cliente novato, nome do produtos e sua respectiva quantidade. "
        }

        # Inicializa o histórico de mensagens
        chat_history = [system_prompt]
        chat_history.append({"role": "user", "content": mensagem_usuario})

        # Faz a chamada à API
        response = client.chat.completions.create(
            messages=chat_history,
            model="llama3-8b-8192",
            temperature=0.7,
            max_completion_tokens=100,
        )

        # Extrai a resposta do assistente
        resposta_assistente = response.choices[0].message.content.strip()
        return resposta_assistente

    except Exception as e:
        # Log do erro (pode ser substituído por um logger)
        print(f"Erro ao se comunicar com o Groq: {e}")
        return "Ocorreu um erro ao processar sua solicitação."


def chatbot(request):
    """
    Metodo responsavel por enviar e receber as perguntas e respontas do modelo Llama.
    """
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_groq(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

