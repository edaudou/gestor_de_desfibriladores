# Generated by Django 3.2 on 2022-03-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20220321_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='cif',
            field=models.CharField(max_length=9, verbose_name='cif'),
        ),
    ]
