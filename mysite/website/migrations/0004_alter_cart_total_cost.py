# Generated by Django 3.2 on 2021-06-13 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
