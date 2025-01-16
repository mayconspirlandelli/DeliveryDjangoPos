from django.contrib import admin
from .models import * 

class PedidoCustomizado(admin.ModelAdmin):
    list_display = ('numeroPedido', 'nomeCliente', )

admin.site.register(pedido, PedidoCustomizado)    