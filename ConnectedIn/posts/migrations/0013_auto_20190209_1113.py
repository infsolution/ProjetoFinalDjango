# Generated by Django 2.1.4 on 2019-02-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_compartilhado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='reaction',
            field=models.CharField(choices=[('fa fa-heart', 'Gostei'), ('fa fa-alicorn', 'Vamos'), ('fa fa-heart-broken', 'Horrivel'), ('fa fa-french-fries', 'Quero'), ('fa fa-apple-alt', 'Legal'), ('fa fa-fish', 'Vou'), ('fa fa-cheeseburge', 'Bom'), ('fa fa-handshake', 'Otimo'), ('fa fa-skull-crossbones', 'Nao')], default='fa fa-heart', max_length=30),
        ),
    ]
