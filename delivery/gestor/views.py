from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from decimal import Decimal
from datetime import datetime
from .forms import UploadCSVForm
from .models import pedido, Entregador, Produto, Cliente
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from .forms import PedidoForm



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

def limpar_banco():
    Entregador.objects.all().delete()
    Cliente.objects.all().delete()
    Produto.objects.all().delete()
    pedido.objects.all().delete()


def convertToDecimal(valor_texto):
    """
    Converte um texto formatado como valor monetário (e.g., 'R$19,56') para Decimal.
    
    Args:
        valor_texto (str): O texto contendo o valor a ser convertido.

    Returns:
        Decimal: O valor convertido em formato Decimal.
    """
    try:
        # Remove o símbolo "R$" e substitui a vírgula por ponto
        valor_texto = valor_texto.replace("R$", "").replace(",", ".").strip()
        return Decimal(valor_texto)
    except Exception as e:
        raise ValueError(f"Erro ao converter '{valor_texto}' para Decimal: {e}")                       
    
    
    from datetime import datetime

def convertToDate(data_texto):
    """
    Converte um texto de data no formato '%d/%m/%y' para um objeto `date`.

    Args:
        data_texto (str): O texto contendo a data no formato 'DD/MM/YY'.

    Returns:
        date: Um objeto de data correspondente ao texto fornecido.
    """
    try:
        # Converte o texto para um objeto datetime e extrai a data
        return datetime.strptime(data_texto, "%d/%m/%y").date()
    except Exception as e:
        raise ValueError(f"Erro ao converter '{data_texto}' para data: {e}")
    

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
                    entregadorObjeto = Entregador.objects.create(
                        nome=row["EntregadorNome"],
                        telefone=row["EntregadorTelefone"],
                        horarioChegada=datetime.strptime(row["EntregadorHoraChegada"], "%d/%m/%y").date()
                    )
                    clienteObjeto = Cliente.objects.create(
                        nome=row["Cliente"],
                        telefone=row["ClienteTelefone"],
                        endereco=row["ClienteEndereco"],                        
                        quantidadePedidos=row["QtdePedidos"],                        
                    )
                    
                    # Remover o "R$" e substituir a vírgula por ponto
                    # Substituir a vírgula por ponto e converter para Decimal
                    # preco_str = row["PrecoUnitario"].replace("R$", "").replace(",", ".")
                    # preco = Decimal(preco_str)
                    
                    produtoObjeto = Produto.objects.create(
                        nome=row["Produto"], 
                        quantidadeProduto=row["QtdeProduto"],
                        precoUnitario=convertToDecimal(row["PrecoUnitario"]),
                    )
                    
                    pedido.objects.create(
                        numeroPedido=row["NumeroPedido"],
                        #horarioDataPedido=datetime.strptime(row["DataPedido"], "%d/%m/%y").date(),
                        horarioDataPedido=convertToDate(row["DataPedido"]),
                        valorTotal=convertToDecimal(row["ValorTotalPedido"]),
                        status=row["StatusPedido"],
                        cliente=clienteObjeto,
                        produto=produtoObjeto,
                        entregador=entregadorObjeto,
                    )
                return redirect("pedido_list")  # Redirecionar para a lista de pedidos
            except Exception as e:
                print(e)
                return render(request, "importar_pedidos.html", {
                    "form": form,
                    "erro": f"Erro ao processar o arquivo: {e}",
                })
    else:
        form = UploadCSVForm()
    return render(request, "importar_pedidos.html", {"form": form})
