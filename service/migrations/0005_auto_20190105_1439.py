# Generated by Django 2.1.4 on 2019-01-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_foaas_foaas_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foaas',
            name='box_2',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='foaas',
            name='box_3',
            field=models.TextField(blank=True),
        ),
    ]
