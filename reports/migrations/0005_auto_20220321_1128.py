# Generated by Django 3.2 on 2022-03-21 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_company_cif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.CharField(max_length=100, null=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Apellidos'),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.CharField(max_length=100, null=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='battery_expiration_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='brand',
            field=models.CharField(max_length=100, null=True, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='check_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='installation_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='location',
            field=models.CharField(max_length=255, null=True, verbose_name='Localización'),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='model',
            field=models.CharField(max_length=100, null=True, verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='defibrillator',
            name='professional',
            field=models.ManyToManyField(null=True, related_name='defibrillator', to='reports.Professional'),
        ),
        migrations.AlterField(
            model_name='patch',
            name='expiration_date',
            field=models.DateTimeField(null=True, verbose_name='Fecha de expiración'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='email',
            field=models.CharField(max_length=100, null=True, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='first_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='last_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Apellidos'),
        ),
    ]
