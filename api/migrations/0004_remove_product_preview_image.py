# Generated by Django 5.0.1 on 2024-02-19 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_seller_product_owner_product_total_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='preview_image',
        ),
    ]
