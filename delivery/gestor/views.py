from django.shortcuts import render
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("EXEMPLO 01.")

from django.contrib.auth import authenticate, login, logout


def index(request):
    print("else")
    usuario = request.POST.get("username")
    senha = request.POST.get("password")
    user = authenticate(username=usuario, password=senha)
    if user is not None:
        login(request, user)
        request.session["username"] = usuario
        request.session["password"] = senha
        request.session["usernamefull"] = user.get_full_name()
        print(request.session["username"])
        print(request.session["password"])
        print(request.session["usernamefull"])
        from django.shortcuts import redirect

        return redirect("menu_alias")
    else:
        return render(request, "index.html")


def pedido(request):
    from .models import pedido

    pedidoResgistrado = pedido.objects.get(id=1)
    print("Número do pedido: ", pedidoResgistrado.numeroPedido)
    print("horário do pedido: ", pedidoResgistrado.horarioDataPedido)
    print("Nome do Cliente: ", pedidoResgistrado.cliente.nome)

    return render(request, "pedido.html", pedidoResgistrado)


def historico_pedidos(request):
    from .models import pedido

    dicionario = {}
    registros = pedido.objects.all()
    dicionario["pedidos"] = registros
    return render(request, "historico_pedidos.html", dicionario)
