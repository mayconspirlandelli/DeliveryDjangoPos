from django.db import models


#Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome do Cliente')
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Telefone do Cliente')  # Telefone (opcional)
    endereco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Endereco do Cliente')
    quantidadePedidos = models.CharField(max_length=50, null=False, blank=True, verbose_name='Quantidade de Pedidos do Cliente') #Zero se o cliente for novamente. Acima de Um o cliente já é de casa.

    def __str__(self):
        return self.nome  # Representação legível do cliente
    
    class Meta:
        ordering = ['nome']

#Registra o entregador do pedido
class Entregador(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome do Cliente')
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone (opcional)
    horarioChegada = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='Horário de Chegada do Entregador')  # Horário e data de chegada do entregado no restaurante.

    def __str__(self):
        return self.nome  # Representação legível do cliente
    
    class Meta:
        ordering = ['nome']


#Registra a lista de produtos pertencentes ao pedido
class Produto(models.Model):
    nome = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome do Produto')
    quantidadeProduto = models.IntegerField(default=0, blank=False, verbose_name='Quantidade')  # Valor total em reais
    precoUnitario = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name='Preço Unitário')  # Valor total em reais

    def __str__(self):
        return self.nome  # Representação legível do cliente
    
    class Meta:
        ordering = ['nome']


# Pedidos
class pedido(models.Model):

    # Definição das opções de status do pedido
    STATUS_CHOICES = [
        ('ACE', 'Em Aceitação'),
        ('PRE', 'Em Preparo'),
        ('PRT', 'Pronto'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregue'),
        ('CAN', 'Cancelado'),
    ]
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)  # Chave estrangeira do Produto
    entregador = models.ForeignKey(Entregador, on_delete=models.CASCADE, default=1)  # Chave estrangeira do Entregador
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)  # Chave estrangeira do cliente
    numeroPedido = models.CharField(max_length=50, null=False, blank=False, verbose_name='Número do Pedido')
    horarioDataPedido = models.DateTimeField(auto_now_add=True,  null=False, blank=False, verbose_name='Horário do Pedido')  # Horário e data do pedido
    #Calculado dinamicamente. Ajustar isso no futuro.
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2,null=False, blank=False, verbose_name='Valor total')  # Valor total em reais
    status = models.CharField(
        max_length=3,  # Tamanho máximo da string baseado nos códigos (e.g., "ACE", "PRE")
        choices=STATUS_CHOICES,  # Lista de opções
        default='ACE',  # Valor padrão
        )
  
    def __str__(self):
        return self.numeroPedido
    class Meta:
        ordering = ['horarioDataPedido']



