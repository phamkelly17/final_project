# Generated by Django 3.2 on 2021-06-16 00:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_alter_cart_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order_completed', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(blank=True, default=None, to='website.CartEntry')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
