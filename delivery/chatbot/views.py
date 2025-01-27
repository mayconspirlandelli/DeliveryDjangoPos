from django.shortcuts import render, redirect
from django.http import JsonResponse
# from .models import Chat
#import openai
from django.utils import timezone
from dotenv import load_dotenv
import os
from groq import Groq
from llama_index.llms.groq import Groq

def ask_groq(message):
    
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
# def chatbot(request):
#     chats = Chat.objects.filter(user=request.user)

#     if request.method == 'POST':
#         message = request.POST.get('message')
#         response = ask_openai(message)

#         chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
#         chat.save()
#         return JsonResponse({'message': message, 'response': response})
#     return render(request, 'chatbot.html', {'chats': chats})


def chatbot (request):
    if request.method == 'POST':
        message = request.POST.get ('message')
        response = 'Hi this is my response'
        return JsonResponse({'message': message, 'response': response})
    return render (request, "chatbot.html")



