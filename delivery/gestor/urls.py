from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pedido", views.pedido, name="pedido"),
    path("historico_pedidos", views.historico_pedidos, name="historico_pedidos"),
    path("pedido_create/", views.pedido_create.as_view(), name="pedido_create"),
    path("pedido_list/", views.pedido_list.as_view(), name="pedido_list"),
    path(
        "entregador_create/",
        views.entregador_create.as_view(),
        name="entregador_create",
    ),
]
