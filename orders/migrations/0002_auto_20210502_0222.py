# Generated by Django 3.2 on 2021-05-01 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_product_code'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orders',
            name='grand_total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
        migrations.CreateModel(
            name='AddItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
