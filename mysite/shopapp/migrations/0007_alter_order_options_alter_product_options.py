# Generated by Django 5.0.6 on 2024-07-11 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_product_created_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]
