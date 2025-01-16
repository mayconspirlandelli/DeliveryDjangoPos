from django.db import models

# Create your models here.
class pedido(models.Model):
    nomeCliente = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome do Cliente')
    numeroPedido = models.CharField(max_length=50, null=False, blank=False, verbose_name='Número do Pedido')
    
    def __str__(self):
        return self.nomeCliente
    class Meta:
        ordering = ['nomeCliente']