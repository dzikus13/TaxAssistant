# Generated by Django 5.1.1 on 2024-09-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teryt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jednostkaadministracyjna',
            name='gmi',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='jednostkaadministracyjna',
            name='pow',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='jednostkaadministracyjna',
            name='rodz',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='jednostkaadministracyjna',
            name='woj',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='gmi',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='mz',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='pow',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='rm',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='rodz_gmi',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='miejscowosc',
            name='woj',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
