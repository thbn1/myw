# Generated by Django 4.1.1 on 2023-08-10 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_remove_product_webapp_prod_product_e3fe25_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='product',
            name='webapp_prod_product_8c50f0_idx',
        ),
    ]
