# Generated by Django 5.1.1 on 2024-09-28 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teryt', '0003_alter_jednostkaadministracyjna_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jednostkaadministracyjna',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
