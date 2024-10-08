# Generated by Django 5.1.1 on 2024-09-28 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xml_generator', '0003_alter_taxforminstance_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxform',
            name='system_prompt',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='taxforminstance',
            name='data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='taxforminstance',
            name='xml',
            field=models.TextField(blank=True, null=True),
        ),
    ]
