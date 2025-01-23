from django import forms
from .models import pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = pedido
        fields = [
            "produto",
            "numeroPedido",
            "valorTotal",
            "status",
            "entregador",
            "cliente",
        ]  # Adicione os campos que você deseja no formulário
        widgets = {
            "entregador": forms.Select(
                attrs={"class": "form-select"}
            ),  # Classe Bootstrap para estilizar
            "produto": forms.Select(attrs={"class": "form-select"}),
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "numeroPedido": forms.TextInput(attrs={"class": "form-control"}),
            "valorTotal": forms.TextInput(attrs={"class": "form-control"}),
        }
