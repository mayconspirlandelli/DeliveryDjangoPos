from django.contrib import admin
from .models import * 

class PedidoCustomizado(admin.ModelAdmin):
    list_display = ('numeroPedido', )

admin.site.register(Pedido, PedidoCustomizado) 
admin.site.register(Cliente)
admin.site.register(Entregador)
admin.site.register(Produto)
