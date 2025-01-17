# Generated by Django 4.2.18 on 2025-01-17 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entregador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome do Cliente')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('horarioChegada', models.DateTimeField(auto_now_add=True, verbose_name='Horário de Chegada do Entregador')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Nome do Produto')),
                ('quantidadeProduto', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('precoUnitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço Unitário')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='endereco',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Endereco do Cliente'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='quantidadePedidos',
            field=models.CharField(blank=True, max_length=50, verbose_name='Quantidade de Pedidos do Cliente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefone do Cliente'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestor.cliente'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valorTotal',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor total'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='entregador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestor.entregador'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='produto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestor.produto'),
        ),
    ]
