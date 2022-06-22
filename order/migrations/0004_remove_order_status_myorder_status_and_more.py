# Generated by Django 4.0.4 on 2022-06-19 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_payment_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='myorder',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered'), ('shipped', 'shipped'), ('out_for_delivery', 'out_for_delivery'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='ordered', max_length=150),
        ),
        migrations.AlterField(
            model_name='myorder',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
