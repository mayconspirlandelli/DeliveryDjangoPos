from django.shortcuts import render
from django.http import HttpResponse
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

# Nao estou usando esse metodo.
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


from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import pedido
from .forms import PedidoForm
class pedido_create(CreateView):
    model = pedido
    form_class = PedidoForm
    template_name = "gestor/pedido_form.html"  # Template que será renderizado
    def get_success_url(self):
        return reverse_lazy("pedido_list")  # Redireciona após o sucesso


from django.views.generic import ListView
class pedido_list(ListView):
    from .models import pedido
    model = pedido
    template_name = "gestor/pedido_list.html"  # Nome do template
    context_object_name = "pedidos"  # Nome do contexto passado ao template
    paginate_by = 20  # Paginação, 10 itens por página (opcional)
    


# Classe cadastra o pedido. NAO TESTEI AINDA
# from django.urls import reverse_lazy
# from django.views.generic.edit import CreateView
# class pedido_create(CreateView):
#     from .models import pedido

#     model = pedido
#     fields = [
#         "numeroPedido",
#         "horarioDataPedido",
#         "valorTotal",
#         "status",
#     ]
#     def get_success_url(self):
#         return reverse_lazy("historico_pedidos.html")


def salvarPedido(request):
    xnumeroPedido = request.POST.get("numeroPedido")
    xhorarioDataPedido = request.POST.get("horarioDataPedido")
    xvalorTotal = request.POST.get("valorTotal")
    xstatus = request.POST.get("status")
    print(xnumeroPedido)
    print(xhorarioDataPedido)
    print(xvalorTotal)
    print(xstatus)

    # from .models import pedido
    # pedido.objects.create(
    #     numeroPedido=xnumeroPedido,
    #     horarioDataPedido=xhorarioDataPedido,
    #     valorTotal=xvalorTotal,
    #     status=xstatus,
    # )
    return render(request, "historico_pedidos.html")


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
class entregador_create(CreateView):
    from .models import Entregador
    model = Entregador
    fields = [
        "nome",
        "telefone",
    ]
    def get_success_url(self):
        return reverse_lazy("entregador_form.html")
