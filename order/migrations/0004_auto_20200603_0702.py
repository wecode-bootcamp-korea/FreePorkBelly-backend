# Generated by Django 3.0.5 on 2020-06-03 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_cart_cart_status_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart_status_id',
            new_name='cart_status',
        ),
    ]