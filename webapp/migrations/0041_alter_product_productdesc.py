# Generated by Django 4.1.1 on 2023-10-11 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0040_alter_product_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productdesc',
            field=models.JSONField(),
        ),
    ]
