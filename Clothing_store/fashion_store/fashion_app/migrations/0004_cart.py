# Generated by Django 4.2.3 on 2024-01-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fashion_app', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fashion_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fashion_app.customer')),
            ],
        ),
    ]
