from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from dotenv import load_dotenv
import os
from groq import Groq
from llama_index.llms.groq import Groq


# def teste():
#     import os
#     from groq import Groq

#     client = Groq(
#         api_key=os.environ.get("GROQ_API_KEY"),
#     )

#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Explain the importance of fast language models",
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )

#     print(chat_completion.choices[0].message.content)


def ask_groq(message):
    #Carrega chave
    load_dotenv()

    # Create the Groq client
    GROQ_API = os.environ.get("GROQ_API_KEY")

    llm = Groq(model='llama3-70b-8192', api_key=GROQ_API)

    #response = llm.complete('Qual é a substância que dá o aroma do alecrim?')
    response = llm.complete('Qual a diferença entre llamaindex, llama e groq')
    return response


# def ask_openai(message):
#     response = openai.ChatCompletion.create(
#         model = "gpt-4",
#         messages=[
#             {"role": "system", "content": "You are an helpful assistant."},
#             {"role": "user", "content": message},
#         ]
#     )
    
#     answer = response.choices[0].message.content.strip()
#     return answer


# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_groq(message)

        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


# def chatbot (request):
#     if request.method == 'POST':
#         message = request.POST.get ('message')
#         response = 'Hi this is my response'
#         return JsonResponse({'message': message, 'response': response})
#     return render (request, "chatbot.html")



