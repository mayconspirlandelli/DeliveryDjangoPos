from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from dotenv import load_dotenv
import os
from groq import Groq
from gestor.models import Cliente, Produto, pedido



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
            max_completion_tokens=150,
        )

        # Extrai a resposta do assistente
        resposta_assistente = response.choices[0].message.content.strip()
        return resposta_assistente

    except Exception as e:
        # Log do erro (pode ser substituído por um logger)
        print(f"Erro ao se comunicar com o Groq: {e}")
        return "Ocorreu um erro ao processar sua solicitação."


def certo_chatbot(request):
    """
    Metodo responsavel por enviar e receber as perguntas e respontas do modelo LLM.
    """
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_groq(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')

def chatbot(request):
    """
    Metodo responsavel por enviar e receber as perguntas e respontas do modelo LLM.
    """
    if request.method == 'POST':
        message = request.POST.get('message')
        
        #pedido_chegou = pedido.objects.filter(status="ACE").first() # esse aqui deu certo.
        pedido_recente = pedido.objects.filter(status="ACE").order_by("-horarioDataPedido").first()
        numero_pedido=pedido_recente.numeroPedido
        cliente=pedido_recente.cliente.nome
        produtos=pedido_recente.produto.nome
        valor_total=pedido_recente.valorTotal
        resposta_chatbot = f"Pedido {numero_pedido} foi cadastrado. Cliente: {cliente}. Produtos: {produtos}. Total: R$ {valor_total:.2f}"
        
        #response = ask_groq(message)
        response = ask_groq(resposta_chatbot)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')
