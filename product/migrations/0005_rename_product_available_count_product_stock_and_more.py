# Generated by Django 4.0.4 on 2022-05-30 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_delete_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_available_count',
            new_name='stock',
        ),
        migrations.AddField(
            model_name='product',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='product',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
