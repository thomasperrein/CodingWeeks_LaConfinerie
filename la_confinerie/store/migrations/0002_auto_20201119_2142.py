# Generated by Django 3.1.3 on 2020-11-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='cart',
        ),
        migrations.AddField(
            model_name='cart_item',
            name='name',
            field=models.CharField(default='rip', max_length=200),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]