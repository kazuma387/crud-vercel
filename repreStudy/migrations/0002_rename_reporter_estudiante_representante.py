# Generated by Django 5.0.7 on 2024-07-30 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repreStudy', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estudiante',
            old_name='reporter',
            new_name='representante',
        ),
    ]
