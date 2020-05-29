# Generated by Django 3.0.5 on 2020-05-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdescription',
            name='photo_order',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='information',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_img_url',
            field=models.URLField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='sales_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sales_price_comment',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_img_url',
            field=models.URLField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_price_comment',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
