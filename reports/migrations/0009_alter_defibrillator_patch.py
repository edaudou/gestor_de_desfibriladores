# Generated by Django 3.2 on 2022-03-21 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_auto_20220321_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defibrillator',
            name='patch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='defibrillator', to='reports.patch'),
        ),
    ]
