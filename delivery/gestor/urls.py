from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pedido", views.pedido, name="pedido"),
    path("historico_pedidos", views.historico_pedidos, name="historico_pedidos"),
    path("pedido_create/", views.pedido_create.as_view(), name="pedido_create"),
    path("pedido_list/", views.pedido_list.as_view(), name="pedido_list"),
    path("pedido_update/<int:pk>/", views.pedido_update.as_view(), name="pedido_update"),
    path("pedido_delete/<int:pk>/", views.pedido_delete.as_view(), name="pedido_delete"),
    path("pedido_detail/<int:pk>/", views.pedido_detail.as_view(), name="pedido_detail"),
    path(
        "entregador_create/",
        views.entregador_create.as_view(),
        name="entregador_create",
    ),
    path('ia_import', views.ia_import, name='ia_import'),
    path('ia_import_save', views.ia_import_save, name='ia_import_save'),
    path('ia_import_list', views.ia_import_list, name='ia_import_list'),
]
