# Generated by Django 5.1.5 on 2025-02-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofertas', '0004_alter_product_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='link',
            field=models.URLField(max_length=999, unique=True),
        ),
    ]
