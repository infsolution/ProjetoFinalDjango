# Generated by Django 2.1.4 on 2019-02-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20190209_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reaction',
            name='reaction',
            field=models.CharField(choices=[('fa fa-heart', 'Gostei'), ('fa fa-rocket', 'Vamos'), ('fa fa-frown-o', 'Horrivel'), ('<fa fa-check-circle', 'Quero'), ('fa fa-star', 'Legal'), ('fa fa-map-marker', 'Vou'), ('fa fa-glass', 'Bom'), ('<fa fa-handshake-o', 'Otimo'), ('fa fa-trash-o', 'Nao')], default='fa fa-heart', max_length=30),
        ),
    ]