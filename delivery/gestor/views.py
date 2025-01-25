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
    paginate_by = 500  # Paginação, 10 itens por página (opcional)


#Atualiza o pedido
from django.views.generic.edit import UpdateView
class pedido_update(UpdateView):
    from .models import pedido
    model = pedido
    form_class = PedidoForm
    template_name = "gestor/pedido_form.html"  # Nome do template
    def get_success_url(self):
        return reverse_lazy("pedido_list")  # Redireciona após o sucesso

#Exclusao do Pedido
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .models import pedido
class pedido_delete(DeleteView):
    model = pedido 
    template_name = "gestor/pedido_delete.html"  # Template de confirmação
    success_url = reverse_lazy("pedido_list")  # Redireciona para a lista após a exclusão


# Visualizar o detalhe do pedido
from django.views.generic.detail import DetailView
class pedido_detail(DetailView):
    model = pedido
    template_name = "gestor/pedido_detail.html"
    context_object_name = "pedido"


# Criar Entregador.
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



# def ia_import(request):
#     return render(request, 'ia_import.html')

#Apagar todos os registros das tabelas
from .models import pedido, Entregador, Produto, Cliente
def limpar_banco():
    Entregador.objects.all().delete()
    Cliente.objects.all().delete()
    Produto.objects.all().delete()
    pedido.objects.all().delete()
    

import pandas as pd
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render, redirect
from .forms import UploadCSVForm
from .models import pedido, Entregador, Produto, Cliente
def importar_pedidos(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo_csv = form.cleaned_data["arquivo_csv"]
            try:
                limpar_banco()
                
                df = pd.read_csv(arquivo_csv)
                print(df)
                for _, row in df.iterrows():
        
        #data_pedido = datetime.strptime(row["data_pedido"], "%d/%m/%y").date()
                    entregadorObjeto = Entregador.objects.get_or_create(
                        nome=row["EntregadorNome"],
                        telefone=row["EntregadorTelefone"],
                        horarioChegada=datetime.strptime(row["EntregadorHoraChegada"], "%d/%m/%y").date()
                    )
                    #entregadorObjeto = Entregador.objects.filter(nome=row["EntregadorNome"])
                    entregadorObjeto = Entregador.objects.latest('id')
                    #entregadorObjeto, created_entregador = Entregador.objects.get_or_create(nome=row["EntregadorNome"])
                    
                    clienteObjeto = Cliente.objects.get_or_create(
                        nome=row["Cliente"],
                        telefone=row["ClienteTelefone"],
                        endereco=row["ClienteEndereco"],                        
                        quantidadePedidos=row["QtdePedidos"],                        
                    )
                    #clienteObjeto = Cliente.objects.filter(nome=row["Cliente"])
                    clienteObjeto = Cliente.objects.latest('id')
                    #clienteObjeto, created_cliente = Cliente.objects.get_or_create(nome=row["Cliente"])
                    
                    # Remover o "R$" e substituir a vírgula por ponto
                    # Substituir a vírgula por ponto e converter para Decimal
                    preco_str = row["PrecoUnitario"].replace("R$", "").replace(",", ".")
                    preco = Decimal(preco_str)
                    
                    produtoObjeto = Produto.objects.get_or_create(
                        nome=row["Produto"], 
                        quantidadeProduto=row["QtdeProduto"],
                        precoUnitario=preco,
                    )
                    #produtoObjeto = Produto.objects.filter(nome=row["Produto"])
                    produtoObjeto = Produto.objects.latest('id')
                    #produtoObjeto, created_produto = Produto.objects.get_or_create(nome=row["Produto"])
                    
                    # Substituir a vírgula por ponto e converter para Decimal
                    valor_str = row["ValorTotalPedido"].replace("R$", "").replace(",", ".")
                    valor_total = Decimal(valor_str)
                    
                    pedido.objects.create(
                        numeroPedido=row["NumeroPedido"],
                        #horarioDataPedido=row["DataPedido"],
                        horarioDataPedido=datetime.strptime(row["DataPedido"], "%d/%m/%y").date(),
                        valorTotal=valor_total,
                        status=row["StatusPedido"],
                        cliente=clienteObjeto,
                        produto=produtoObjeto,
                        entregador=entregadorObjeto,
                    )
                return redirect("pedido_list")  # Redirecionar para a lista de pedidos
            except Exception as e:
                return render(request, "importar_pedidos.html", {
                    "form": form,
                    "erro": f"Erro ao processar o arquivo: {e}",
                })
    else:
        form = UploadCSVForm()
    return render(request, "importar_pedidos.html", {"form": form})



# def ia_import_save(request):
#     from .models import dados
#     import os
#     from django.core.files.storage import FileSystemStorage
#     if request.method == 'POST' and request.FILES['arq_upload']:
#     fss = FileSystemStorage()
#     upload = request.FILES['arq_upload']
#     file1 = fss.save(upload.name, upload)
#     file_url = fss.url(file1)
#     from .models import dados
#     dados.objects.all().delete()
#     i = 0
#     file2 = open(file1,'r')
#     for row in file2:
#     if (i > 0):
#     row2 = row.replace(',', '.')
#     row3 = row2.split(';')
#     dados.objects.create(
#     grupo = row3[0], mdw = float(row3[1]), latw = float(row3[2]),
#     tmcw = float(row3[3]), racw = float(row3[4]), araw = float(row3[5]),
#     i = i + 1
#     file2.close()
#     os.remove(file_url.replace(